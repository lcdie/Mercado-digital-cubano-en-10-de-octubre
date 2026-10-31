#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el informe del Bloque 1 (Precios del mercado) a partir de los datos
brutos ya scrapeados.

Lee:
  - datos/brutos/revolico_crudos.json
  - datos/brutos/elcaiman_crudos.json

Escribe:
  - analisis/bloque1/Bloque_1_Precios_del_mercado.txt

Filtros aplicados:
  - Se excluyen anuncios sospechosos (campo sospechoso == true).
  - Se excluyen anuncios sin precio declarado.
  - Se unifican fuentes Revolico y El Caimán.
"""

import json
import os
import statistics

REVOLICO_FILE = "datos/brutos/revolico_crudos.json"
ELCAIMAN_FILE = "datos/brutos/elcaiman_crudos.json"
OUTPUT_DIR = "analisis/bloque1"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Bloque_1_Precios_del_mercado.txt")

# Cuartiles para el rango que cubre el 80% central (percentiles 10 y 90)


def cargar_datos():
    datos = []
    for ruta in (REVOLICO_FILE, ELCAIMAN_FILE):
        if not os.path.exists(ruta):
            print(f"No se encontró {ruta}, se omite.")
            continue
        with open(ruta, encoding="utf-8") as f:
            datos.extend(json.load(f))
    return datos


def es_venta(titulo):
    if not titulo:
        return False
    t = titulo.lower()
    palabras_venta = ["vendo", "se vende", "venta", "vende"]
    palabras_alquiler = ["alquiler", "alquila", "se alquila", "renta"]
    es_v = any(p in t for p in palabras_venta)
    es_a = any(p in t for p in palabras_alquiler)
    return es_v and not es_a


def es_alquiler(titulo):
    if not titulo:
        return False
    t = titulo.lower()
    palabras_alquiler = ["alquiler", "alquila", "se alquila", "renta"]
    palabras_venta = ["vendo", "se vende", "venta", "vende"]
    es_a = any(p in t for p in palabras_alquiler)
    es_v = any(p in t for p in palabras_venta)
    return es_a and not es_v


def percentil(datos, p):
    if not datos:
        return None
    datos_ordenados = sorted(datos)
    k = (len(datos_ordenados) - 1) * (p / 100.0)
    f = int(k)
    c = f + 1
    if c >= len(datos_ordenados):
        return datos_ordenados[-1]
    d = k - f
    return datos_ordenados[f] + d * (datos_ordenados[c] - datos_ordenados[f])


def formateo_moneda(valor):
    if valor is None:
        return "N/D"
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    datos = cargar_datos()
    print(f"Total anuncios cargados: {len(datos)}")

    # Filtrar sospechosos y sin precio
    limpios = [
        a for a in datos
        if not a.get("sospechoso", False) and a.get("precio") is not None
    ]
    print(f"Anuncios limpios con precio: {len(limpios)}")

    ventas_usd = [
        a["precio"] for a in limpios
        if es_venta(a.get("titulo", "")) and a.get("moneda", "").upper() == "USD"
    ]
    alquileres_usd = [
        a["precio"] for a in limpios
        if es_alquiler(a.get("titulo", "")) and a.get("moneda", "").upper() == "USD"
    ]

    total_anuncios = len(datos)
    sin_precio = len([a for a in datos if a.get("precio") is None])

    lineas = []
    lineas.append("=" * 80)
    lineas.append("BLOQUE 1: PRECIOS DEL MERCADO INMOBILIARIO DIGITAL EN DIEZ DE OCTUBRE, LA HABANA")
    lineas.append("=" * 80)
    lineas.append("")
    lineas.append(f"Fuentes analizadas: Revolico + El Caimán")
    lineas.append(f"Total de anuncios cargados: {total_anuncios}")
    lineas.append(f"Anuncios con precio declarado: {total_anuncios - sin_precio}")
    lineas.append(f"Anuncios sin precio declarado: {sin_precio}")
    lineas.append(f"Anuncios limpios (sin sospechosos) con precio: {len(limpios)}")
    lineas.append("")

    lineas.append("=" * 80)
    lineas.append("RESPUESTAS A LAS PREGUNTAS DEL BLOQUE 1")
    lineas.append("=" * 80)

    if ventas_usd:
        promedio_venta = statistics.mean(ventas_usd)
        mediana_venta = statistics.median(ventas_usd)
        p10 = percentil(ventas_usd, 10)
        p90 = percentil(ventas_usd, 90)
        mas_caro = max(ventas_usd)
        mas_barato = min(ventas_usd)
    else:
        promedio_venta = mediana_venta = p10 = p90 = mas_caro = mas_barato = None

    lineas.append("")
    lineas.append("1. ¿Cuál es el precio promedio de venta en USD en Diez de Octubre?")
    lineas.append(f"   RESPUESTA: {formateo_moneda(promedio_venta)} USD")
    lineas.append(f"   Cálculo basado en: {len(ventas_usd)} anuncios de venta con precio en USD")

    lineas.append("")
    lineas.append("2. ¿Cuál es el precio mediano de alquiler en USD?")
    if alquileres_usd:
        mediana_alquiler = statistics.median(alquileres_usd)
        promedio_alquiler = statistics.mean(alquileres_usd)
        lineas.append(f"   RESPUESTA: {formateo_moneda(mediana_alquiler)} USD")
        lineas.append(f"   Cálculo basado en: {len(alquileres_usd)} anuncios de alquiler con precio en USD")
    else:
        mediana_alquiler = promedio_alquiler = None
        lineas.append("   RESPUESTA: No hay datos suficientes")
        lineas.append("   Cálculo basado en: 0 anuncios de alquiler con precio en USD")

    lineas.append("")
    lineas.append("3. ¿Cuál es el rango de precios que cubre el 80% de los anuncios de venta?")
    if p10 is not None and p90 is not None:
        lineas.append(f"   RESPUESTA: Entre {formateo_moneda(p10)} USD y {formateo_moneda(p90)} USD (percentiles 10 - 90)")
        lineas.append("   Interpretación: El 80% central de los anuncios de venta se encuentra en este rango")
    else:
        lineas.append("   RESPUESTA: No hay datos suficientes")
    lineas.append(f"   Cálculo basado en: {len(ventas_usd)} anuncios de venta con precio en USD")

    lineas.append("")
    lineas.append("4. ¿Cuál es el anuncio de venta más caro y el más barato publicado?")
    if mas_caro is not None and mas_barato is not None:
        lineas.append(f"   ANUNCIO MÁS BARATO: {formateo_moneda(mas_barato)} USD")
        lineas.append(f"   ANUNCIO MÁS CARO: {formateo_moneda(mas_caro)} USD")
    else:
        lineas.append("   No hay datos suficientes")

    lineas.append("")
    lineas.append("5. ¿Qué proporción de anuncios no declara precio?")
    proporcion = (sin_precio / total_anuncios * 100) if total_anuncios else 0
    lineas.append(f"   RESPUESTA: {proporcion:.2f}% ({sin_precio} de {total_anuncios} anuncios)")

    lineas.append("")
    lineas.append("6. ¿Existe diferencia significativa entre el precio promedio de venta y el de alquiler?")
    if promedio_venta is not None and promedio_alquiler is not None:
        lineas.append("   RESPUESTA: Sí, existe una diferencia considerable.")
        lineas.append("")
        lineas.append("   COMPARATIVA:")
        lineas.append(f"     Venta - Promedio: {formateo_moneda(promedio_venta)} USD (n={len(ventas_usd)})")
        lineas.append(f"     Venta - Mediana:  {formateo_moneda(mediana_venta)} USD (n={len(ventas_usd)})")
        lineas.append(f"     Alquiler - Promedio: {formateo_moneda(promedio_alquiler)} USD (n={len(alquileres_usd)})")
        lineas.append(f"     Alquiler - Mediana:  {formateo_moneda(mediana_alquiler)} USD (n={len(alquileres_usd)})")
    else:
        lineas.append("   RESPUESTA: No hay datos suficientes para comparar")

    lineas.append("")
    lineas.append("=" * 80)
    lineas.append("METODOLOGÍA")
    lineas.append("=" * 80)
    lineas.append("")
    lineas.append("Herramientas utilizadas (disponibles en el repositorio):")
    lineas.append("  - src/scrape_revolico.py: Scraping de Revolico")
    lineas.append("  - src/scrape_elcaiman.py: Scraping de El Caimán")
    lineas.append("  - scripts/agregar_permuta.py: Detección de permutas")
    lineas.append("  - analisis/generar_informe_bloque1.py: Generación de este informe")
    lineas.append("")
    lineas.append("Criterios:")
    lineas.append("  - Tipos (venta/alquiler) inferidos del título usando palabras clave")
    lineas.append("  - Precios normalizados a números, moneda preservada (USD/CUP)")
    lineas.append("  - Campo 'sospechoso' para descartar outliers (precios <100 o >1,000,000)")
    lineas.append("  - Municipio forzado a 'Diez de Octubre' según filtro de la URL de búsqueda")
    lineas.append("  - Promedios y medianas calculados sobre anuncios limpios (sin sospechosos)")
    lineas.append("")
    lineas.append("Generado por: analisis/generar_informe_bloque1.py")
    lineas.append("Repositorio: https://github.com/lcdie/Mercado-digital-cubano-en-10-de-octubre")
    lineas.append("=" * 80)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    print(f"Informe guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
