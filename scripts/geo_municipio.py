#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades geográficas para verificar la pertenencia al municipio Diez de Octubre.

Fuente geoespacial:
    /home/luis/Downloads/lha.geojson (15 municipios de La Habana)

El módulo:
- carga el polígono de Diez de Octubre (DPA 23.09);
- prueba si un punto (lat, lon) cae dentro del polígono;
- geocodifica topónimos con Nominatim y guarda caché local para no repetir
  consultas.

La caché se guarda en ``datos/geo/geocoding_lha.json`` y se versiona para que
la verificación sea reproducible sin volver a consultar el servicio.
"""

import json
import os
import time
import urllib.parse
import urllib.request

GEOJSON = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "datos", "geo", "lha.geojson",
)
CACHE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "datos", "geo", "geocoding_lha.json",
)
MUNICIPIO_OBJETIVO = "Diez de Octubre"

USER_AGENT = "proyecto-mercado-10-octubre/1.0 (uso académico)"
NOMINATIM = "https://nominatim.openstreetmap.org/search"


def cargar_poligono(ruta=GEOJSON, municipio=MUNICIPIO_OBJETIVO):
    """Devuelve la lista de anillos del polígono del municipio indicado."""
    with open(ruta, encoding="utf-8") as f:
        geojson = json.load(f)

    for feature in geojson["features"]:
        props = feature.get("properties") or {}
        if props.get("municipality") == municipio:
            geometria = feature["geometry"]
            if geometria["type"] == "Polygon":
                return geometria["coordinates"]
            if geometria["type"] == "MultiPolygon":
                return [anillo for poligono in geometria["coordinates"] for anillo in poligono]

    raise ValueError(f"No se encontró el municipio {municipio!r} en {ruta}")


def limites(anillos):
    """Bounding box (lon_min, lat_min, lon_max, lat_max) del polígono."""
    puntos = [p for anillo in anillos for p in anillo]
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]
    return min(xs), min(ys), max(xs), max(ys)


def punto_en_poligono(lon, lat, anillos):
    """Ray casting: True si el punto (lon, lat) está dentro del polígono."""
    dentro = False
    for anillo in anillos:
        n = len(anillo)
        j = n - 1
        for i in range(n):
            xi, yi = anillo[i]
            xj, yj = anillo[j]
            if (yi > lat) != (yj > lat):
                x_corte = (xj - xi) * (lat - yi) / (yj - yi) + xi
                if lon < x_corte:
                    dentro = not dentro
            j = i
    return dentro


def distancia_aproximada_km(lon, lat, anillos):
    """Distancia mínima aproximada del punto al borde del polígono, en km."""
    import math

    mejor = float("inf")
    for anillo in anillos:
        for i in range(len(anillo) - 1):
            x1, y1 = anillo[i]
            x2, y2 = anillo[i + 1]
            dx = (x2 - x1) * 111.32 * math.cos(math.radians(lat))
            dy = (y2 - y1) * 110.57
            px = (lon - x1) * 111.32 * math.cos(math.radians(lat))
            py = (lat - y1) * 110.57
            largo2 = dx * dx + dy * dy
            if largo2 == 0:
                dist = (px * px + py * py) ** 0.5
            else:
                t = max(0.0, min(1.0, (px * dx + py * dy) / largo2))
                dist = ((px - t * dx) ** 2 + (py - t * dy) ** 2) ** 0.5
            mejor = min(mejor, dist)
    return mejor


def cargar_cache(ruta=CACHE_FILE):
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_cache(cache, ruta=CACHE_FILE):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def geocodificar(consulta, cache, pausa=1.1):
    """Geocodifica una consulta con Nominatim y la guarda en caché.

    Devuelve un diccionario con lat, lon, municipio declarado por OSM y el
    nombre mostrado, o ``None`` si no hay resultado.
    """
    clave = consulta.strip().lower()
    if clave in cache:
        return cache[clave]

    url = NOMINATIM + "?" + urllib.parse.urlencode({
        "q": consulta,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    })
    peticion = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(peticion, timeout=25) as respuesta:
            datos = json.load(respuesta)
    except Exception as error:  # red lenta o límite del servicio
        cache[clave] = {"consulta": consulta, "error": str(error)}
        guardar_cache(cache)
        time.sleep(pausa)
        return cache[clave]

    if datos:
        primero = datos[0]
        direccion = primero.get("address") or {}
        cache[clave] = {
            "consulta": consulta,
            "lat": float(primero["lat"]),
            "lon": float(primero["lon"]),
            "municipio_osm": direccion.get("municipality")
            or direccion.get("city")
            or direccion.get("town")
            or direccion.get("village"),
            "tipo_osm": primero.get("type"),
            "nombre_osm": primero.get("name"),
            "display_name": primero.get("display_name"),
        }
    else:
        cache[clave] = {"consulta": consulta, "sin_resultado": True}

    guardar_cache(cache)
    time.sleep(pausa)
    return cache[clave]
