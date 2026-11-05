#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper educativo para elyerromenu.com.
ADVERTENCIA: Antes de ejecutar, verifica:
1. https://elyerromenu.com/robots.txt (qué rutas están permitidas)
2. Términos de servicio del sitio
3. No recolectes datos personales (teléfonos, nombres) sin consentimiento
4. Respeta límites de tasa (rate limiting) para no saturar el servidor

Este script solo extrae datos públicos visibles en anuncios inmobiliarios.
Los datos se guardan en datos/brutos/elyerromenu/ (uno por anuncio) y
datos/limpios/elyerromenu/elyerromenu_unificado.json (resultado unificado).

Después de ejecutar, pasa los datos por tu pipeline de verificación municipal
(título primero + polígono de Diez de Octubre) antes de incluirlos en el informe.
"""

import json
import os
import re
import time
import hashlib
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ==================== CONFIGURACIÓN ====================
RAIZ = Path(__file__).resolve().parent.parent
URLS_OBJETIVO = [
    "https://elyerromenu.com/l/search/casas?page=1&location=62aa50c6dd41e7e0b8282f68",
    "https://elyerromenu.com/",
]

CARPETA_CRUDOS = RAIZ / "datos" / "brutos" / "elyerromenu"
CARPETA_LIMPIOS = RAIZ / "datos" / "limpios" / "elyerromenu"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; proyecto-matcom-10octubre/1.0; +educational)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "es-CU,es;q=0.9,en;q=0.8",
}
TIMEOUT = 20
PAUSA_ENTRE_PETICIONES = 3  # segundos, sé amable con el servidor
MAX_ANUNCIOS_POR_URL = 50   # límite de seguridad

# ==================== FUNCIONES ====================

def slug_id(url: str) -> str:
    """Genera un identificador único y seguro a partir de la URL."""
    return "elyerromenu-" + hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


def pedir_html(url: str) -> str | None:
    """Descarga el HTML de una URL con manejo de errores."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[ERROR] No se pudo descargar {url}: {e}")
        return None


def extraer_enlaces_anuncios(html: str, base_url: str) -> list[str]:
    """
    Extrae enlaces que parezcan anuncios individuales.
    Ajusta los selectores según la estructura real del sitio.
    """
    soup = BeautifulSoup(html, "html.parser")
    enlaces = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        texto = a.get_text(" ", strip=True).lower()
        if any(p in href.lower() for p in ["casa", "apartamento", "venta", "alquiler", "permuta", "inmueble", "anuncio"]):
            url_completa = urljoin(base_url, href)
            if urlparse(url_completa).netloc == urlparse(base_url).netloc:
                enlaces.add(url_completa)
    return list(enlaces)[:MAX_ANUNCIOS_POR_URL]


