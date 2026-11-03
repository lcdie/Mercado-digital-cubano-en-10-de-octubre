#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis de precios con filtros de percentil 10-90 y eliminación de outliers extremos.

Lee:  datos/brutos/revolico_crudos_limpio_final.json
Escribe: datos/limpios/reporte_analisis_precios_rango_p10_p90.txt
"""

import json
import statistics
from datetime import datetime
from collections import Counter

INPUT_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
OUTPUT_FILE = "datos/limpios/reporte_analisis_precios_rango_p10_p90.txt"


def percentil(datos, p):
    """Calcula el percentil p usando interpolación lineal."""
    datos_ord = sorted(datos)
    n = len(datos_ord)
    k = (n - 1) * (p / 100)
    f = int(k)
    c = f + 1
    if c >= n:
        return datos_ord[f]
    d = k - f
    return datos_ord[f] + d * (datos_ord[c] - datos_ord[f])


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        anuncios = json.load(f)

    # Filtrar solo anuncios con precio en USD
    anuncios_con_precio = []
    for a in anuncios:
        precio = a.get("precio")
        moneda = (a.get("moneda") or "").upper()
        if precio is not None and moneda == "USD":
            anuncios_con_precio.append(a)

    print(f"Total anuncios con precio en USD: {len(anuncios_con_precio)}")

    precios = [a["precio"] for a in anuncios_con_precio]

    # Eliminar precios > 100,000,000
    precios_filtrados = [p for p in precios if p <= 100_000_000]
    print(f"Después de eliminar > 100,000,000 USD: {len(precios_filtrados)}")

    # Calcular percentiles
    p10 = percentil(precios_filtrados, 10)
    p90 = percentil(precios_filtrados, 90)

    # Filtrar solo el rango P10-P90
    precios_rango = [p for p in precios_filtrados if p10 <= p <= p90]

    # Calcular estadísticas
    promedio_rango = sum(precios_rango) / len(precios_rango)
    mediana_rango = statistics.median(precios_rango)
    desviacion_rango = statistics.stdev(precios_rango) if len(precios_rango) > 1 else 0
    min_rango = min(precios_rango)
    max_rango = max(precios_rango)

    # Contadores
    eliminados_bajo = len([p for p in precios_filtrados if p < p10])
    eliminados_alto = len([p for p in precios_filtrados if p > p90])
    eliminados_100m = len([p for p in precios if p > 100_000_000])

    # Generar reporte
    lineas = []
    lineas.append("=" * 80)
    lineas.append("REPORTE DE ANÁLISIS DE PRECIOS - RANGO P10-P90 (PERCENTIL 10-90)")
    lineas.append("=" * 80)
    lineas.append("")
    lineas.append(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lineas.append(f"Archivo fuente: datos/brutos/revolico_crudos_limpio_final.json")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("PASO 1: DATOS ORIGINALES")
    lineas.append("-" * 80)
    lineas.append("")
    lineas.append(f"Total anuncios con precio en USD: {len(precios)}")
    lineas.append(f"Precio mínimo original: ${min(precios):,}")
    lineas.append(f"Precio máximo original: ${max(precios):,}")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("PASO 2: ELIMINACIÓN DE PRECIOS > 100,000,000 USD")
    lineas.append("-" * 80)
    lineas.append("")
    lineas.append(f"Anuncios eliminados por precio > 100,000,000 USD: {eliminados_100m}")
    lineas.append(f"Anuncios restantes: {len(precios_filtrados)}")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("PASO 3: CÁLCULO DE PERCENTILES P10 Y P90")
    lineas.append("-" * 80)
    lineas.append("")
    lineas.append(f"Percentil 10 (P10): ${p10:,.2f}")
    lineas.append(f"Percentil 90 (P90): ${p90:,.2f}")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("PASO 4: FILTRADO POR RANGO P10-P90")
    lineas.append("-" * 80)
    lineas.append("")
    lineas.append(f"Anuncios eliminados por debajo de P10 (${p10:,.2f}): {eliminados_bajo}")
    lineas.append(f"Anuncios eliminados por encima de P90 (${p90:,.2f}): {eliminados_alto}")
    lineas.append(f"Anuncios retenidos en rango P10-P90: {len(precios_rango)}")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("PASO 5: ESTADÍSTICAS DEL RANGO P10-P90")
    lineas.append("-" * 80)
    lineas.append("")
    lineas.append(f"Promedio en rango P10-P90: ${promedio_rango:,.2f}")
    lineas.append(f"Mediana en rango P10-P90: ${mediana_rango:,.2f}")
    lineas.append(f"Desviación estándar: ${desviacion_rango:,.2f}")
    lineas.append(f"Mínimo en rango: ${min_rango:,}")
    lineas.append(f"Máximo en rango: ${max_rango:,}")
    lineas.append("")
    lineas.append("=" * 80)
    lineas.append("RESUMEN EJECUTIVO")
    lineas.append("=" * 80)
    lineas.append("")
    lineas.append(f"Total anuncios con precio USD original: {len(precios)}")
    lineas.append(f"Anuncios eliminados por precio > 100,000,000 USD: {eliminados_100m}")
    lineas.append(f"Anuncios eliminados por debajo de P10: {eliminados_bajo}")
    lineas.append(f"Anuncios eliminados por encima de P90: {eliminados_alto}")
    lineas.append(f"Anuncios utilizados para el promedio final: {len(precios_rango)}")
    lineas.append("")
    lineas.append(f"PRECIO PROMEDIO EN RANGO P10-P90: ${promedio_rango:,.2f}")
    lineas.append(f"PRECIO MEDIANA EN RANGO P10-P90: ${mediana_rango:,.2f}")
    lineas.append("")
    lineas.append("=" * 80)
    lineas.append("DISTRIBUCIÓN DE PRECIOS EN EL RANGO P10-P90")
    lineas.append("=" * 80)
    lineas.append("")

    # Agrupar por rangos de 10,000
    rangos = [
        (0, 10000, "0 - 10,000"),
        (10000, 20000, "10,000 - 20,000"),
        (20000, 30000, "20,000 - 30,000"),
        (30000, 40000, "30,000 - 40,000"),
        (40000, 50000, "40,000 - 50,000"),
        (50000, 60000, "50,000 - 60,000"),
        (60000, 70000, "60,000 - 70,000"),
        (70000, 80000, "70,000 - 80,000"),
        (80000, 90000, "80,000 - 90,000"),
        (90000, 1000000, "90,000+"),
    ]

    for min_r, max_r, etiqueta in rangos:
        cuenta = sum(1 for p in precios_rango if min_r <= p < max_r)
        porcentaje = (cuenta / len(precios_rango) * 100) if precios_rango else 0
        bar = "█" * int(porcentaje / 2)
        lineas.append(f"  {etiqueta:15s}: {cuenta:3d} anuncios ({porcentaje:5.1f}%) {bar}")

    lineas.append("")
    lineas.append("=" * 80)
    lineas.append("NOTAS Y LIMITACIONES")
    lineas.append("=" * 80)
    lineas.append("")
    lineas.append("1. Se eliminaron anuncios con precio > 100,000,000 USD como valores atípicos extremos.")
    lineas.append("2. Se calcularon percentiles P10 y P90 sobre los datos restantes.")
    lineas.append(f"3. Se eliminaron {eliminados_bajo} anuncios por debajo de P10 (${p10:,.2f}).")
    lineas.append(f"4. Se eliminaron {eliminados_alto} anuncios por encima de P90 (${p90:,.2f}).")
    lineas.append("5. El promedio se calculó únicamente sobre los anuncios dentro del rango P10-P90.")
    lineas.append("6. Este enfoque reduce el impacto de valores atípicos tanto bajos como altos.")
    lineas.append("")
    lineas.append("=" * 80)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    print(f"\n{'=' * 80}")
    print("REPORTE GUARDADO EN:", OUTPUT_FILE)
    print(f"{'=' * 80}")
    print(f"\nResumen:")
    print(f"  Total anuncios con precio USD: {len(precios)}")
    print(f"  Eliminados > 100,000,000 USD: {eliminados_100m}")
    lineas_f = f"  Eliminados por debajo de P10 (${p10:,.2f}): {eliminados_bajo}"
    print(f"  Eliminados por encima de P90 (${p90:,.2f}): {eliminados_alto}")
    print(f"  Anuncios en rango P10-P90: {len(precios_rango)}")
    print(f"  Promedio en rango P10-P90: ${promedio_rango:,.2f}")
    print(f"  Mediana en rango P10-P90: ${mediana_rango:,.2f}")


if __name__ == "__main__":
    main()
