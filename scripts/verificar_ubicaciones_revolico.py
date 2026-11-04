#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae la ubicación publicada en cada ficha de Revolico.

El scraper original guardó ``municipio = "Diez de Octubre"`` en todos los
anuncios, pero la ficha de Revolico muestra su propia ubicación en el elemento
``data-cy="adLocation"`` y en el breadcrumb (``municipality=<slug>``). Este
script recupera ese dato para poder verificar la pertenencia municipal.

Entrada:
    datos/brutos/revolico_crudos_limpio_final.json
Salida:
    datos/brutos/revolico_ubicaciones_pagina.json

La salida es reanudable: si ya existe, sólo descarga los anuncios que faltan.
"""

import html
import json
import os
import re
import time
import urllib.request

INPUT_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
OUTPUT_FILE = "datos/brutos/revolico_ubicaciones_pagina.json"
PAUSA = 0.7
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124 Safari/537.36"
)

RE_UBICACION = re.compile(
    r'<p[^>]*data-cy="adLocation"[^>]*>(.*?)</p>', re.S
)
RE_TITULO = re.compile(r"<title[^>]*>(.*?)</title>", re.S)
RE_MUNICIPIO = re.compile(r"municipality=([a-z0-9\-]+)")


def limpiar_html(texto):
    texto = re.sub(r"<[^>]+>", " ", texto or "")
    return re.sub(r"\s+", " ", html.unescape(texto)).strip()


def id_efectivo(anuncio, indice):
    """ID del anuncio o, si falta, el número final de su enlace."""
    if anuncio.get("id_anuncio"):
        return anuncio["id_anuncio"]
    coincidencia = re.search(r"-(\d{5,})(?:\?|$)", anuncio.get("enlace", "") or "")
    if coincidencia:
        return int(coincidencia.group(1))
    return f"sin-id-{indice}"


def descargar(enlace):
    peticion = urllib.request.Request(enlace, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(peticion, timeout=30) as respuesta:
        return respuesta.read().decode("utf-8", errors="replace")


def analizar(enlace):
    try:
        pagina = descargar(enlace)
    except Exception as error:
        return {"error": str(error)}

    ubicacion = RE_UBICACION.search(pagina)
    titulo = RE_TITULO.search(pagina)
    municipios = RE_MUNICIPIO.findall(pagina)

    return {
        "ubicacion_pagina": limpiar_html(ubicacion.group(1)) if ubicacion else "",
        "titulo_pagina": limpiar_html(titulo.group(1)) if titulo else "",
        "municipio_slug": municipios[0] if municipios else "",
    }


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        anuncios = json.load(f)

    resultados = {}
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, encoding="utf-8") as f:
                for item in json.load(f):
                    resultados[str(item["id_anuncio"])] = item
        except (json.JSONDecodeError, ValueError):
            resultados = {}

    pendientes = [
        (indice, a) for indice, a in enumerate(anuncios, start=1)
        if str(id_efectivo(a, indice)) not in resultados
    ]
    print(f"Anuncios: {len(anuncios)} | ya descargados: {len(resultados)} | pendientes: {len(pendientes)}")

    for posicion, (indice_base, anuncio) in enumerate(pendientes, start=1):
        identificador = str(id_efectivo(anuncio, indice_base))
        datos = analizar(anuncio.get("enlace", ""))
        item = {
            "id_anuncio": identificador,
            "indice_base": indice_base,
            "enlace": anuncio.get("enlace", ""),
            "titulo": anuncio.get("titulo", ""),
            **datos,
        }
        resultados[identificador] = item

        if "error" in datos:
            print(f"  [{posicion}/{len(pendientes)}] {identificador} ERROR {datos['error']}")
        else:
            print(
                f"  [{posicion}/{len(pendientes)}] {identificador} "
                f"{datos['ubicacion_pagina'] or '(sin ubicación)'}"
            )

        if posicion % 10 == 0 or posicion == len(pendientes):
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    sorted(resultados.values(), key=lambda x: str(x["id_anuncio"])),
                    f, ensure_ascii=False, indent=2,
                )

        time.sleep(PAUSA)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            sorted(resultados.values(), key=lambda x: str(x["id_anuncio"])),
            f, ensure_ascii=False, indent=2,
        )

    print(f"\nUbicaciones guardadas en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