def extraer_datos_anuncio(html: str, url: str) -> dict:
    """
    Extrae campos de un anuncio individual.
    Los selectores son genéricos; ajústalos según el HTML real del sitio.
    """
    soup = BeautifulSoup(html, "html.parser")

    titulo = ""
    h1 = soup.find("h1")
    if h1:
        titulo = h1.get_text(" ", strip=True)

    texto_completo = soup.get_text(" ", strip=True)

    # Extraer precio (heurística muy básica)
    precio_monto = None
    precio_moneda = "USD"
    m = re.search(r"(\d[\d\.,]*)\s*(USD|CUP|\$|usd|cup)", texto_completo, re.IGNORECASE)
    if m:
        precio_monto = float(m.group(1).replace(",", "").replace(".", ""))
        if m.group(2).lower() in ("cup",):
            precio_moneda = "CUP"

    # Detectar operación por palabras clave
    operacion = "Sin clasificar"
    t_lower = (titulo + " " + texto_completo).lower()
    if any(p in t_lower for p in ["permuta", "intercambio", "cambio"]):
        operacion = "Permuta"
    elif any(p in t_lower for p in ["alquiler", "alquila", "renta"]):
        operacion = "Alquiler"
    elif any(p in t_lower for p in ["venta", "vendo", "se vende"]):
        operacion = "Venta"

    # Ubicación y zona (muy básica, se mejora con tu verificación municipal)
    ubicacion = "No especificado"
    zona = "No especificado"
    m_loc = re.search(
        r"(10\s*(?:de\s*)?octubre|diez\s*de\s*octubre|santos\s*suárez|lawton|la víbora|el sevillano|reparto flores|el mónaco)",
        t_lower,
        re.IGNORECASE,
    )
    if m_loc:
        ubicacion = m_loc.group(0)
        zona = m_loc.group(0)

    contacto_telefono = ""
    m_tel = re.search(r"(\d{2}\s*\d{3}\s*\d{4}|\d{8})", texto_completo)
    if m_tel:
        contacto_telefono = m_tel.group(0)

    return {
        "id_unico": slug_id(url),
        "fuente": "elyerromenu",
        "url_origen": url,
        "titulo": titulo,
        "precio": {
            "monto": precio_monto,
            "moneda": precio_moneda,
            "negociable": False,
            "nota": "",
        },
        "operacion": operacion,
        "detalles_propiedad": {
            "tipo": "Inmueble",
            "tipo_original": None,
            "ubicacion": ubicacion,
            "zona": zona,
            "distribucion": [],
        },
        "publicacion": {
            "autor": "elyerromenu",
            "enlace": url,
            "fecha": "",
            "grupo": "elyerromenu",
        },
        "contacto": {
            "telefono": contacto_telefono,
            "metodo": "Web",
            "enlace_elyerromenu": url,
        },
        "equipamiento_incluido": [],
        "servicios_y_caracteristicas": [],
        "extras": {},
        "fecha_verificacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_publicacion": None,
        "permuta": operacion == "Permuta",
        "estado": "activo",
        "motivo_estado": "Activo",
        "municipio_evidencia": "pendiente",
        "posibles_duplicados": [],
    }


def guardar_json_individual(datos: dict, carpeta: Path):
    """Guarda un JSON individual por anuncio."""
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre_archivo = datos["id_unico"] + ".json"
    ruta = carpeta / nombre_archivo
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    return ruta


def main():
    CARPETA_CRUDOS.mkdir(parents=True, exist_ok=True)
    CARPETA_LIMPIOS.mkdir(parents=True, exist_ok=True)

    todos_los_anuncios = []

    for url_base in URLS_OBJETIVO:
        print(f"\n[+] Procesando URL base: {url_base}")
        html_listado = pedir_html(url_base)
        if not html_listado:
            continue

        enlaces = extraer_enlaces_anuncios(html_listado, url_base)
        print(f"    Enlaces de anuncios encontrados: {len(enlaces)}")

        for enlace in enlaces:
            print(f"    Descargando anuncio: {enlace}")
            html_anuncio = pedir_html(enlace)
            if not html_anuncio:
                continue

            datos = extraer_datos_anuncio(html_anuncio, enlace)
            ruta_guardada = guardar_json_individual(datos, CARPETA_CRUDOS)
            print(f"    Guardado individual: {ruta_guardada.name}")

            todos_los_anuncios.append(datos)
            time.sleep(PAUSA_ENTRE_PETICIONES)

        time.sleep(PAUSA_ENTRE_PETICIONES)

    # Guardar JSON unificado de resultado
    ruta_unificado = CARPETA_LIMPIOS / "elyerromenu_unificado.json"
    with open(ruta_unificado, "w", encoding="utf-8") as f:
        json.dump(todos_los_anuncios, f, ensure_ascii=False, indent=2)

    print(f"\n[+] Total anuncios extraídos: {len(todos_los_anuncios)}")
    print(f"[+] JSON unificado guardado en: {ruta_unificado}")
    print(f"[+] JSON individuales guardados en: {CARPETA_CRUDOS}")
    print("\n[!] IMPORTANTE: Estos datos están SIN verificar municipalmente.")
    print("[!] Debes pasarlos por tu pipeline de verificación (título primero + polígono) antes de incluirlos en el informe.")


if __name__ == "__main__":
    main()
