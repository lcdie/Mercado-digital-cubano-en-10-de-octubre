#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera un reporte completo y ordenado de los anuncios limpios de Revolico.

Lee:  datos/brutos/revolico_crudos_limpio.json
Escribe:
  - datos/limpios/anuncios_limpios_listado.txt   (lista legible ordenada)
  - datos/limpios/reporte_tecnico_datos_limpios.txt (reporte técnico completo)
"""

import json
import os
from datetime import datetime
from collections import Counter

INPUT_FILE = "datos/brutos/revolico_crudos_limpio.json"
OUTPUT_LIST = "datos/limpios/anuncios_limpios_listado.txt"
OUTPUT_REPORT = "datos/limpios/reporte_tecnico_datos_limpios.txt"


def cargar_datos():
    with open(INPUT_FILE, encoding="utf-8") as f:
        return json.load(f)


def ordenar_anuncios(anuncios):
    """Ordena por moneda (USD primero), luego por precio descendente, luego por título."""
    def clave(a):
        moneda = a.get("moneda") or ""
        precio = a.get("precio") or 0
        titulo = a.get("titulo", "")
        # USD primero, luego CUP, luego sin moneda
        orden_moneda = 0 if moneda == "USD" else (1 if moneda == "CUP" else 2)
        return (orden_moneda, -precio if precio else 0, titulo.lower())
    return sorted(anuncios, key=clave)


def generar_reporte_tecnico(anuncios):
    total = len(anuncios)
    con_precio = [a for a in anuncios if a.get("precio") is not None]
    sin_precio = [a for a in anuncios if not a.get("precio")]

    precios_usd = [a["precio"] for a in anuncios if a.get("moneda") == "USD" and a.get("precio") is not None]
    precios_cup = [a["precio"] for a in anuncios if a.get("moneda") == "CUP" and a.get("precio") is not None]

    # Estadísticas USD
    if precios_usd:
        promedio_usd = sum(precios_usd) / len(precios_usd)
        mediana_usd = sorted(precios_usd)[len(precios_usd)//2]
        min_usd = min(precios_usd)
        max_usd = max(precios_usd)
    else:
        promedio_usd = mediana_usd = min_usd = max_usd = None

    # Estadísticas CUP
    if precios_cup:
        promedio_cup = sum(precios_cup) / len(precios_cup)
        s_cup = sorted(precios_cup)
        mediana_cup = s_cup[len(s_cup)//2] if len(s_cup)%2==1 else (s_cup[len(s_cup)//2-1] + s_cup[len(s_cup)//2])/2
        min_cup = min(precios_cup)
        max_cup = max(precios_cup)
    else:
        promedio_cup = mediana_cup = min_cup = max_cup = None

    # Municipios
    municipios = Counter(a.get("municipio", "Sin especificar") for a in anuncios)

    # Con/sin precio
    p_con_precio = len(con_precio)
    p_sin_precio = len(sin_precio)

    # Permutas
    con_permuta = sum(1 for a in anuncios if a.get("permuta"))

    # Municipios válidos (Diez de Octubre)
    diez_de_octubre = [a for a in anuncios if a.get("municipio") and ("diez de octubre" in a["municipio"].lower() or "10 de octubre" in a["municipio"].lower())]

    lineas = []
    lineas.append("=" * 80)
    lineas.append("REPORTE TÉCNICO DE DATOS LIMPIOS - MERCADO INMOBILIARIO DIEZ DE OCTUBRE")
    lineas.append("=" * 80)
    lineas.append("")
    lineas.append(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lineas.append(f"Archivo fuente: datos/brutos/revolico_crudos_limpio.json")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("RESUMEN EJECUTIVO")
    lineas.append("-" * 80)
    lineas.append("")
    lineas.append(f"Total de anuncios limpios:           {total}")
    lineas.append(f"Anuncios con precio declarado:       {p_con_precio}")
    lineas.append(f"Anuncios sin precio declarado:       {p_sin_precio}")
    lineas.append(f"Anuncios con permuta:                {con_permuta}")
    lineas.append(f"Anuncios en Diez de Octubre:         {len(diez_de_octubre)}")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("DISTRIBUCIÓN POR MONEDA")
    lineas.append("-" * 80)
    lineas.append("")
    lineas.append(f"USD:  {sum(1 for a in anuncios if a.get('moneda') == 'USD')} anuncios")
    lineas.append(f"CUP:  {sum(1 for a in anuncios if a.get('moneda') == 'CUP')} anuncios")
    lineas.append(f"Sin declarar: {sum(1 for a in anuncios if not a.get('moneda'))} anuncios")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("ESTADÍSTICAS DE PRECIOS (USD)")
    lineas.append("-" * 80)
    lineas.append("")
    if precios_usd:
        lineas.append(f"Cantidad de anuncios con precio en USD: {len(precios_usd)}")
        lineas.append(f"Promedio: ${promedio_usd:,.2f}")
        lineas.append(f"Mediana:  ${mediana_usd:,.2f}")
        lineas.append(f"Mínimo:   ${min_usd:,}")
        lineas.append(f"Máximo:   ${max_usd:,}")
    else:
        lineas.append("No hay anuncios con precio en USD.")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("ESTADÍSTICAS DE PRECIOS (CUP)")
    lineas.append("-" * 80)
    lineas.append("")
    if precios_cup:
        lineas.append(f"Cantidad de anuncios con precio en CUP: {len(precios_cup)}")
        lineas.append(f"Promedio: {promedio_cup:,.2f} CUP")
        lineas.append(f"Mediana:  {mediana_cup:,.2f} CUP")
        lineas.append(f"Mínimo:   {min_cup:,} CUP")
        lineas.append(f"Máximo:   {max_cup:,} CUP")
    else:
        lineas.append("No hay anuncios con precio en CUP.")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("DISTRIBUCIÓN POR MUNICIPIO")
    lineas.append("-" * 80)
    lineas.append("")
    for municipio, count in municipios.most_common():
        lineas.append(f"  {municipio}: {count} anuncios")
    lineas.append("")
    lineas.append("-" * 80)
    lineas.append("ANUNCIOS SIN PRECIO DECLARADO")
    lineas.append("-" * 80)
    lineas.append("")
    if sin_precio:
        for a in sin_precio:
            lineas.append(f"  - {a.get('titulo', 'Sin título')[:80]} | {a.get('enlace', '')}")
    else:
        lineas.append("  Todos los anuncios tienen precio declarado.")
    lineas.append("")
    lineas.append("=" * 80)
    lineas.append("FIN DEL REPORTE TÉCNICO")
    lineas.append("=" * 80)

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    print(f"Reporte técnico guardado en: {OUTPUT_REPORT}")


def generar_listado(anuncios):
    lineas = []
    lineas.append("=" * 90)
    lineas.append("LISTA COMPLETA DE ANUNCIOS LIMPIOS - MERCADO INMOBILIARIO DIEZ DE OCTUBRE")
    lineas.append("=" * 90)
    lineas.append("")
    lineas.append(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lineas.append(f"Total de anuncios: {len(anuncios)}")
    lineas.append("")
    lineas.append("Ordenamiento: Moneda (USD primero) > Precio (mayor a menor) > Título alfabético")
    lineas.append("")
    lineas.append("=" * 90)
    lineas.append("LISTADO DETALLADO")
    lineas.append("=" * 90)
    lineas.append("")

    for i, a in enumerate(anuncios, start=1):
        precio = a.get("precio")
        moneda = a.get("moneda") or "-"
        titulo = a.get("titulo", "Sin título")
        municipio = a.get("municipio", "No especificado")
        enlace = a.get("enlace", "")
        permuta = "SÍ" if a.get("permuta") else "NO"
        estado = a.get("estado", "N/D")
        fecha = a.get("fecha_verificacion", "N/D")

        if precio is not None:
            precio_str = f"{precio:,} {moneda}"
        else:
            precio_str = "Sin precio declarado"

        lineas.append(f"[{i:03d}] {precio_str}")
        lineas.append(f"    Título:       {titulo}")
        lineas.append(f"    Municipio:    {municipio}")
        lineas.append(f"    Permuta:      {permuta}")
        lineas.append(f"    Estado:       {estado}")
        lineas.append(f"    Enlace:       {enlace}")
        if fecha != "N/D":
            lineas.append(f"    Verificado:   {fecha}")
        lineas.append("")
        lineas.append("-" * 90)
        lineas.append("")

    with open(OUTPUT_LIST, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    print(f"Listado guardado en: {OUTPUT_LIST}")


def main():
    os.makedirs("datos/limpios", exist_ok=True)
    with open(INPUT_FILE, encoding="utf-8") as f:
        anuncios = json.load(f)

    print(f"Total de anuncios cargados: {len(anuncios)}")

    anuncios_ordenados = ordenar_anuncios(anuncios)
    generar_listado(anuncios_ordenados)
    generar_reporte_tecnico(anuncios_ordenados)

    print("Proceso completado exitosamente.")


if __name__ == "__main__":
    main()
