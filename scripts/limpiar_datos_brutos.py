#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpieza de datos brutos de Revolico.
Elimina anuncios con anomalías graves que invalidan el análisis.

Criterios de eliminación:
1. No son anuncios inmobiliarios (botón publicar, puertas, hoteles, piscinas, pasadías)
2. Precios imposiblemente bajos (< 100 USD)
3. Precios imposiblemente altos (> 1,000,000 USD)
4. Municipio incorrecto (no es Diez de Octubre)
5. Títulos que son solo precios (sin descripción del inmueble)
6. Duplicados exactos (misma URL o mismo título+precio)
"""

import json
import re
import os
from datetime import datetime

INPUT_FILE = "datos/brutos/revolico_crudos_actualizados.json"
OUTPUT_FILE = "datos/brutos/revolico_crudos_limpio.json"

# Patrones de basura no inmobiliaria
PATRONES_BASURA = [
    r"publicar anuncio",
    r"puertas blindadas",
    r"puerta para exterior",
    r"hoteles todo incluido",
    r"varadero",
    r"jibacoa",
    r"cayo santa mar",
    r"piscina",
    r"jacuzzi",
    r"pasad[aí]a",
    r"pasadi",
    r"item/publish",
]

# Umbrales de precio (en USD)
PRECIO_MINIMO = 100
PRECIO_MAXIMO = 1_000_000

# Municipios válidos (solo Diez de Octubre y sus variantes)
MUNICIPIOS_VALIDOS = ["diez de octubre", "10 de octubre"]


def es_titulo_solo_precio(titulo):
    """Detecta si el título es solo un precio sin descripción del inmueble."""
    if not titulo:
        return True
    # Quitar moneda, números, comas, puntos, símbolos, espacios, emojis comunes
    limpio = re.sub(r"[\d.,\s\$€£¥usdcup]+", "", titulo, flags=re.IGNORECASE)
    limpio = re.sub(r"[💥🔴🏠🏡🔑🛑✨🏘️🏢🏤🏥🏦🏨🏩🏪🏫🏬🏭🏯🏰💒🏠🏡🏢🏤🏥🏦🏨🏩🏪🏫🏬🏭🏯🏰💒]+", "", limpio)
    limpio = limpio.strip()
    return len(limpio) == 0


def es_municipio_valido(municipio):
    if not municipio:
        return False
    m = municipio.lower().strip()
    return any(v in m for v in MUNICIPIOS_VALIDOS)


def es_anuncio_basura(titulo, enlace):
    """Detecta anuncios que no son inmuebles residenciales válidos."""
    texto = (titulo + " " + (enlace or "")).lower()
    for patron in PATRONES_BASURA:
        if re.search(patron, texto, re.IGNORECASE):
            return True
    return False


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        anuncios = json.load(f)

    print(f"Total anuncios originales: {len(anuncios)}")

    eliminados = []
    limpios = []
    enlaces_vistos = set()

    for anuncio in anuncios:
        titulo = anuncio.get("titulo", "") or ""
        enlace = anuncio.get("enlace", "") or ""
        precio = anuncio.get("precio")
        moneda = (anuncio.get("moneda") or "").upper()
        municipio = anuncio.get("municipio", "") or ""

        motivo = None

        # 1. No es anuncio inmobiliario
        if es_anuncio_basura(titulo, enlace):
            motivo = "NO ES ANUNCIO INMOBILIARIO"

        # 2. Precio muy bajo (< 100 USD)
        if moneda == "USD" and precio is not None and precio < PRECIO_MINIMO:
            motivo = "PRECIO IMPOSIBLEMENTE BAJO"

        # 3. Precio muy alto (> 1,000,000 USD)
        if moneda == "USD" and precio is not None and precio > PRECIO_MAXIMO:
            motivo = "PRECIO IMPOSIBLEMENTE ALTO"

        # 4. Municipio incorrecto
        if not es_municipio_valido(municipio):
            motivo = "MUNICIPIO INCORRECTO"

        # 5. Título solo precio
        if es_titulo_solo_precio(titulo):
            motivo = "TÍTULO ES SOLO PRECIO"

        # 6. Duplicado por enlace
        if enlace and enlace in enlaces_vistos:
            motivo = "DUPLICADO (enlace repetido)"
        elif enlace:
            enlaces_vistos.add(enlace)

        # 7. Duplicado por título + precio (si no se detectó por enlace)
        clave_titulo = (titulo.strip().lower(), precio, moneda)
        # Revisar duplicados por título+precio entre los ya aceptados
        for existente in limpios:
            if (existente.get("titulo", "").strip().lower() == clave_titulo[0] and
                    existente.get("precio") == clave_titulo[1] and
                    existente.get("moneda") == clave_titulo[2]):
                motivo = "DUPLICADO (título + precio repetido)"
                break

        if motivo:
            motivo_full = f"{motivo} | Título: {titulo[:60]} | Precio: {precio} {moneda} | Municipio: {municipio}"
            eliminados.append({
                "titulo": titulo,
                "precio": precio,
                "moneda": moneda,
                "municipio": municipio,
                "enlace": enlace,
                "motivo": motivo_full
            })
        else:
            limpios.append(anuncio)

    print(f"\nAnuncios eliminados: {len(eliminados)}")
    print(f"Anuncios limpios: {len(limpios)}")

    # Mostrar resumen de eliminados por motivo
    from collections import Counter
    motivos = Counter()
    for e in eliminados:
        motivo = e["motivo"].split(" | ")[0]
        motivos[motivo] += 1
    print("\nMotivos de eliminación:")
    for m, c in motivos.most_common():
        print(f"  {m}: {c}")

    # Guardar archivo limpio
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(limpios, f, ensure_ascii=False, indent=2)

    # Guardar lista de eliminados para auditoría
    elim_file = "datos/limpios/anuncios_eliminados_por_sospecha.json"
    os.makedirs(os.path.dirname(elim_file), exist_ok=True)
    with open(elim_file, "w", encoding="utf-8") as f:
        json.dump(eliminados, f, ensure_ascii=False, indent=2)

    print(f"\nArchivo limpio guardado: {OUTPUT_FILE}")
    print(f"Archivo de eliminados guardado: {elim_file}")


if __name__ == "__main__":
    main()
