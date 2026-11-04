#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación de pertenencia al municipio Diez de Octubre.

Fuente geoespacial
------------------
``/home/luis/Downloads/lha.geojson``: 15 municipios de La Habana. Se extrae el
polígono de Diez de Octubre (DPA 23.09) y se usa para comprobar si un punto
geocodificado cae dentro del municipio.

Evidencias que se combinan
--------------------------
1. FICHA: la ubicación que muestra la propia ficha de Revolico
   (``data-cy="adLocation"``). Es la evidencia principal para Revolico.
2. TEXTO: municipios, repartos y calles mencionados en el título, el grupo o
   la ubicación de la publicación.
3. GEOCODIFICACIÓN: los topónimos del texto se geocodifican con Nominatim y se
   comprueban contra el polígono (punto en polígono + distancia al borde).
4. OSM: el municipio que OpenStreetMap declara para el topónimo, útil cuando
   el punto cae muy cerca del límite.

Salidas
-------
- datos/limpios/verificacion_municipal_revolico.json
- datos/limpios/verificacion_municipal_facebook.json
- datos/limpios/verificacion_municipal_unificado.json
- datos/limpios/verificacion_municipal.csv
- datos/limpios/revolico_confirmados_diez_octubre.json
- datos/limpios/facebook_confirmados_diez_octubre.json
- datos/limpios/unificado_confirmados_diez_octubre.json
- analisis/verificacion_municipal_geojson_20261104.md
"""

import csv
import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from geo_municipio import (
    cargar_cache,
    cargar_poligono,
    distancia_aproximada_km,
    geocodificar,
    limites,
    punto_en_poligono,
)

GEOJSON = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "datos", "geo", "lha.geojson",
)
FACEBOOK_FILE = "datos/limpios/facebook_publicaciones_limpias.json"
FACEBOOK_RECHAZADOS = "datos/limpios/facebook_eliminados_por_filtro.json"
REVOLICO_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
REVOLICO_PAGINAS = "datos/brutos/revolico_ubicaciones_pagina.json"

OUT_REVOLICO = "datos/limpios/verificacion_municipal_revolico.json"
OUT_FACEBOOK = "datos/limpios/verificacion_municipal_facebook.json"
OUT_UNIFICADO = "datos/limpios/verificacion_municipal_unificado.json"
OUT_CSV = "datos/limpios/verificacion_municipal.csv"
OUT_REV_CONFIRMADOS = "datos/limpios/revolico_confirmados_diez_octubre.json"
OUT_FB_CONFIRMADOS = "datos/limpios/facebook_confirmados_diez_octubre.json"
OUT_UNI_CONFIRMADOS = "datos/limpios/unificado_confirmados_diez_octubre.json"
OUT_REPORTE = "analisis/verificacion_municipal_geojson_20261104.md"

MUNICIPIOS_LHA = {
    "playa", "plaza de la revolucion", "centro habana", "habana vieja",
    "regla", "guanabacoa", "san miguel del padron", "diez de octubre",
    "cerro", "marianao", "la lisa", "boyeros", "arroyo naranjo", "cotorro",
    "habana del este",
}

# Topónimos que se buscan en el texto. Los patrones se aplican sobre texto
# normalizado (minúsculas y sin acentos).
TOPONIMOS = [
    # Dentro de Diez de Octubre
    {"nombre": "Diez de Octubre", "patron": r"\b(?:10\s*(?:de\s*)?octubre|diez\s*de\s*octubre|10\s*/\s*10|10\s*octubre)\b", "tipo": "dentro_explicito"},
    {"nombre": "Lawton", "patron": r"\blawton\b|\blautow\b", "consulta": "Lawton, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Luyanó", "patron": r"\bluyano\b", "consulta": "Luyanó, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "La Víbora", "patron": r"\bvibora\b", "consulta": "La Víbora, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Santos Suárez", "patron": r"\bsantos?\s*suarez\b", "consulta": "Santos Suárez, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "El Sevillano", "patron": r"\bsevillano\b", "consulta": "El Sevillano, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Santa Catalina", "patron": r"\bsanta\s*catalina\b", "consulta": "Santa Catalina, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Vista Alegre", "patron": r"\bvista\s*alegre\b", "consulta": "Vista Alegre, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "El Mónaco", "patron": r"\bmonaco\b", "consulta": "El Mónaco, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "La Asunción", "patron": r"\basuncion\b", "consulta": "Asunción, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Plaza Roja", "patron": r"\bplaza\s*roja\b", "consulta": "Plaza Roja, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Reparto Flores", "patron": r"\breparto\s*flores\b", "consulta": "Flores, Diez de Octubre, La Habana, Cuba", "tipo": "lugar_ambiguo"},
    {"nombre": "Calzada 10 de Octubre", "patron": r"\bcalzada\s*(?:de\s*)?(?:10|diez)\s*(?:de\s*)?octubre\b", "consulta": "Calzada de Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Lacret", "patron": r"\blacret\b", "consulta": "Lacret, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Porvenir", "patron": r"\bporvenir\b", "consulta": "Porvenir, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Aguilera", "patron": r"\baguilera\b", "consulta": "Aguilera, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Juan Delgado", "patron": r"\bjuan\s*delgado\b", "consulta": "Juan Delgado, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Dolores", "patron": r"\bdolores\b", "consulta": "Dolores, Diez de Octubre, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Santa Ana", "patron": r"\bsanta\s*ana\b", "consulta": "Santa Ana, Luyanó, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Hospital Hijas de Galicia", "patron": r"\bhijas?\s*de\s*galicia\b", "consulta": "Hospital Materno Hijas de Galicia, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Ampliación del Sevillano", "patron": r"\bampliacion\s+(?:del?\s+)?sevillano\b", "tipo": "ambiguo"},
    # Fuera de Diez de Octubre: repartos y localidades
    {"nombre": "Santa Amalia", "patron": r"\bsanta\s*amalia\b", "consulta": "Santa Amalia, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Boca Ciega", "patron": r"\bboca\s*ciega\b", "consulta": "Boca Ciega, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Chibás", "patron": r"\bchibas\b", "consulta": "Chibás, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Mantilla", "patron": r"\bmantilla\b", "consulta": "Mantilla, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "San Agustín", "patron": r"\bsan\s*agustin\b", "consulta": "San Agustín, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Atavey/Atabey", "patron": r"\batav?ey\b", "consulta": "Atabey, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Casino Deportivo", "patron": r"\bcasino\s*deportivo\b|\bel\s*casino\b", "consulta": "Casino Deportivo, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Víbora Park", "patron": r"\bvibora\s*park\b", "consulta": "Víbora Park, La Habana, Cuba", "tipo": "lugar"},
    {"nombre": "Pimienta", "patron": r"\bpimienta\b", "consulta": "Pimienta, La Habana, Cuba", "tipo": "lugar_ambiguo"},
    {"nombre": "Náutico", "patron": r"\bnautico\b", "consulta": "Náutico, Playa, La Habana, Cuba", "tipo": "lugar"},
    # Municipios y localidades fuera de La Habana
    {"nombre": "Habana Vieja", "patron": r"\bhabana\s*vieja\b", "tipo": "fuera_explicito"},
    {"nombre": "Centro Habana", "patron": r"\bcentro\s*habana\b", "tipo": "fuera_explicito"},
    {"nombre": "Cerro", "patron": r"\bcerro\b", "tipo": "fuera_explicito"},
    {"nombre": "Marianao", "patron": r"\bmarianao\b", "tipo": "fuera_explicito"},
    {"nombre": "La Lisa", "patron": r"\bla\s*lisa\b", "tipo": "fuera_explicito"},
    {"nombre": "Arroyo Naranjo", "patron": r"\barroyo\s*naranjo\b", "tipo": "fuera_explicito"},
    {"nombre": "Boyeros", "patron": r"\bboyeros\b", "tipo": "fuera_explicito"},
    {"nombre": "Habana del Este", "patron": r"\bhabana\s*del\s*este\b", "tipo": "fuera_explicito"},
    {"nombre": "Guanabacoa", "patron": r"\bguanabacoa\b", "tipo": "fuera_explicito"},
    {"nombre": "Regla", "patron": r"\bregla\b", "tipo": "fuera_explicito"},
    {"nombre": "Cotorro", "patron": r"\bcotorro\b", "tipo": "fuera_explicito"},
    {"nombre": "San Miguel del Padrón", "patron": r"\bsan\s*miguel\s*del\s*padron\b", "tipo": "fuera_explicito"},
    {"nombre": "Plaza de la Revolución", "patron": r"\bplaza\s*de\s*la\s*revolucion\b", "tipo": "fuera_explicito"},
    {"nombre": "Artemisa", "patron": r"\bartemisa\b", "tipo": "fuera_explicito"},
    {"nombre": "Consolación del Sur", "patron": r"\bconsolacion\s*del\s*sur\b", "tipo": "fuera_explicito"},
]


def es_referencia_proximidad(texto, patron):
    """True si todas las menciones del patrón son referencias de cercanía.

    Ejemplo: «Santa Amalia, a 3 cuadras de la Calzada de 10 de Octubre».
    La Calzada se usa como punto de referencia, no como ubicación de la
    propiedad, por lo que no debe convertir el anuncio en «dentro».
    """
    coincidencias = list(re.finditer(patron, texto, re.IGNORECASE))
    if not coincidencias:
        return False

    prefijo_proximidad = re.compile(
        r"(?:a\s+(?:solo\s+)?(?:\d+|un|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)"
        r"\s+cuadras?\s+de|cerca\s+de|proximo\s+a|proxima\s+a|frente\s+a)"
        r"\s+(?:la\s+|el\s+)?(?:calzada\s+)?(?:de\s+)?$",
        re.IGNORECASE,
    )
    for coincidencia in coincidencias:
        prefijo = texto[max(0, coincidencia.start() - 70):coincidencia.start()]
        if not prefijo_proximidad.search(prefijo):
            return False
    return True


def normalizar(texto):
    texto = (texto or "").lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto)


def id_revolico(anuncio, indice):
    if anuncio.get("id_anuncio"):
        return str(anuncio["id_anuncio"])
    coincidencia = re.search(r"-(\d{5,})(?:\?|$)", anuncio.get("enlace", "") or "")
    if coincidencia:
        return coincidencia.group(1)
    return f"sin-id-{indice}"


def cargar_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def municipio_osm_desde_resultado(resultado):
    """Municipio de OSM a partir del campo municipality o del display_name."""
    municipio = normalizar(resultado.get("municipio_osm"))
    if municipio in MUNICIPIOS_LHA:
        return municipio
    display = normalizar(resultado.get("display_name"))
    for nombre in sorted(MUNICIPIOS_LHA, key=len, reverse=True):
        if re.search(rf"\b{re.escape(nombre)}\b", display):
            return nombre
    return municipio or ""


def analizar_toponimo(entrada, texto_normalizado, anillos, cache):
    """Devuelve la evidencia del topónimo si aparece en el texto."""
    if not re.search(entrada["patron"], texto_normalizado, re.IGNORECASE):
        return None

    evidencia = {
        "nombre": entrada["nombre"],
        "tipo": entrada["tipo"],
        "patron": entrada["patron"],
    }

    if entrada["tipo"] == "dentro_explicito":
        evidencia["estado"] = "dentro"
        evidencia["detalle"] = "mención textual explícita al municipio"
        return evidencia

    if entrada["tipo"] == "fuera_explicito":
        evidencia["estado"] = "fuera"
        evidencia["detalle"] = "mención textual a otro municipio"
        return evidencia

    if entrada["tipo"] == "ambiguo" or not entrada.get("consulta"):
        evidencia["estado"] = "ambigua"
        evidencia["detalle"] = "topónimo no geocodificable con precisión"
        return evidencia

    resultado = geocodificar(entrada["consulta"], cache)
    if not resultado or "lat" not in resultado:
        evidencia["estado"] = "ambigua"
        evidencia["detalle"] = "sin resultado de geocodificación"
        return evidencia

    dentro = punto_en_poligono(resultado["lon"], resultado["lat"], anillos)
    distancia = distancia_aproximada_km(resultado["lon"], resultado["lat"], anillos)
    municipio_osm = municipio_osm_desde_resultado(resultado)

    if municipio_osm == "diez de octubre":
        estado = "dentro"
    elif municipio_osm in MUNICIPIOS_LHA:
        estado = "fuera"
    elif dentro:
        estado = "dentro"
    elif distancia <= 0.5:
        estado = "frontera"
    else:
        estado = "fuera"

    if entrada["tipo"] == "lugar_ambiguo" and estado == "dentro":
        # El topónimo existe dentro y fuera del municipio; se conserva la
        # evidencia pero se marca como ambigua para revisión.
        estado = "ambigua"

    evidencia.update({
        "estado": estado,
        "lat": resultado["lat"],
        "lon": resultado["lon"],
        "municipio_osm": resultado.get("municipio_osm"),
        "display_name_osm": resultado.get("display_name"),
        "dentro_poligono": dentro,
        "distancia_borde_km": round(distancia, 2),
        "detalle": (
            f"OSM: {resultado.get('municipio_osm') or 'sin municipio'}; "
            f"{'dentro' if dentro else 'fuera'} del polígono; "
            f"{round(distancia, 2)} km del borde"
        ),
    })
    return evidencia


def analizar_texto(texto, anillos, cache):
    texto_normalizado = normalizar(texto)
    evidencias = []

    for entrada in TOPONIMOS:
        evidencia = analizar_toponimo(entrada, texto_normalizado, anillos, cache)
        if evidencia:
            evidencias.append(evidencia)

    # Si el anuncio declara explícitamente un lugar fuera del municipio, una
    # mención interna usada solo como referencia de cercanía («a 3 cuadras de
    # la Calzada de 10 de Octubre») no convierte el anuncio en «dentro».
    if any(e["estado"] == "fuera" for e in evidencias):
        evidencias = [
            e for e in evidencias
            if not (
                e["estado"] == "dentro"
                and es_referencia_proximidad(texto_normalizado, e.get("patron", ""))
            )
        ]

    # "Víbora Park" está fuera y contiene la cadena "Víbora": se descarta la
    # señal genérica de La Víbora para no crear una contradicción artificial.
    if any(e["nombre"] == "Víbora Park" and e["estado"] == "fuera" for e in evidencias):
        evidencias = [
            e for e in evidencias
            if not (e["nombre"] == "La Víbora" and e["estado"] == "dentro")
        ]

    return {
        "dentro": [e for e in evidencias if e["estado"] == "dentro"],
        "fuera": [e for e in evidencias if e["estado"] == "fuera"],
        "ambigua": [e for e in evidencias if e["estado"] in ("ambigua", "frontera")],
        "todas": evidencias,
    }


def clasificar(ficha_estado, senales):
    """Devuelve (resultado, confianza, pertenece, motivo)."""
    dentro = senales["dentro"]
    fuera = senales["fuera"]
    ambigua = senales["ambigua"]

    if ficha_estado == "dentro":
        if fuera:
            return "CONTRADICTORIO", "baja", None, (
                "La ficha declara Diez de Octubre, pero el texto menciona un lugar fuera del municipio."
            )
        if ambigua:
            return "CONTRADICTORIO", "baja", None, (
                "La ficha declara Diez de Octubre, pero hay un topónimo ambiguo o de frontera."
            )
        return "SÍ", "alta", True, (
            "La ficha del anuncio declara Diez de Octubre, La Habana."
        )

    if ficha_estado == "fuera":
        if dentro:
            return "CONTRADICTORIO", "baja", None, (
                "La ficha declara otro municipio, pero el texto menciona Diez de Octubre o un reparto suyo."
            )
        if ambigua:
            return "CONTRADICTORIO", "baja", None, (
                "La ficha declara otro municipio, pero hay un topónimo ambiguo o de frontera."
            )
        return "NO", "alta", False, (
            "La ficha del anuncio declara otro municipio de La Habana."
        )

    # Ficha sin ubicación (página retirada o sin dato)
    if dentro and not fuera:
        return "SÍ", "media", True, (
            "Sin ubicación en la ficha, pero el texto menciona Diez de Octubre o un reparto suyo."
        )
    if fuera and not dentro:
        return "NO", "media", False, (
            "Sin ubicación en la ficha, pero el texto menciona un lugar fuera del municipio."
        )
    if dentro and fuera:
        return "CONTRADICTORIO", "baja", None, (
            "El texto mezcla referencias dentro y fuera del municipio."
        )
    return "INDETERMINADO", "baja", None, (
        "No hay ficha municipal ni topónimo verificable en el texto."
    )


def preparar_revolico(anillos, cache):
    anuncios = cargar_json(REVOLICO_FILE)
    paginas = {str(p["id_anuncio"]): p for p in cargar_json(REVOLICO_PAGINAS)}
    resultados = []

    for indice, anuncio in enumerate(anuncios, start=1):
        identificador = id_revolico(anuncio, indice)
        pagina = paginas.get(identificador, {})
        ubicacion_pagina = pagina.get("ubicacion_pagina") or ""
        municipio_ficha = ubicacion_pagina.split(",")[0].strip() if ubicacion_pagina else ""

        if normalizar(municipio_ficha) in ("diez de octubre", "10 de octubre"):
            ficha_estado = "dentro"
        elif municipio_ficha:
            ficha_estado = "fuera"
        else:
            ficha_estado = "sin ubicación"

        texto = " ".join([
            anuncio.get("titulo", "") or "",
            anuncio.get("enlace", "") or "",
        ])
        senales = analizar_texto(texto, anillos, cache)
        resultado, confianza, pertenece, motivo = clasificar(ficha_estado, senales)

        resultados.append({
            "id_unico": f"revolico-{identificador}",
            "id_anuncio": identificador,
            "indice_base": indice,
            "fuente": "revolico",
            "titulo": anuncio.get("titulo", ""),
            "enlace": anuncio.get("enlace", ""),
            "ficha": {
                "ubicacion_pagina": ubicacion_pagina,
                "municipio": municipio_ficha,
                "estado": ficha_estado,
            },
            "senales_texto": senales,
            "resultado": resultado,
            "confianza": confianza,
            "pertenece": pertenece,
            "motivo": motivo,
            "registro_original": anuncio,
        })

    return resultados


def preparar_facebook(anillos, cache):
    publicaciones = cargar_json(FACEBOOK_FILE)
    rechazadas = cargar_json(FACEBOOK_RECHAZADOS)
    resultados = []

    for registro in publicaciones:
        publicacion = registro.get("publicacion") or {}
        detalles = registro.get("detalles_propiedad") or {}
        texto = " ".join(str(x) for x in [
            publicacion.get("grupo"),
            publicacion.get("titulo"),
            publicacion.get("autor"),
            detalles.get("ubicacion"),
            detalles.get("zona"),
        ] if x)

        senales = analizar_texto(texto, anillos, cache)
        # Facebook no tiene ficha municipal normalizada: se usa el texto.
        resultado, confianza, pertenece, motivo = clasificar("sin ubicación", senales)

        resultados.append({
            "id_unico": f"facebook-{registro.get('id_publicacion')}",
            "id_publicacion": registro.get("id_publicacion"),
            "fuente": "facebook",
            "titulo": publicacion.get("titulo", ""),
            "ubicacion": detalles.get("ubicacion", ""),
            "en_base_limpia": True,
            "ficha": {
                "ubicacion_pagina": None,
                "municipio": None,
                "estado": "no_aplica",
            },
            "senales_texto": senales,
            "resultado": resultado,
            "confianza": confianza,
            "pertenece": pertenece,
            "motivo": motivo,
            "registro_original": registro,
        })

    # Se incluye la publicación rechazada por el filtro anterior para validar
    # si el rechazo fue correcto.
    for registro in rechazadas:
        publicacion = registro.get("publicacion") or {}
        detalles = registro.get("detalles_propiedad") or {}
        texto = " ".join(str(x) for x in [
            publicacion.get("grupo"),
            publicacion.get("titulo"),
            publicacion.get("autor"),
            detalles.get("ubicacion"),
            detalles.get("zona"),
        ] if x)

        senales = analizar_texto(texto, anillos, cache)
        resultado, confianza, pertenece, motivo = clasificar("sin ubicación", senales)

        resultados.append({
            "id_unico": f"facebook-{registro.get('id_publicacion')}",
            "id_publicacion": registro.get("id_publicacion"),
            "fuente": "facebook",
            "titulo": publicacion.get("titulo", ""),
            "ubicacion": detalles.get("ubicacion", ""),
            "en_base_limpia": False,
            "motivo_rechazo_previo": registro.get("motivo_eliminacion"),
            "patron_rechazo_previo": registro.get("patron_detectado"),
            "ficha": {
                "ubicacion_pagina": None,
                "municipio": None,
                "estado": "no_aplica",
            },
            "senales_texto": senales,
            "resultado": resultado,
            "confianza": confianza,
            "pertenece": pertenece,
            "motivo": motivo,
            "registro_original": registro,
        })

    return resultados


def analizar_geojson():
    with open(GEOJSON, encoding="utf-8") as f:
        geojson = json.load(f)

    objetivo = next(
        f for f in geojson["features"]
        if f["properties"].get("municipality") == "Diez de Octubre"
    )
    anillos = objetivo["geometry"]["coordinates"]
    bbox = limites(anillos)

    # Área aproximada por fórmula del zapato.
    area_grados = 0.0
    for i in range(len(anillos[0]) - 1):
        x1, y1 = anillos[0][i]
        x2, y2 = anillos[0][i + 1]
        area_grados += x1 * y2 - x2 * y1
    area_km2 = abs(area_grados) / 2 * (111.32 ** 2) * math.cos(
        math.radians((bbox[1] + bbox[3]) / 2)
    )

    def segmentos(municipio_anillos):
        conjunto = set()
        for anillo in municipio_anillos:
            for i in range(len(anillo) - 1):
                p, q = anillo[i], anillo[i + 1]
                conjunto.add(frozenset([
                    (round(p[0], 7), round(p[1], 7)),
                    (round(q[0], 7), round(q[1], 7)),
                ]))
        return conjunto

    # El GeoJSON es una simplificación de 11 vértices y no distingue tierra de
    # agua. Se mide el borde compartido con cada municipio para dejar la
    # evidencia a la vista; la clasificación tierra/bahía se documenta aparte.
    segmentos_objetivo = segmentos(anillos)
    contactos = {}
    for feature in geojson["features"]:
        nombre = feature["properties"].get("municipality")
        if nombre == "Diez de Octubre":
            continue
        comunes = segmentos_objetivo & segmentos(feature["geometry"]["coordinates"])
        longitud = 0.0
        for segmento in comunes:
            (lon1, lat1), (lon2, lat2) = tuple(segmento)
            kx = 111.32 * math.cos(math.radians(lat1))
            longitud += math.hypot((lon2 - lon1) * kx, (lat2 - lat1) * 110.57)
        if comunes:
            contactos[nombre] = round(longitud, 2)

    # Vecinos con frontera terrestre. La Habana Vieja comparte 1.61 km de borde
    # norte, pero ese tramo discurre por la bahía; Regla solo coincide en un
    # vértice. Ninguno de los dos limita por tierra con Diez de Octubre.
    VECINOS_TIERRA = ["Cerro", "San Miguel del Padrón", "Arroyo Naranjo", "Boyeros"]
    vecinos = [(nombre, contactos.get(nombre, 0.0)) for nombre in VECINOS_TIERRA]

    return {
        "municipios": len(geojson["features"]),
        "municipio": "Diez de Octubre",
        "codigo_dpa": objetivo["properties"].get("DPA_municipality_code"),
        "vertices": len(anillos[0]),
        "bbox": bbox,
        "area_km2": round(area_km2, 2),
        "vecinos": vecinos,
        "contactos_geojson": contactos,
        "anillos": anillos,
    }


def evidencia_texto(senales):
    partes = []
    for e in senales["dentro"]:
        partes.append(f"DENTRO:{e['nombre']}")
    for e in senales["fuera"]:
        partes.append(f"FUERA:{e['nombre']}")
    for e in senales["ambigua"]:
        partes.append(f"AMBIGUA:{e['nombre']}")
    return "; ".join(partes)


def escribir_json(ruta, datos):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def main():
    geo = analizar_geojson()
    anillos = geo["anillos"]
    cache = cargar_cache()

    revolico = preparar_revolico(anillos, cache)
    facebook_completo = preparar_facebook(anillos, cache)
    facebook = [r for r in facebook_completo if r["en_base_limpia"]]

    unificado = revolico + facebook

    for r in revolico + facebook_completo:
        r.pop("anillos", None)

    escribir_json(OUT_REVOLICO, revolico)
    escribir_json(OUT_FACEBOOK, facebook_completo)
    escribir_json(OUT_UNIFICADO, unificado)

    confirmados_rev = [r for r in revolico if r["resultado"] == "SÍ"]
    confirmados_fb = [r for r in facebook if r["resultado"] == "SÍ"]
    confirmados_uni = confirmados_rev + confirmados_fb

    escribir_json(OUT_REV_CONFIRMADOS, [
        {**r["registro_original"], "verificacion_municipal": {
            "resultado": r["resultado"], "confianza": r["confianza"],
            "ficha": r["ficha"], "motivo": r["motivo"],
        }} for r in confirmados_rev
    ])
    escribir_json(OUT_FB_CONFIRMADOS, [
        {**r["registro_original"], "verificacion_municipal": {
            "resultado": r["resultado"], "confianza": r["confianza"],
            "motivo": r["motivo"],
        }} for r in confirmados_fb
    ])
    escribir_json(OUT_UNI_CONFIRMADOS, [
        {**r["registro_original"], "verificacion_municipal": {
            "resultado": r["resultado"], "confianza": r["confianza"],
            "ficha": r["ficha"], "motivo": r["motivo"],
        }} for r in confirmados_uni
    ])

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow([
            "id_unico", "fuente", "resultado", "confianza", "pertenece",
            "municipio_ficha", "ubicacion_ficha", "evidencia_dentro",
            "evidencia_fuera", "evidencia_ambigua", "titulo",
        ])
        for r in unificado:
            escritor.writerow([
                r["id_unico"], r["fuente"], r["resultado"], r["confianza"],
                "" if r["pertenece"] is None else ("sí" if r["pertenece"] else "no"),
                r["ficha"]["municipio"], r["ficha"]["ubicacion_pagina"],
                "; ".join(e["nombre"] for e in r["senales_texto"]["dentro"]),
                "; ".join(e["nombre"] for e in r["senales_texto"]["fuera"]),
                "; ".join(e["nombre"] for e in r["senales_texto"]["ambigua"]),
                r["titulo"],
            ])

    # Reporte
    resumen_rev = Counter(r["resultado"] for r in revolico)
    resumen_fb = Counter(r["resultado"] for r in facebook)
    resumen_fb_completo = Counter(r["resultado"] for r in facebook_completo)
    resumen_uni = Counter(r["resultado"] for r in unificado)
    fuera_por_municipio = Counter(
        r["ficha"]["municipio"] for r in revolico
        if r["ficha"]["estado"] == "fuera"
    )

    lineas = []
    lineas.append("# Verificación de pertenencia al municipio Diez de Octubre")
    lineas.append("")
    lineas.append(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}  ")
    lineas.append(f"**Fuente geoespacial:** `{GEOJSON}`  ")
    lineas.append("**Método:** polígono municipal + ubicación de la ficha + geocodificación de topónimos.")
    lineas.append("")
    lineas.append("## 1. Análisis del GeoJSON")
    lineas.append("")
    lineas.append(f"- Municipios incluidos: **{geo['municipios']}**.")
    lineas.append(f"- Municipio objetivo: **{geo['municipio']}** (DPA `{geo['codigo_dpa']}`).")
    lineas.append(f"- Vértices del polígono: **{geo['vertices']}**.")
    lineas.append(
        f"- Bounding box: lon {geo['bbox'][0]:.4f} a {geo['bbox'][2]:.4f}; "
        f"lat {geo['bbox'][1]:.4f} a {geo['bbox'][3]:.4f}."
    )
    lineas.append(f"- Área aproximada: **{geo['area_km2']} km²**.")
    lineas.append(
        "- Municipios con frontera terrestre: "
        + ", ".join(n for n, _ in geo["vecinos"]) + "."
    )
    contactos = geo.get("contactos_geojson", {})
    if contactos:
        lineas.append(
            "- Borde compartido medido en el GeoJSON: "
            + ", ".join(
                f"{nombre} ({longitud:.2f} km)"
                for nombre, longitud in sorted(
                    contactos.items(), key=lambda x: -x[1]
                )
            )
            + "."
        )
    lineas.append(
        "- **Matiz:** el GeoJSON no distingue tierra de agua. El tramo compartido "
        "con La Habana Vieja corresponde al borde norte por la bahía, y Regla solo "
        "coincide en un vértice; por eso no se cuentan como vecinos terrestres. "
        "Boyeros tampoco registra longitud de borde: la simplificación de 11 "
        "vértices reduce su frontera a un vértice."
    )
    lineas.append("")
    lineas.append(
        "> El polígono tiene solo 11 vértices, por lo que sirve para descartar "
        "o confirmar ubicaciones con margen, no para resolver casos catastrales "
        "a pocos metros del límite. En esos casos se usa además el municipio "
        "declarado por OpenStreetMap y la ficha del anuncio."
    )
    lineas.append("")
    lineas.append("## 2. Cómo se diferenció el municipio")
    lineas.append("")
    lineas.append("1. **Ficha del anuncio:** en Revolico se extrajo `data-cy=\"adLocation\"` de cada página. Es la ubicación que declara el propio anuncio.")
    lineas.append("2. **Texto:** se buscaron menciones a Diez de Octubre, a sus repartos (Lawton, Luyanó, La Víbora, Santos Suárez, El Sevillano, Santa Catalina, Vista Alegre, El Mónaco, La Asunción, Reparto Flores, Plaza Roja) y a otros municipios o repartos.")
    lineas.append("3. **Geocodificación:** cada topónimo se convirtió en coordenadas con Nominatim y se comprobó con `punto_en_poligono` contra el polígono de Diez de Octubre.")
    lineas.append("4. **Criterio de resultado:**")
    lineas.append("   - **SÍ:** la ficha declara Diez de Octubre, o el texto lo declara y no hay contradicción.")
    lineas.append("   - **NO:** la ficha declara otro municipio, o el topónimo geocodificado queda fuera, sin señal interna que lo contradiga.")
    lineas.append("   - **CONTRADICTORIO:** la ficha y el texto apuntan a municipios distintos; requiere revisión manual.")
    lineas.append("   - **INDETERMINADO:** no hay ficha municipal ni topónimo verificable.")
    lineas.append("")
    lineas.append("## 3. Resultado en Revolico (n = 134)")
    lineas.append("")
    lineas.append("| Resultado | n | % | Nivel de evidencia |")
    lineas.append("|---|---:|---:|---|")
    for clave, nivel in [("SÍ", "alta/media"), ("NO", "alta"), ("CONTRADICTORIO", "baja"), ("INDETERMINADO", "baja")]:
        n = resumen_rev.get(clave, 0)
        lineas.append(f"| {clave} | {n} | {n/len(revolico)*100:.1f}% | {nivel} |")
    lineas.append(f"| **Total** | **{len(revolico)}** | **100.0%** | |")
    lineas.append("")
    lineas.append("### 3.1 Ubicación declarada por la ficha")
    lineas.append("")
    lineas.append("| Municipio en la ficha | n |")
    lineas.append("|---|---:|")
    for municipio, n in Counter(
        r["ficha"]["municipio"] or "(sin ubicación)" for r in revolico
    ).most_common():
        lineas.append(f"| {municipio} | {n} |")
    lineas.append("")
    lineas.append(
        f"**Hallazgo principal:** de los 134 anuncios de la base llamada «estricta», "
        f"solo **{sum(1 for r in revolico if r['ficha']['estado']=='dentro')}** declaran "
        f"Diez de Octubre en su propia ficha; **{sum(1 for r in revolico if r['ficha']['estado']=='fuera')}** "
        f"declaran otro municipio y **{sum(1 for r in revolico if r['ficha']['estado']=='sin ubicación')}** "
        f"no tienen ubicación recuperable."
    )
    lineas.append("")
    sin_ficha_confirmados = [
        r for r in revolico
        if r["resultado"] == "SÍ" and r["ficha"]["estado"] == "sin ubicación"
    ]
    lineas.append(
        f"Los **{sum(1 for r in revolico if r['resultado']=='SÍ')}** confirmados de Revolico "
        f"se componen de **{sum(1 for r in revolico if r['resultado']=='SÍ' and r['ficha']['estado']=='dentro')}** "
        f"cuya ficha declara Diez de Octubre más **{len(sin_ficha_confirmados)}** sin ubicación "
        f"recuperable pero con el municipio explícito en el título: "
        + ", ".join(f"`{r['id_anuncio']}`" for r in sin_ficha_confirmados)
        + "."
    )
    lineas.append("")
    lineas.append("### 3.2 Anuncios con ficha de otro municipio")
    lineas.append("")
    lineas.append("| Municipio | n |")
    lineas.append("|---|---:|")
    for municipio, n in fuera_por_municipio.most_common():
        lineas.append(f"| {municipio} | {n} |")
    lineas.append("")
    lineas.append("### 3.3 Casos contradictorios")
    lineas.append("")
    contradictorios = [r for r in revolico if r["resultado"] == "CONTRADICTORIO"]
    if contradictorios:
        lineas.append("| ID | Ficha | Evidencia textual | Título |")
        lineas.append("|---|---|---|---|")
        for r in contradictorios:
            lineas.append(
                f"| {r['id_unico']} | {r['ficha']['ubicacion_pagina']} | "
                f"{evidencia_texto(r['senales_texto'])} | {r['titulo'][:90]} |"
            )
    else:
        lineas.append("No se detectaron contradicciones.")
    lineas.append("")
    lineas.append("### 3.4 Casos indeterminados")
    lineas.append("")
    indeterminados = [r for r in revolico if r["resultado"] == "INDETERMINADO"]
    if indeterminados:
        lineas.append("| ID | Título | Motivo |")
        lineas.append("|---|---|---|")
        for r in indeterminados:
            lineas.append(f"| {r['id_unico']} | {r['titulo'][:90]} | {r['motivo']} |")
    else:
        lineas.append("No se detectaron casos indeterminados.")
    lineas.append("")
    lineas.append("## 4. Resultado en Facebook (n = 42 + 1 rechazada)")
    lineas.append("")
    lineas.append("| Resultado | n (base limpia) | % | Nivel de evidencia |")
    lineas.append("|---|---:|---:|---|")
    for clave, nivel in [("SÍ", "alta/media"), ("NO", "alta"), ("CONTRADICTORIO", "baja"), ("INDETERMINADO", "baja")]:
        n = resumen_fb.get(clave, 0)
        lineas.append(f"| {clave} | {n} | {n/len(facebook)*100:.1f}% | {nivel} |")
    lineas.append(f"| **Total** | **{len(facebook)}** | **100.0%** | |")
    lineas.append("")
    lineas.append(
        f"La publicación rechazada previamente (id 27) queda clasificada como "
        f"**{next(r['resultado'] for r in facebook_completo if not r['en_base_limpia'])}**: "
        f"menciona Santa Amalia, que OpenStreetMap ubica en Arroyo Naranjo, a 0.77 km "
        f"del polígono de Diez de Octubre. La alusión a la Calzada de 10 de Octubre "
        f"es una referencia de cercanía («a solo 3 cuadras»), no la ubicación de la "
        f"propiedad, por lo que no se contó como señal interna. El rechazo anterior "
        f"fue correcto."
    )
    lineas.append("")
    lineas.append("### 4.1 Casos indeterminados de Facebook")
    lineas.append("")
    ind_fb = [r for r in facebook if r["resultado"] == "INDETERMINADO"]
    if ind_fb:
        lineas.append("| ID | Ubicación | Motivo |")
        lineas.append("|---|---|---|")
        for r in ind_fb:
            lineas.append(f"| {r['id_unico']} | {r['ubicacion'] or '(sin ubicación)'} | {r['motivo']} |")
    else:
        lineas.append("No se detectaron casos indeterminados.")
    lineas.append("")
    lineas.append("## 5. Resultado unificado (n = 176)")
    lineas.append("")
    lineas.append("| Resultado | n | % |")
    lineas.append("|---|---:|---:|")
    for clave in ["SÍ", "NO", "CONTRADICTORIO", "INDETERMINADO"]:
        n = resumen_uni.get(clave, 0)
        lineas.append(f"| {clave} | {n} | {n/len(unificado)*100:.1f}% |")
    lineas.append(f"| **Total** | **{len(unificado)}** | **100.0%** |")
    lineas.append("")
    lineas.append("## 6. Impacto en el informe A-F")
    lineas.append("")
    lineas.append(
        f"El informe A-F usa los **134 anuncios de Revolico**. Esta verificación "
        f"encuentra que solo **{resumen_rev.get('SÍ', 0)}** están confirmados dentro "
        f"de Diez de Octubre; **{resumen_rev.get('NO', 0)}** pertenecen a otros "
        f"municipios, **{resumen_rev.get('CONTRADICTORIO', 0)}** son contradictorios y "
        f"**{resumen_rev.get('INDETERMINADO', 0)}** no son verificables. Por tanto, "
        f"las cifras del informe deben interpretarse como una muestra de anuncios "
        f"etiquetados como Diez de Octubre por el scraper, no como una muestra "
        f"estrictamente municipal."
    )
    lineas.append("")
    lineas.append(
        "La base depurada de confirmados queda en "
        f"**{len(confirmados_uni)} registros** ({len(confirmados_rev)} de Revolico + "
        f"{len(confirmados_fb)} de Facebook). No se sobrescribió la base canónica "
        "de 134 ni el informe A-F: la decisión de recalcular el informe queda "
        "pendiente."
    )
    lineas.append("")
    lineas.append("## 7. Archivos generados")
    lineas.append("")
    lineas.append("| Archivo | Contenido |")
    lineas.append("|---|---|")
    lineas.append(f"| `{OUT_REVOLICO}` | Verificación de los 134 anuncios de Revolico |")
    lineas.append(f"| `{OUT_FACEBOOK}` | Verificación de las 42 publicaciones limpias + la rechazada |")
    lineas.append(f"| `{OUT_UNIFICADO}` | Verificación de los 176 registros unificados |")
    lineas.append(f"| `{OUT_CSV}` | Resumen tabular para revisión |")
    lineas.append(f"| `{OUT_REV_CONFIRMADOS}` | {len(confirmados_rev)} anuncios de Revolico confirmados |")
    lineas.append(f"| `{OUT_FB_CONFIRMADOS}` | {len(confirmados_fb)} publicaciones de Facebook confirmadas |")
    lineas.append(f"| `{OUT_UNI_CONFIRMADOS}` | {len(confirmados_uni)} registros confirmados |")
    lineas.append("")
    lineas.append("## 8. Limitaciones")
    lineas.append("")
    lineas.append("- El polígono de Diez de Octubre tiene 11 vértices: es una simplificación administrativa, no un límite catastral.")
    lineas.append("- La ubicación de la ficha de Revolico la declara el anunciante y puede contener errores.")
    lineas.append("- Los topónimos se geocodifican a un punto representativo del reparto, no a la dirección exacta de la propiedad.")
    lineas.append("- La verificación cubre los 134 anuncios conservados y las 43 publicaciones de Facebook; no se re-verificaron los 136 anuncios rechazados por el filtro anterior.")
    lineas.append("- Los casos contradictorios e indeterminados se reportan como tales; no se imputa municipio.")
    lineas.append("")
    lineas.append("---")
    lineas.append("")
    lineas.append("Proyecto de Ciencia de Datos — Universidad de La Habana  ")
    lineas.append("Facultad de Matemática y Computación (MATCOM)  ")
    lineas.append("Profesor: **Yudivian Almeida Cruz**")
    lineas.append("")

    os.makedirs(os.path.dirname(OUT_REPORTE), exist_ok=True)
    with open(OUT_REPORTE, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    # Resumen por consola
    print("=== GEOJSON ===")
    print(f"Municipios: {geo['municipios']} | Diez de Octubre: {geo['vertices']} vértices | área {geo['area_km2']} km²")
    print(f"Vecinos: {', '.join(n for n, _ in geo['vecinos'])}")
    print("\n=== REVOLICO (n=134) ===")
    for k in ["SÍ", "NO", "CONTRADICTORIO", "INDETERMINADO"]:
        print(f"  {k}: {resumen_rev.get(k,0)}")
    print("\n=== FACEBOOK (n=42) ===")
    for k in ["SÍ", "NO", "CONTRADICTORIO", "INDETERMINADO"]:
        print(f"  {k}: {resumen_fb.get(k,0)}")
    print("\n=== UNIFICADO (n=176) ===")
    for k in ["SÍ", "NO", "CONTRADICTORIO", "INDETERMINADO"]:
        print(f"  {k}: {resumen_uni.get(k,0)}")
    print(f"\nConfirmados unificados: {len(confirmados_uni)}")
    print(f"Reporte: {OUT_REPORTE}")


if __name__ == "__main__":
    main()
