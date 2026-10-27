#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para scrapear anuncios de inmobiliaria de El Caimán.

No se usan atributos class para buscar los anuncios. En su lugar se buscan
enlaces <a> cuyo href contenga '/propiedad/'.

Dentro de cada bloque de anuncio se extrae:
  - titulo: texto del nodo <p> con el título del anuncio.
  - precio: nodo que contenga 'USD' (formato $X,XXX USD).
  - telefono: se extrae desde la ficha del anuncio cuando esté visible.
Se priorizan los atributos data-testid cuando existan.

Resultados: datos/brutos/elcaiman_crudos.json  (titulo, precio, moneda, municipio, telefono, enlace, fuente)
"""

import json
import os
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# URL objetivo
URL = (
    "https://www.elcaiman.com/casas-en-la-habana"
    "?provincia=La+Habana&municipio=Diez+de+Octubre"
)

# Carpeta y archivo de salida
OUTPUT_DIR = "datos/brutos"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "elcaiman_crudos.json")

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

# Patrón para teléfonos cubanos
TELEFONO_PATTERN = re.compile(r'(?:\+53\s*)?[567]\d{7}', re.IGNORECASE)


def extraer_telefono(url):
    """Extrae el número de teléfono desde la ficha del anuncio."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return "NO DISPONIBLE"
        texto = resp.text
        matches = TELEFONO_PATTERN.findall(texto)
        if matches:
            tel = matches[0].strip().replace(' ', '')
            return tel
        return "NO DISPONIBLE"
    except Exception:
        return "NO DISPONIBLE"


def parse_precio_elcaiman(texto):
    """
    Convierte un texto de precio tipo "$4,000 USD" en (numero, moneda).
    Devuelve (None, "") si no se puede parsear.
    """
    if not texto:
        return None, ""

    texto = texto.strip()

    # Detectar moneda: código ISO de 3 letras o símbolo $
    moneda = ""
    m_moneda = re.search(r"\b([A-Z]{3})\b", texto)
    if m_moneda:
        moneda = m_moneda.group(1).upper()
    elif "$" in texto:
        moneda = "USD"

    # Extraer el primer grupo numérico (admite comas y puntos)
    m_num = re.search(r"[\d][\d.,]*", texto)
    if not m_num:
        return None, moneda

    num_str = m_num.group(0).replace(",", "").replace(".", "")

    try:
        valor = int(num_str)
    except ValueError:
        try:
            valor = float(num_str)
        except ValueError:
            valor = None

    return valor, moneda


def extraer_anuncios(html, base_url):
    """
    Parsea el HTML y devuelve una lista de diccionarios con
    titulo, precio (numero), moneda, municipio, enlace y fuente.
    """
    soup = BeautifulSoup(html, "html.parser")
    anuncios = []
    enlaces_vistos = set()

    # Buscar todos los <a> cuyo href contenga /propiedad/
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/propiedad/" not in href:
            continue

        enlace_absoluto = urljoin(base_url, href)
        if enlace_absoluto in enlaces_vistos:
            continue
        enlaces_vistos.add(enlace_absoluto)

        # Extraer título: buscar <p> dentro del <a> que no sea precio ni ubicación
        titulo = ""
        parrafos = a.find_all("p")
        for p in parrafos:
            t = p.get_text(strip=True)
            if t and "USD" not in t and "$" not in t:
                # Saltar el párrafo de ubicación (contiene "hab" o "·")
                if "hab" not in t.lower() and "·" not in t:
                    titulo = t
                    break

        # Si no se encontró título por párrafos, usar aria-label o texto del enlace
        if not titulo:
            aria = a.get("aria-label", "")
            if aria:
                # Formato: "Título — Ubicación"
                titulo = aria.split("—")[0].strip()
            if not titulo:
                titulo = a.get_text(strip=True)

        # Extraer precio: buscar <p> con USD o $
        precio_texto = ""
        for p in parrafos:
            t = p.get_text(strip=True)
            if "USD" in t or "$" in t:
                precio_texto = t
                break

        precio_numero, moneda = parse_precio_elcaiman(precio_texto)
        telefono = extraer_telefono(enlace_absoluto)
        time.sleep(1)

        anuncios.append({
            "titulo": titulo,
            "precio": precio_numero,
            "moneda": moneda,
            "municipio": "Diez de Octubre",
            "telefono": telefono,
            "enlace": enlace_absoluto,
            "fuente": "elcaiman",
        })

        # Pausa entre peticiones
        time.sleep(2)

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

    html = respuesta.text
    anuncios = extraer_anuncios(html, URL)

    print(f"Se encontraron {len(anuncios)} anuncios.")
    guardar_json(anuncios, OUTPUT_FILE)
    print(f"Resultados guardados en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
