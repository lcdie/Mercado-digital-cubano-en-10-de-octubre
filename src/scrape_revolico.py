#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para scrapear anuncios de inmobiliaria en Revolico.

No se usan atributos class para buscar los anuncios, ya que Revolico usa
clases dinámicas (generadas por CSS-in-JS). En su lugar se buscan enlaces
<a> cuyo href contenga patrones de anuncio (/item/, /anuncio/ o /ad/).

Dentro de cada bloque de anuncio se extrae:
  - titulo: texto del anuncio (el nodo de texto que NO es el precio).
  - precio: el nodo/elemento cuyo texto contenga un código de moneda (USD, CUP, etc.).
Se priorizan los atributos data-testid (data-testid="ad-card",
data-testid="ad-price") cuando existan en el HTML.

El precio se convierte a número y se conserva la moneda declarada.
El municipio se asume como "Diez de Octubre" porque la URL de búsqueda
ya filtra por ese municipio (evita falsos positivos de detección por
palabras clave).

Resultados: datos/brutos/revolico_crudos.json  (titulo, precio, moneda,
municipio, enlace, sospechoso)
"""

import json
import os
import re
import time
import unicodedata
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# URL objetivo (ya filtra por municipio diez-de-octubre)
URL = (
    "https://www.revolico.com/search"
    "?category=inmobiliaria&province=la-habana&municipio=diez-de-octubre"
)

# Patrones de href que identifican un anuncio. Revolico usa /item/<slug>-<id>;
# se mantienen /anuncio/ y /ad/ por si el sitio los usa en otras secciones.
ANUNCIO_HREF_PATTERNS = ("/item/", "/anuncio/", "/ad/")

# Carpeta y archivo de salida (coincide con el resto del repositorio)
OUTPUT_DIR = "datos/brutos"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "revolico_crudos.json")
SIN_MUNICIPIO_FILE = os.path.join(OUTPUT_DIR, "revolico_sin_municipio.json")

# Cabeceras con un User-Agent real de navegador
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Umbrales para marcar precios como sospechosos (outliers obvios)
PRECIO_MINIMO_SOSPECHOSO = 100
PRECIO_MAXIMO_SOSPECHOSO = 1_000_000


def _sin_tildes(texto):
    """Devuelve el texto en minúsculas sin tildes ni caracteres especiales."""
    if not texto:
        return ""
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


# Municipios de La Habana con sus variantes de escritura.
# Se mantiene por compatibilidad, aunque el scraper ahora fuerza el municipio
# desde la URL de búsqueda.
MUNICIPIOS = [
    ("Diez de Octubre", ["diez de octubre", "10 de octubre", "diez-de-octubre", "10-de-octubre"]),
    ("La Víbora", ["la vibora", "la víbora", "la-vibora", "vibora", "víbora"]),
    ("Santos Suárez", ["santos suarez", "santos suárez", "santo suarez", "santo suárez", "santos-suarez", "santo-suarez"]),
    ("Lawton", ["lawton"]),
    ("El Sevillano", ["el sevillano", "sevillano"]),
    ("Luyano", ["luyano"]),
    ("Nuevo Vedado", ["nuevo vedado", "nuevo-vedado"]),
    ("Vedado", ["vedado"]),
    ("Playa", ["playa"]),
    ("Cerro", ["cerro"]),
    ("Mantilla", ["mantilla"]),
    ("Guanabo", ["guanabo"]),
    ("Centro Habana", ["centro habana", "centro-habana"]),
    ("Habana Vieja", ["habana vieja", "habana-vieja"]),
    ("Plaza de la Revolución", ["plaza de la revolucion", "plaza de la revolución", "plaza-de-la-revolucion"]),
    ("Marianao", ["marianao"]),
    ("Guanabacoa", ["guanabacoa"]),
    ("San Miguel del Padrón", ["san miguel del padron", "san miguel del padrón", "san miguel"]),
    ("Regla", ["regla"]),
    ("Casablanca", ["casablanca"]),
    ("Cotorro", ["cotorro"]),
    ("Boyeros", ["boyeros"]),
    ("Arroyo Naranjo", ["arroyo naranjo", "arroyo-naranjo"]),
    ("La Lisa", ["la lisa", "la-lisa"]),
    ("San Francisco de Paula", ["san francisco de paula", "san-francisco-de-paula"]),
]


def detectar_municipio(titulo, enlace):
    """
    Detecta el municipio del anuncio buscando palabras clave en el título
    y en el slug del enlace. Devuelve el nombre del municipio o
    "no especificado" si no se encuentra.
    """
    texto = _sin_tildes(titulo) + " " + _sin_tildes(enlace)

    for nombre, variantes in MUNICIPIOS:
        for variante in variantes:
            if variante in texto:
                return nombre

    return "no especificado"


def _texto_precio(nodo):
    """
    Devuelve el texto de un elemento descendiente que contenga un código de
    moneda de 3 letras o un símbolo de moneda.
    Prioriza data-testid='ad-price'.
    """
    if nodo is None:
        return ""

    precio_el = nodo.find(attrs={"data-testid": "ad-price"})
    if precio_el is not None:
        return precio_el.get_text(strip=True)

    for elem in nodo.find_all(string=lambda t: t and re.search(r"\b[A-Z]{3}\b|\$|€|£|¥", t)):
        padre = elem.parent
        if padre is not None:
            return padre.get_text(strip=True)
    return ""


def parse_precio(texto):
    """
    Convierte un texto de precio tipo "25,000 USD" o "50,000 CUP" en
    (numero, moneda). Detecta cualquier código de moneda de 3 letras (ISO 4217)
    o símbolo ($, €, £, ¥) solo cuando esté adyacente al número.
    Devuelve (None, "") si no se puede parsear.

    CORREGIDO: ya no elimina todos los puntos/comas indiscriminadamente.
    - Las comas se tratan como separadores de miles y se quitan.
    - Un punto con 1-2 decimales se conserva como decimal.
    - Un punto con 3 decimales se trata como separador de miles.
    """
    if not texto:
        return None, ""

    texto = texto.strip()

    # Buscar número con moneda adyacente (antes o después)
    m = re.search(
        r"\b([A-Z]{3}|[\$€£¥])\s*([\d][\d.,]*)|([\d][\d.,]*)\s*([A-Z]{3}|[\$€£¥])",
        texto,
    )
    if not m:
        return None, ""

    moneda = ""
    num_str = ""

    if m.group(1) and m.group(2):
        moneda_raw = m.group(1)
        num_str = m.group(2)
    elif m.group(3) and m.group(4):
        num_str = m.group(3)
        moneda_raw = m.group(4)

    if moneda_raw == "$":
        moneda = "USD"
    elif moneda_raw == "€":
        moneda = "EUR"
    elif moneda_raw == "£":
        moneda = "GBP"
    elif moneda_raw == "¥":
        moneda = "JPY"
    else:
        moneda = moneda_raw.upper()

    # Limpiar número: quitar comas de miles
    num_str = num_str.replace(",", "")

    # Manejo de punto: decimal vs separador de miles
    if "." in num_str:
        partes = num_str.split(".")
        if len(partes) > 2:
            # Varios puntos -> quitar todos (formato raro de miles)
            num_str = "".join(partes)
        else:
            entero, decimal = partes
            if len(decimal) == 3:
                # Probable separador de miles (1.250)
                num_str = entero + decimal
            else:
                # Probable decimal (50.50)
                num_str = entero + "." + decimal

    try:
        if "." in num_str:
            valor = float(num_str)
        else:
            valor = int(num_str)
    except ValueError:
        return None, ""

    return valor, moneda


def _titulo_del_anuncio(enlace, precio_texto):
    """
    Extrae el título del anuncio desde dentro del <a>.
    Es el texto del bloque que no corresponde al precio.
    """
    if enlace is None:
        return ""

    parrafos = enlace.find_all("p")
    if parrafos:
        patron_precio = re.compile(
            r"\b([A-Z]{3}|[\$€£¥])\s*([\d][\d.,]*)|([\d][\d.,]*)\s*([A-Z]{3}|[\$€£¥])"
        )
        for p in parrafos:
            t = p.get_text(strip=True)
            if t and not patron_precio.search(t):
                return t
        for p in parrafos:
            t = p.get_text(strip=True)
            if t:
                return t

    texto_completo = enlace.get_text(" ", strip=True)
    if precio_texto:
        texto_completo = texto_completo.replace(precio_texto, " ").strip()
    return " ".join(texto_completo.split())


def es_boton_publicar(titulo, enlace):
    """Detecta el botón 'Publicar anuncio' que no es un anuncio real."""
    if not titulo:
        return False
    if "publicar anuncio" in _sin_tildes(titulo).strip():
        return True
    if enlace and "/item/publish" in enlace:
        return True
    return False


def es_titulo_solo_precio(titulo):
    """Detecta títulos que son solo un precio sin descripción."""
    if not titulo:
        return False
    t = _sin_tildes(titulo).strip()
    # Si solo contiene número, moneda y símbolos, es solo precio
    return bool(re.fullmatch(r"[\d.,\s\$€£¥usdcup]+", t)) and len(t) <= 12


def extraer_precio(enlace):
    """
    Busca el precio del anuncio dentro del bloque del enlace.
    Prioriza data-testid='ad-card' (contenedor) + data-testid='ad-price'.
    Fallback: cualquier elemento con moneda en el texto.

    Devuelve un diccionario con: texto, numero, moneda
    """
    resultado = {"texto": "", "numero": None, "moneda": ""}

    card = enlace.find_parent(attrs={"data-testid": "ad-card"})
    if card is not None:
        texto = _texto_precio(card)
        if texto:
            numero, moneda = parse_precio(texto)
            resultado["texto"] = texto
            resultado["numero"] = numero
            resultado["moneda"] = moneda
            return resultado

    for nodo in (enlace, enlace.parent):
        texto = _texto_precio(nodo)
        if texto:
            numero, moneda = parse_precio(texto)
            resultado["texto"] = texto
            resultado["numero"] = numero
            resultado["moneda"] = moneda
            return resultado

    return resultado


def href_es_anuncio(href):
    return any(p in href for p in ANUNCIO_HREF_PATTERNS)


def precio_es_sospechoso(numero, moneda):
    """Marca como sospechoso precios fuera de rango realista para la zona."""
    if numero is None:
        return False
    if numero < PRECIO_MINIMO_SOSPECHOSO:
        return True
    if numero > PRECIO_MAXIMO_SOSPECHOSO:
        return True
    return False


def extraer_anuncios(html, base_url):
    """
    Parsea el HTML y devuelve una lista de diccionarios con
    titulo, precio (numero), moneda, municipio, enlace y sospechoso.
    """
    soup = BeautifulSoup(html, "html.parser")
    anuncios = []
    enlaces_vistos = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href_es_anuncio(href):
            continue

        enlace_absoluto = urljoin(base_url, href)
        if enlace_absoluto in enlaces_vistos:
            continue
        enlaces_vistos.add(enlace_absoluto)

        # Extraer título y precio
        precio_info = extraer_precio(a)
        titulo = _titulo_del_anuncio(a, precio_info["texto"])

        # Descartar botón de publicar y basura obvia
        if es_boton_publicar(titulo, enlace_absoluto):
            continue

        # Municipio: forzar "Diez de Octubre" porque la URL ya filtra por ese
        # municipio. Se conserva la detección por palabras clave como referencia
        # pero no se usa para reasignar a otros municipios.
        municipio = "Diez de Octubre"

        # Detectar si el precio es sospechoso (outlier)
        sospechoso = precio_es_sospechoso(precio_info["numero"], precio_info["moneda"]) \
            or es_titulo_solo_precio(titulo)

        anuncios.append({
            "titulo": titulo,
            "precio": precio_info["numero"],
            "moneda": precio_info["moneda"],
            "municipio": municipio,
            "enlace": enlace_absoluto,
            "sospechoso": sospechoso,
        })

    return anuncios


def guardar_json(anuncios, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(anuncios, f, ensure_ascii=False, indent=2)


def main():
    print(f"Descargando: {URL}")
    try:
        respuesta = requests.get(URL, headers=HEADERS, timeout=30)
        respuesta.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al descargar la página: {e}")
        return

    time.sleep(2)

    html = respuesta.text
    anuncios = extraer_anuncios(html, URL)

    print(f"Se encontraron {len(anuncios)} anuncios.")
    guardar_json(anuncios, OUTPUT_FILE)
    print(f"Resultados guardados en: {OUTPUT_FILE}")

    # Archivo aparte con los anuncios que no tienen municipio especificado
    # (conservado por compatibilidad, aunque ahora el municipio se fuerza)
    sin_municipio = [a for a in anuncios if a["municipio"] == "no especificado"]
    guardar_json(sin_municipio, SIN_MUNICIPIO_FILE)
    print(f"Anuncios sin municipio guardados en: {SIN_MUNICIPIO_FILE} ({len(sin_municipio)} anuncios)")


if __name__ == "__main__":
    main()
