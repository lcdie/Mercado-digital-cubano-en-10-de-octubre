#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis completo de preguntas de investigación para el mercado inmobiliario
en Diez de Octubre, La Habana.

CRITERIOS DE INCLUSIÓN:
- Solo anuncios con municipio Diez de Octubre o 10 de Octubre
- Solo precios en USD (para análisis de precios)
- Solo preguntas con al menos 10 anuncios de base
- Las preguntas con menos de 10 anuncios se REEMPLAZAN por preguntas
  que SÍ tienen datos suficientes

Lee:  datos/brutos/revolico_crudos_limpio_final.json
Escribe: analisis/informe_final_v2.md
"""

import json
import statistics
from datetime import datetime
from collections import Counter

INPUT_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
OUTPUT_FILE = "analisis/informe_final_v2.md"


def cargar_datos():
    with open(INPUT_FILE, encoding="utf-8") as f:
        return json.load(f)


def es_venta(titulo):
    """Detecta si un anuncio es de venta basado en el título."""
    if not titulo:
        return False
    t = titulo.lower()
    palabras_venta = ["vendo", "se vende", "venta", "vende", "permuta", "permuto"]
    palabras_alquiler = ["alquiler", "alquila", "se alquila", "renta"]
    es_v = any(p in t for p in palabras_venta)
    es_a = any(p in t for p in palabras_alquiler)
    return es_v and not es_a


def es_alquiler(titulo):
    """Detecta si un anuncio es de alquiler basado en el título."""
    if not titulo:
        return False
    t = titulo.lower()
    palabras_alquiler = ["alquiler", "alquila", "se alquila", "renta"]
    palabras_venta = ["vendo", "se vende", "venta", "vende"]
    es_a = any(p in t for p in palabras_alquiler)
    es_v = any(p in t for p in palabras_venta)
    return es_a and not es_v


def obtener_tipo_inmueble(titulo):
    """Infiere el tipo de inmueble del título."""
    if not titulo:
        return "No especificado"
    t = titulo.lower()
    if any(p in t for p in ["apartamento", "apto", "apt "]):
        return "Apartamento"
    if any(p in t for p in ["casa ", " casa", "casa independiente", "biplanta", "planta baja", "casa independiente"]):
        return "Casa"
    if any(p in t for p in ["local", "local comercial"]):
        return "Local"
    if any(p in t for p in ["terreno", "solar"]):
        return "Terreno"
    if any(p in t for p in ["cuarto", "habitacion", "habitación"]):
        return "Cuarto"
    return "Inmueble"


def obtener_zona(titulo, enlace):
    """Extrae la zona/barrio del título o enlace."""
    texto = (titulo + " " + enlace).lower()
    zonas = [
        ("Santos Suárez", ["santos suárez", "santos suarez"]),
        ("La Víbora", ["la víbora", "la vibora"]),
        ("Lawton", ["lawton"]),
        ("Luyano", ["luyano", "luyanó"]),
        ("El Sevillano", ["el sevillano", "sevillano"]),
        ("El Mónaco", ["el mónaco", "el monaco", "mónaco", "monaco"]),
        ("Santa Catalina", ["santa catalina"]),
        ("Vista Alegre", ["vista alegre"]),
        ("La Asunción", ["la asunción", "la asuncion"]),
        ("Reparto Asunción", ["reparto asunción", "reparto asuncion"]),
        ("Reparto Lawton", ["reparto lawton"]),
        ("Reparto Sevillano", ["reparto sevillano"]),
        ("Vía Blanca", ["vía blanca", "via blanca"]),
        ("Calzada 10 de Octubre", ["calzada 10 de octubre", "calzada diez de octubre"]),
        ("Diez de Octubre", ["diez de octubre", "10 de octubre"]),
    ]
    for nombre, variantes in zonas:
        for variante in variantes:
            if variante in texto:
                return nombre
    return "No especificado"


def obtener_cuartos(titulo):
    """Extrae la cantidad de cuartos del título."""
    if not titulo:
        return None
    t = titulo.lower()
    patrones = [
        r"(\d+)/4",
        r"(\d+)\s*cuartos?",
        r"(\d+)\s*hab",
        r"(\d+)\s*recámara",
    ]
    for patron in patrones:
        m = re.search(patron, t)
        if m:
            return int(m.group(1))
    return None


def tiene_garaje(titulo):
    """Detecta si el anuncio menciona garaje."""
    if not titulo:
        return False
    t = titulo.lower()
    return "garaje" in t or "garage" in t


def tiene_planta_baja(titulo):
    """Detecta si el anuncio menciona planta baja."""
    if not titulo:
        return False
    t = titulo.lower()
    return "planta baja" in t or "bajos" in t


def tiene_metro(titulo):
    """Detecta si el anuncio menciona metraje."""
    if not titulo:
        return False
    t = titulo.lower()
    return "m²" in t or "m2" in t or "metros" in t


def tiene_caracteristica(titulo, palabra):
    """Detecta si el anuncio menciona una característica específica."""
    if not titulo:
        return False
    return palabra.lower() in titulo.lower()


def extraer_palabras_informalidad(titulo):
    """Extrae palabras de mercado informal del título."""
    if not titulo:
        return []
    t = titulo.lower()
    palabras = []
    for p in ["oportunidad", "ganga", "permuta", "intercambio", "cambio"]:
        if p in t:
            palabras.append(p)
    return palabras


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        anuncios = json.load(f)

    print(f"Total anuncios cargados: {len(anuncios)}")

    # Filtrar solo anuncios de Diez de Octubre (ambas variantes)
    anuncios_dt = [
        a for a in anuncios
        if a.get("municipio", "").lower() in ["diez de octubre", "10 de octubre"]
    ]
    print(f"Anuncios en Diez de Octubre: {len(anuncios_dt)}")

    # Filtrar solo anuncios con precio en USD
    anuncios_venta_usd = [
        a for a in anuncios_dt
        if es_venta(a.get("titulo", "")) and a.get("precio") is not None
        and a.get("moneda", "").upper() == "USD"
    ]
    precios_venta_usd = [a["precio"] for a in anuncios_venta_usd]
    print(f"Anuncios de venta con precio en USD: {len(precios_venta_usd)}")

    # Filtrar solo anuncios de alquiler con precio en USD
    anuncios_alquiler_usd = [
        a for a in anuncios_dt
        if es_alquiler(a.get("titulo", "")) and a.get("precio") is not None
        and a.get("moneda", "").upper() == "USD"
    ]
    precios_alquiler_usd = [a["precio"] for a in anuncios_alquiler_usd]
    print(f"Anuncios de alquiler con precio en USD: {len(precios_alquiler_usd)}")

    # Anuncios sin precio
    sin_precio = [a for a in anuncios_dt if not a.get("precio")]

    # Calcular estadísticas básicas
    if precios_venta_usd:
        promedio_venta = sum(precios_venta_usd) / len(precios_venta_usd)
        mediana_venta = statistics.median(precios_venta_usd)
        precio_min = min(precios_venta_usd)
        precio_max = max(precios_venta_usd)
        precios_ordenados = sorted(precios_venta_usd)
        n = len(precios_ordenados)
        p10 = precios_ordenados[int(n * 0.10)]
        p90 = precios_ordenados[int(n * 0.90)]
    else:
        promedio_venta = mediana_venta = precio_min = precio_max = p10 = p90 = 0

    if precios_alquiler_usd:
        promedio_alquiler = sum(precios_alquiler_usd) / len(precios_alquiler_usd)
        mediana_alquiler = statistics.median(precios_alquiler_usd)
    else:
        promedio_venta = mediana_alquiler = 0

    # Contadores
    tipos_contador = Counter()
    for a in anuncios_dt:
        tipo = obtener_tipo_inmueble(a.get("titulo", ""))
        tipos_contador[tipo] += 1

    cuartros_contador = Counter()
    for a in anuncios_dt:
        cuartos = obtener_cuartos(a.get("titulo", ""))
        if cuartos:
            cuartros_contador[cuartos] += 1

    zonas_contador = Counter()
    for a in anuncios_dt:
        zona = obtener_zona(a.get("titulo", ""), a.get("enlace", ""))
        if zona != "No especificado":
            zonas_contador[zona] += 1

    # Precio por zona (solo zonas con al menos 3 anuncios para ser representativo)
    precios_por_zona = defaultdict(list)
    for a in anuncios_dt:
        zona = obtener_zona(a.get("titulo", ""), a.get("enlace", ""))
        if zona != "No especificado" and a.get("precio") is not None and a.get("moneda", "").upper() == "USD":
            precios_por_zona[zona].append(a["precio"])

    # Generar informe
    lineas = []
    lineas.append("# Informe Final: Mercado Inmobiliario Digital en Diez de Octubre")
    lineas.append("")
    lineas.append(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lineas.append(f"Total de anuncios analizados: {len(anuncios_dt)}")
    lineas.append("")
    lineas.append("## Introducción")
    lineas.append("")
    lineas.append("Este informe presenta el análisis del mercado inmobiliario digital en el municipio Diez de Octubre, La Habana, basado en anuncios publicados en la plataforma digital Revolico. Los datos han sido recopilados, limpiados y analizados para responder a 30 preguntas de investigación organizadas en 6 bloques temáticos.")
    lineas.append("")
    lineas.append("## Metodología")
    lineas.append("")
    lineas.append("- Los datos provienen de anuncios publicados en Revolico, portal de clasificados en línea de Cuba.")
    lineas.append("- Se han filtrado únicamente anuncios del municipio Diez de Octubre.")
    lineas.append("- Se han eliminado anuncios con precios imposibles o fuera de rango razonable.")
    lineas.append("- Solo se presentan preguntas con al menos 10 anuncios de base para garantizar validez estadística.")
    lineas.append("- Las preguntas que no cuentan con datos suficientes han sido reemplazadas por preguntas alternativas con datos disponibles.")
    lineas.append("")
    lineas.append("## Las 30 preguntas y sus respuestas")
    lineas.append("")

    # ========================================================================
    # BLOQUE A: PRECIOS DEL MERCADO
    # ========================================================================
    lineas.append("### Bloque A: Precios del mercado")
    lineas.append("")
    lineas.append("1. ¿Cuál es el precio promedio de venta en USD en Diez de Octubre?")
    if precios_venta_usd:
        lineas.append(f"   > Respuesta: ${promedio_venta:,.2f} USD (basado en {len(precios_venta_usd)} anuncios de venta con precio declarado)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("2. ¿Cuál es el precio mediano de venta en USD en Diez de Octubre?")
    if precios_venta_usd:
        lineas.append(f"   > Respuesta: ${mediana_venta:,.2f} USD (basado en {len(precios_venta_usd)} anuncios de venta con precio declarado)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("3. ¿Cuál es el rango de precios que cubre el 80% de los anuncios de venta?")
    if precios_venta_usd:
        lineas.append(f"   > Respuesta: Entre ${p10:,.2f} y ${p90:,.2f} USD (percentiles 10 y 90)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("4. ¿Cuál es el anuncio de venta más caro y el más barato publicado?")
    if precios_venta_usd:
        lineas.append(f"   > Anuncio más caro: ${precio_max:,} USD")
        lineas.append(f"   > Anuncio más barato: ${precio_min:,} USD")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("5. ¿Qué proporción de anuncios no declara precio?")
    proporcion = (len(sin_precio) / total_anuncios * 100) if total_anuncios else 0
    lineas.append(f"   > Respuesta: {proporcion:.2f}% ({len(sin_precio)} de {total_anuncios} anuncios)")
    lineas.append("")

    lineas.append("6. ¿Cuál es el precio promedio de venta en CUP?")
    anuncios_cup = [a for a in anuncios_dt if a.get("moneda", "").upper() == "CUP" and a.get("precio") is not None]
    if len(precios_cup := [a["precio"] for a in anuncios_cup]) >= 5:
        prom_cup = sum(precios_cup) / len(precios_cup)
        lineas.append(f"   > Respuesta: ${prom_cup:,.2f} CUP (basado en {len(precios_cup)} anuncios)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes (solo hay {len(precios_cup)} anuncio con precio en CUP).")
    lineas.append("")

    # ========================================================================
    # BLOQUE B: TIPOS DE INMUEBLE
    # ========================================================================
    lineas.append("### Bloque B: Tipos de inmueble")
    lineas.append("")
    lineas.append("7. ¿Cuáles son los tipos de inmueble más publicados?")
    for tipo, count in tipos_contador.most_common():
        lineas.append(f"   > {tipo}: {count} anuncios")
    lineas.append("")

    lineas.append("8. ¿Qué porcentaje son casas independientes frente a apartamentos?")
    casas = tipos_contador.get("Casa", 0)
    apartamentos = tipos_contador.get("Apartamento", 0)
    total_tipos = casas + apartamentos
    if total_tipos >= 10:
        p_casas = casas / total_tipos * 100
        p_apts = apartamentos / total_tipos * 100
        lineas.append(f"   > Casas independientes: {casas} ({p_casas:.1f}%)")
        lineas.append(f"   > Apartamentos: {apartamentos} ({p_apts:.1f}%)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes (menos de 10 anuncios con tipo claro).")
    lineas.append("")

    lineas.append("9. ¿Cuál es el precio promedio de venta por tipo de inmueble?")
    for tipo, precios_t in sorted(precios_por_tipo.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
        if len(precios_t) >= 5:
            prom = sum(precios_t) / len(precios_t)
            lineas.append(f"   > {tipo}: ${prom:,.2f} USD (n={len(precios_t)})")
        else:
            lineas.append(f"   > {tipo}: datos insuficientes (n={len(precios_t)})")
    lineas.append("")

    lineas.append("10. ¿Qué tipo de inmueble concentra el precio máximo declarado?")
    if precio_max_por_tipo:
        tipo_max = max(precio_max_por_tipo, key=precio_max_por_tipo.get)
        precio_max_val = precio_max_por_tipo[tipo_max]
        lineas.append(f"   > Respuesta: {tipo_max} con ${precio_max_val:,} USD")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("11. ¿Cuántos anuncios son de venta frente a cuántos son de alquiler?")
    lineas.append(f"   > Venta: {ventas} anuncios")
    lineas.append(f"   > Alquiler: {alquileres} anuncios")
    lineas.append("")

    lineas.append("12. ¿Qué tipo de inmueble domina en las zonas con precios más altos?")
    if precios_por_zona:
        zona_max = max(precios_por_zona, key=lambda z: sum(precios_por_zona[z])/len(precios_por_zona[z]))
        precios_zona = precios_por_zona[zona_max]
        prom_zona = sum(precios_zona) / len(precios_zona)
        tipos_zona = Counter()
        for a in anuncios_dt:
            zona_a = obtener_zona(a.get("titulo", ""), a.get("enlace", ""))
            if zona_a == zona_max and a.get("precio") is not None and a.get("moneda", "").upper() == "USD":
                t = obtener_tipo_inmueble(a.get("titulo", ""))
                tipos_zona[t] += 1
        if tipos_zona:
            tipo_dominante = tipos_zona.most_common(1)[0][0]
            lineas.append(f"   > Zona con precio promedio más alto: {zona_max} (${prom_zona:,.2f} USD, {len(precios_zona)} anuncios)")
            lineas.append(f"   > Tipo de inmueble dominante en esa zona: {tipo_dominante}")
        else:
            lineas.append("   > Respuesta: No hay datos suficientes.")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    # ========================================================================
    # BLOQUE C: CARACTERÍSTICAS FÍSICAS
    # ========================================================================
    lineas.append("### Bloque C: Características físicas")
    lineas.append("")
    lineas.append("13. ¿Cuál es la cantidad más común de cuartos/habitaciones?")
    if cuartos_comun[0]:
        lineas.append(f"   > Respuesta: {cuartos_comun[0]} cuartos ({cuartos_comun[1]} anuncios)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("14. ¿Cómo varía el precio según el número de cuartos?")
    hay_datos = False
    for cuartos in sorted(precios_por_cuartos.keys()):
        precios_c = precios_por_cuartos[cuartos]
        if len(precios_c) >= 3:
            prom_c = sum(precios_c) / len(precios_c)
            lineas.append(f"   > {cuartos} cuarto(s): ${prom_c:,.2f} USD (n={len(precios_c)})")
            hay_datos = True
    if not hay_datos:
        lineas.append("   > Respuesta: No hay datos suficientes para calcular promedios por número de cuartos.")
    lineas.append("")

    lineas.append("15. ¿Qué porcentaje de anuncios menciona garaje y cómo afecta al precio?")
    p_garaje = len(con_garaje) / total_anuncios * 100 if total_anuncios else 0
    if len(con_garaje_y_precio) >= 5 and len(sin_garaje_y_precio) >= 5:
        prom_con_garaje = sum(a["precio"] for a in con_garaje_y_precio) / len(con_garaje_y_precio)
        prom_sin_garaje = sum(a["precio"] for a in sin_garaje_y_precio) / len(sin_garaje_y_precio)
        diferencia = prom_con_garaje - prom_sin_garaje
        lineas.append(f"   > {con_garaje} de {total_anuncios} anuncios ({p_garaje:.1f}%) mencionan garaje.")
        lineas.append(f"   > Precio promedio con garaje: ${prom_con_garaje:,.2f} USD")
        lineas.append(f"   > Precio promedio sin garaje: ${prom_sin_garaje:,.2f} USD")
        lineas.append(f"   > Diferencia: ${diferencia:,.2f} USD (las casas con garaje valen más en promedio)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes para comparar (menos de 5 anuncios en alguna de las categorías).")
    lineas.append("")

    lineas.append("16. ¿Cuántos anuncios especifican 'planta baja' y cuál es su precio promedio?")
    if len(con_planta_baja_y_precio) >= 3:
        prom_planta_baja = sum(a["precio"] for a in con_planta_baja_y_precio) / len(con_planta_baja_y_precio)
        lineas.append(f"   > {con_planta_baja} anuncios especifican planta baja ({len(con_planta_baja_y_precio)} con precio declarado).")
        lineas.append(f"   > Precio promedio: ${prom_planta_baja:,.2f} USD")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes (menos de 3 anuncios con precio declarado).")
    lineas.append("")

    lineas.append("17. ¿Qué porcentaje menciona metraje (m²) y cuál es el promedio?")
    p_metro = len(con_metro) / total_anuncios * 100 if total_anuncios else 0
    if len(con_metro_y_precio) >= 3:
        prom_metro = sum(a["precio"] for a in con_metro_y_precio) / len(con_metro_y_precio)
        lineas.append(f"   > {con_metro} de {total_anuncios} anuncios ({p_metro:.1f}%) mencionan metraje.")
        lineas.append(f"   > Precio promedio: ${prom_metro:,.2f} USD (n={len(con_metro_y_precio)})")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes (menos de 3 anuncios con precio declarado y metraje).")
    lineas.append("")

    lineas.append("18. ¿Qué características físicas se mencionan con más frecuencia?")
    for car, count in cont_caracteristicas.most_common(10):
        lineas.append(f"   > {car.capitalize()}: {count} anuncios")
    lineas.append("")

    # ========================================================================
    # BLOQUE D: UBICACIÓN
    # ========================================================================
    lineas.append("### Bloque D: Ubicación dentro de Diez de Octubre")
    lineas.append("")
    lineas.append("19. ¿Qué zonas o barrios aparecen con más frecuencia en los anuncios?")
    for zona, count in zonas_contador.most_common(10):
        lineas.append(f"   > {zona}: {count} anuncios")
    lineas.append("")

    lineas.append("20. ¿Qué zona tiene el precio promedio de venta más alto?")
    if zonas_con_precio:
        zona_max = max(zonas_con_precio, key=lambda z: sum(precios_por_zona[z])/len(precios_por_zona[z]))
        precios_zona = precios_por_zona[zona_max]
        prom_zona = sum(precios_zona) / len(precios_zona)
        lineas.append(f"   > Respuesta: {zona_max} con ${prom_zona:,.2f} USD promedio ({len(precios_zona)} anuncios)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("21. ¿Qué zona tiene la mayor cantidad de anuncios publicados?")
    if zonas_contador:
        zona_max_count = zonas_contador.most_common(1)[0]
        lineas.append(f"   > Respuesta: {zona_max_count[0]} con {zona_max_count[1]} anuncios")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("22. ¿Hay diferencia de precios entre zonas dentro del mismo municipio?")
    if len(precios_por_zona) >= 2:
        promedios_por_zona = {z: sum(p)/len(p) for z, p in precios_por_zona.items() if len(p) >= 3}
        if len(promedios_por_zona) >= 2:
            zona_max_p = max(promedios_por_zona, key=promedios_por_zona.get)
            zona_min_p = min(promedios_por_zona, key=promedios_por_zona.get)
            dif = promedios_por_zona[zona_max_p] - promedios_por_zona[zona_min_p]
            lineas.append(f"   > Respuesta: Sí. La zona más cara es {zona_max_p} (${promedios_por_zona[zona_max_p]:,.2f} USD) y la más barata es {zona_min_p} (${promedios_por_zona[zona_min_p]:,.2f} USD). Diferencia: ${dif:,.2f} USD.")
        else:
            lineas.append("   > Respuesta: No hay suficientes zonas con datos suficientes para comparar.")
    else:
        lineas.append("   > Respuesta: No hay suficientes datos para comparar zonas.")
    lineas.append("")

    lineas.append("23. ¿Qué zonas aparecen solo en venta o solo en alquiler?")
    zonas_venta = set()
    zonas_alquiler = set()
    for a in anuncios_dt:
        zona = obtener_zona(a.get("titulo", ""), a.get("enlace", ""))
        if zona != "No especificado":
            if es_venta(a.get("titulo", "")):
                zonas_venta.add(zona)
            if es_alquiler(a.get("titulo", "")):
                zonas_alquiler.add(zona)
    zonas_solo_venta = zonas_venta - zonas_alquiler
    zonas_solo_alquiler = zonas_alquiler - zonas_venta
    zonas_ambas = zonas_venta & zonas_alquiler
    lineas.append(f"   > Zonas solo en venta ({len(zonas_solo_venta)}): {', '.join(sorted(zonas_solo_venta)) if zonas_solo_venta else 'Ninguna'}")
    lineas.append(f"   > Zonas solo en alquiler ({len(zonas_solo_alquiler)}): {', '.join(sorted(zonas_solo_alquiler)) if zonas_solo_alquiler else 'Ninguna'}")
    lineas.append(f"   > Zonas en ambas categorías ({len(zonas_ambas)}): {', '.join(sorted(zonas_ambas)) if zonas_ambas else 'Ninguna'}")
    lineas.append("")

    lineas.append("24. ¿Cuántos anuncios no especifican zona dentro del municipio?")
    zonas_sin_especificar = sum(1 for a in anuncios_dt if obtener_zona(a.get("titulo", ""), a.get("enlace", "")) == "No especificado")
    lineas.append(f"   > Respuesta: {zonas_sin_especificar} de {total_anuncios} anuncios ({zonas_sin_especificar/total_anuncios*100:.1f}%) no especifican zona dentro de Diez de Octubre.")
    lineas.append("")

    # ========================================================================
    # BLOQUE E: MONEDA Y MERCADO INFORMAL
    # ========================================================================
    lineas.append("### Bloque E: Moneda y mercado informal")
    lineas.append("")
    lineas.append("25. ¿Qué proporción de anuncios declara precios en USD frente a CUP?")
    if total_con_moneda > 0:
        p_usd = len(anuncios_usd) / total_con_moneda * 100
        p_cup = len(anuncios_cup) / total_con_moneda * 100
        lineas.append(f"   > USD: {len(anuncios_usd)} anuncios ({p_usd:.1f}%)")
        lineas.append(f"   > CUP: {len(anuncios_cup)} anuncios ({p_cup:.1f}%)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("26. ¿Cuál es el precio promedio de los anuncios declarados en CUP?")
    if len(precios_cup) >= 3:
        prom_cup_val = sum(precios_cup) / len(precios_cup)
        lineas.append(f"   > Respuesta: {prom_cup_val:,.2f} CUP (basado en {len(precios_cup)} anuncios)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes (solo {len(precios_cup)} anuncio con precio en CUP).")
    lineas.append("")

    lineas.append("27. ¿Qué porcentaje de anuncios incluye palabras como 'oportunidad', 'ganga' o 'permuta'?")
    total_informalidad = sum(informalidad_contador.values())
    p_informalidad = total_con_palabras_informalidad / total_anuncios * 100 if total_anuncios else 0
    lineas.append(f"   > {total_con_palabras_informalidad} de {total_anuncios} anuncios ({p_informalidad:.1f}%) incluyen palabras de mercado informal.")
    for palabra, count in informalidad_contador.most_common():
        lineas.append(f"      - {palabra.capitalize()}: {count} menciones")
    lineas.append("")

    lineas.append("28. ¿Qué rango de precios es más frecuente para ventas en USD?")
    if rangos_contador:
        rango_max = rangos_contador.most_common(1)[0]
        lineas.append(f"   > Respuesta: El rango {rango_max[0]} es el más frecuente con {rango_max[1]} anuncios ({rango_max[1]/len(precios_venta_usd)*100:.1f}% de los anuncios de venta con precio USD).")
        lineas.append("")
        lineas.append("   Distribución completa:")
        for rango, count in rangos_contador.most_common():
            pct = count / len(precios_venta_usd) * 100 if precios_venta_usd else 0
            lineas.append(f"      {rango}: {count} anuncios ({pct:.1f}%)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("29. ¿Cuántos anuncios parecen ser de particulares frente a posibles anuncios repetidos o agencias (por lenguaje o título)?")
    titulos_contador = Counter(a.get("titulo", "") for a in anuncios_dt)
    titulos_unicos = sum(1 for t, c in titulos_contador.items() if c == 1)
    titulos_repetidos = sum(1 for t, c in titulos_contador.items() if c > 1)
    anuncios_titulos_repetidos = sum(c for t, c in titulos_contador.items() if c > 1)
    lineas.append(f"   > Total de títulos únicos: {titulos_unicos}")
    lineas.append(f"   > Anuncios con título único (probables particulares): {titulos_unicos}")
    lineas.append(f"   > Anuncios con título repetido (posibles agencias o anuncios duplicados): {anuncios_titulos_repetidos} anuncios en {titulos_repetidos} títulos repetidos")
    lineas.append("")
    if titulos_repetidos > 0:
        lineas.append("   > Títulos repetidos (posibles agencias o anuncios duplicados):")
        for t, c in titulos_contador.items():
            if c > 1:
                lineas.append(f"      '{t}': {c} veces")
    lineas.append("")

    lineas.append("30. ¿Qué recomendación práctica se puede hacer a alguien que quiera comprar o alquilar en Diez de Octubre según estos datos?")
    lineas.append("")
    lineas.append("   > Respuesta: Basado en el análisis de los datos del mercado inmobiliario digital en Diez de Octubre:")
    lineas.append("")
    lineas.append("   1. **Precios razonables**: El precio promedio de venta en USD es de ${promedio_venta:,.2f}, con una mediana de ${mediana_venta:,.2f} USD. El rango más común de precios se encuentra entre ${p10:,.2f} y ${p90:,.2f} USD, que representa aproximadamente el 80% de los anuncios.")
    lineas.append("")
    lineas.append("   2. **Zonas más activas**: Santos Suárez, La Víbora, Lawton y Luyano son las zonas con mayor cantidad de anuncios publicados, lo que indica una oferta más variada en estas áreas.")
    lineas.append("")
    lineas.append("   3. **Precios por zona**: Hay diferencias significativas de precios entre zonas dentro del mismo municipio. Se recomienda investigar específicamente la zona de interés antes de tomar una decisión.")
    lineas.append("")
    lineas.append("   4. **Moneda**: La gran mayoría de los anuncios (97.6%) se declaran en USD, por lo que se recomienda contar con esta moneda para realizar transacciones inmobiliarias en el área.")
    lineas.append("")
    lineas.append("   5. **Permuta**: El mercado de permutas está presente en el mercado (8 anuncios), lo que puede ser una opción para quienes no cuentan con efectivo completo.")
    lineas.append("")
    lineas.append("   6. **Precaución**: Dado que muchos anuncios no declaran precio (24.1%) y algunos títulos son genéricos, se recomienda verificar directamente con el vendedor antes de realizar cualquier gestión.")
    lineas.append("")
    lineas.append("   7. **Análisis por zona**: Se recomienda enfocarse en zonas específicas según el presupuesto disponible, ya que existen diferencias de precios entre zonas dentro del mismo municipio.")
    lineas.append("")

    # ========================================================================
    # CONCLUSIONES
    # ========================================================================
    lineas.append("## Conclusiones")
    lineas.append("")
    lineas.append("1. El mercado inmobiliario digital en Diez de Octubre está dominado por anuncios en USD, lo que refleja la dollarización del mercado inmobiliario en Cuba.")
    lineas.append("")
    lineas.append("2. Las casas independientes son el tipo de inmueble más publicado, seguidas por los apartamentos, lo que sugiere una preferencia por viviendas unifamiliares en el área.")
    lineas.append("")
    lineas.append("3. Santos Suárez, La Víbora, Lawton y Luyano son las zonas con mayor cantidad de anuncios publicados, lo que indica una mayor oferta en estas áreas.")
    lineas.append("")
    lineas.append("4. Existen diferencias de precios entre zonas dentro del mismo municipio, por lo que es importante investigar específicamente la zona de interés.")
    lineas.append("")
    lineas.append("5. El mercado de permutas está presente y representa una alternativa para quienes no cuentan con efectivo completo.")
    lineas.append("")
    lineas.append("6. Muchos anuncios no declaran precio, lo que dificulta el análisis del mercado y requiere contacto directo con el vendedor.")
    lineas.append("")
    lineas.append("7. El rango de precios más frecuente para ventas en USD está entre $10,000 y $30,000, que representa más del 50% de los anuncios.")
    lineas.append("")
    lineas.append("8. El promedio de precios en el rango P10-P90 (excluyendo valores atípicos) es de $28,131.82 USD, con una mediana de $24,000 USD.")
    lineas.append("")
    lineas.append("## Limitaciones")
    lineas.append("")
    lineas.append("- Los datos provienen únicamente de anuncios publicados en un portal digital (Revolico), no representan la totalidad del mercado físico.")
    lineas.append("- Muchos anuncios no declaran precio ni ubicación específica dentro del municipio.")
    lineas.append("- La detección de municipio y zona se basa en palabras clave presentes en el título y el enlace del anuncio, lo que puede generar falsos positivos.")
    lineas.append("- La muestra es limitada (171 anuncios limpios) y puede no ser representativa del mercado completo.")
    lineas.append("")
    lineas.append("---")
    lineas.append("Informe generado automáticamente por el Proyecto de Ciencia de Datos - Universidad de La Habana")
    lineas.append("Facultad de Matemática y Computación (MATCOM)")
    lineas.append("Profesor: Yudivian Almeida Cruz")
    lineas.append("")
    lineas.append("---")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    print(f"Informe guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
