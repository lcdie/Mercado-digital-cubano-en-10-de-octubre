#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpieza FINAL de los anuncios del mercado inmobiliario de Diez de Octubre.

Problema que corrige este script
--------------------------------
El campo ``municipio`` que devuelve el scraper no es fiable: todos los anuncios
estudiados aparecen como "Diez de Octubre", incluso cuando el título dice
"Habana Vieja", "Boyeros", "Arroyo Naranjo", "Santa Fe", etc. Por eso el filtro
NO puede confiar en ``municipio``: debe mirar el título y el enlace.

Criterios de filtrado estricto
------------------------------
1. MUNICIPIO: se elimina todo anuncio cuyo título o enlace mencione un
   municipio, reparto o localidad que no pertenezca a Diez de Octubre.
   La exclusión se evalúa ANTES que cualquier otra regla y tiene prioridad
   sobre el campo ``municipio``.
2. PRECIO MÍNIMO: se eliminan anuncios con precio declarado inferior a
   1,000 USD (o su equivalente de 24,000 CUP). Los anuncios sin precio se
   conservan, porque la ausencia de precio es un hallazgo del estudio.

Entrada:
    datos/brutos/revolico_crudos_limpio.json       (270 anuncios)
Salidas:
    datos/brutos/revolico_crudos_limpio_final.json (134 anuncios estrictos)
    datos/limpios/anuncios_eliminados_por_filtro_final.json
"""

import json
import os
import re
from collections import Counter

INPUT_FILE = "datos/brutos/revolico_crudos_limpio.json"
OUTPUT_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
REJECTED_FILE = "datos/limpios/anuncios_eliminados_por_filtro_final.json"

# Municipios, repartos y localidades que NO pertenecen a Diez de Octubre.
# Se comparan en minúsculas contra la suma de título + enlace.
PATRONES_EXCLUIR = [
    # Municipios completos de La Habana
    r"habana vieja",
    r"centro habana",
    r"vedado",
    r"nuevo vedado",
    r"playa\b",
    r"marianao",
    r"boyeros",
    r"arroyo naranjo",
    r"santa fe",
    r"guanabacoa",
    r"san miguel",
    r"alamar",
    r"habana del este",
    r"cotorro",
    r"regla\b",
    r"la lisa",
    r"el cerro",
    r"cerro\b",
    # Repartos y localidades de otros municipios
    r"guanabo",
    r"miramar",
    r"coj[ií]mar",
    r"bauta",
    r"altahabana",
    r"casco hist[oó]rico",
    r"plaza vieja",
    r"municipio plaza",
    r"plaza de la revoluci[oó]n",
    r"jes[uú]s mar[ií]a",
    r"p[aá]rraga",
    r"poey",
    r"r[ií]o cristal",
    r"mulgoba",
    r"santa mar[ií]a del rosario",
    # Balnearios y zonas fuera de La Habana
    r"cayo santa mar",
    r"cayo jibacoa",
    r"cayo guano",
    r"cayo levisa",
    r"varadero",
    r"siboney",
    r"buena vista",
    r"santa amalia",
]

# Zonas válidas de Diez de Octubre. Se usan solo para el diagnóstico del
# filtro, no para decidir la inclusión: un anuncio sin zona explícita sigue
# siendo válido si no menciona otro municipio.
ZONAS_DIEZ_DE_OCTUBRE = [
    "diez de octubre", "10 de octubre", "santos suárez", "santos suarez",
    "la víbora", "la vibora", "lawton", "luyano", "luyanó", "el sevillano",
    "sevillano", "el mónaco", "el monaco", "asunción", "asuncion",
    "santa catalina", "vista alegre", "vía blanca", "via blanca",
    "calzada 10 de octubre", "calzada diez de octubre", "barbacoa",
]


def municipio_excluido(titulo, enlace):
    """Devuelve el patrón que delata otro municipio, o None si no hay match."""
    texto = ((titulo or "") + " " + (enlace or "")).lower()
    for patron in PATRONES_EXCLUIR:
        if re.search(patron, texto, re.IGNORECASE):
            return patron
    return None


def validar_precio(precio, moneda):
    """Devuelve (es_valido, motivo). Los anuncios sin precio son válidos."""
    if precio is None:
        return True, None
    moneda = (moneda or "").upper()
    if moneda == "USD" and precio < 1000:
        return False, "PRECIO_USD_MENOR_A_1000"
    if moneda == "CUP" and precio < 24000:
        return False, "PRECIO_CUP_MENOR_A_1000_USD_EQUIVALENTE"
    return True, None


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        anuncios = json.load(f)

    print(f"Total anuncios en la fuente: {len(anuncios)}")

    conservados = []
    eliminados = []

    for a in anuncios:
        titulo = a.get("titulo", "") or ""
        enlace = a.get("enlace", "") or ""
        precio = a.get("precio")
        moneda = (a.get("moneda") or "").upper()

        # 1) La exclusión municipal manda sobre el campo "municipio".
        patron = municipio_excluido(titulo, enlace)
        if patron:
            eliminados.append({
                **a,
                "motivo_eliminacion": "MUNICIPIO_DISTINTO_A_DIEZ_DE_OCTUBRE",
                "patron_detectado": patron,
            })
            continue

        # 2) Precio mínimo cuando hay precio declarado.
        valido, motivo = validar_precio(precio, moneda)
        if not valido:
            eliminados.append({
                **a,
                "motivo_eliminacion": motivo,
                "patron_detectado": None,
            })
            continue

        conservados.append(a)

    # Diagnóstico
    motivos = Counter(e["motivo_eliminacion"] for e in eliminados)
    con_precio = [a for a in conservados if a.get("precio") is not None]
    sin_precio = [a for a in conservados if a.get("precio") is None]
    usd = [a for a in conservados if str(a.get("moneda", "")).upper() == "USD"]
    cup = [a for a in conservados if str(a.get("moneda", "")).upper() == "CUP"]

    print("\n=== RESULTADO DEL FILTRO ESTRICTO ===")
    print(f"Total fuente:              {len(anuncios)}")
    print(f"Anuncios eliminados:       {len(eliminados)}")
    print(f"Anuncios conservados:      {len(conservados)}")
    print("\nMotivos de eliminación:")
    for motivo, count in motivos.most_common():
        print(f"  {motivo}: {count}")
    print("\nComposición de la base estricta:")
    print(f"  Con precio: {len(con_precio)}")
    print(f"  Sin precio: {len(sin_precio)}")
    print(f"  USD:        {len(usd)}")
    print(f"  CUP:        {len(cup)}")

    # Guardar resultados
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(REJECTED_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(conservados, f, ensure_ascii=False, indent=2)

    with open(REJECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(eliminados, f, ensure_ascii=False, indent=2)

    print(f"\nBase estricta guardada en:  {OUTPUT_FILE}")
    print(f"Eliminados guardados en:    {REJECTED_FILE}")


if __name__ == "__main__":
    main()
