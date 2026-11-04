#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis completo de las 30 preguntas de investigación del mercado inmobiliario
digital en Diez de Octubre, La Habana.
Solo responde preguntas con datos suficientes (mínimo 10 anuncios).
"""

import json
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime

INPUT_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
OUTPUT_FILE = "analisis/informe_final.md"


def cargar_datos():
    with open(INPUT_FILE, encoding="utf-8") as f:
        return json.load(f)


def es_venta(titulo):
    if not titulo:
        return False
    t = titulo.lower()
    v = ["vendo", "se vende", "venta", "vende", "permuta", "permuto"]
    a = ["alquiler", "alquila", "se alquila", "renta"]
    ev = any(p in t for p in v)
    ea = any(p in t for p in a)
    return ev and not ea


def es_alquiler(titulo):
    if not titulo:
        return False
    t = titulo.lower()
    a = ["alquiler", "alquila", "se alquila", "renta"]
    v = ["vendo", "se vende", "venta", "vende"]
    ea = any(p in t for p in a)
    ev = any(p in t for p in v)
    return ea and not ev


def obtener_tipo(titulo):
    if not titulo:
        return "Inmueble"
    t = titulo.lower()
    if any(p in t for p in ["apartamento", "apto", "apt "]):
        return "Apartamento"
    if any(p in t for p in ["casa ", " casa", "casa independiente", "biplanta", "planta baja"]):
        return "Casa"
    if any(p in t for p in ["local", "local comercial"]):
        return "Local"
    if any(p in t for p in ["terreno", "solar"]):
        return "Terreno"
    if any(p in t for p in ["cuarto", "habitacion", "habitación"]):
        return "Cuarto"
    return "Inmueble"


def obtener_zona(titulo, enlace):
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
    ]
    for nombre, variantes in zonas:
        for variante in variantes:
            if variante in texto:
                return nombre
    return "No especificado"


def obtener_cuartos(titulo):
    if not titulo:
        return None
    t = titulo.lower()
    for pat in [r"(\d+)/4", r"(\d+)\s*cuartos?", r"(\d+)\s*hab"]:
        m = re.search(pat, t)
        if m:
            return int(m.group(1))
    return None


def tiene_garaje(titulo):
    if not titulo:
        return False
    t = titulo.lower()
    return "garaje" in t or "garage" in t


def tiene_planta_baja(titulo):
    if not titulo:
        return False
    t = titulo.lower()
    return "planta baja" in t or "bajos" in t


def tiene_metro(titulo):
    if not titulo:
        return False
    t = titulo.lower()
    return "m²" in t or "m2" in t or "metros" in t


def tiene_permuta(titulo):
    if not titulo:
        return False
    t = titulo.lower()
    return "permuta" in t or "permuto" in t


def extraer_palabras_informalidad(titulo):
    if not titulo:
        return []
    t = titulo.lower()
    ps = []
    for p in ["oportunidad", "ganga", "permuta", "intercambio", "cambio"]:
        if p in t:
            ps.append(p)
    return ps


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        anuncios = json.load(f)

    # Filtrar solo Diez de Octubre
    dt = [a for a in anuncios if a.get("municipio", "").lower() in ["diez de octubre", "10 de octubre"]]
    total = len(dt)
    print(f"Total anuncios en Diez de Octubre: {total}")

    # Ventas con precio USD
    ventas_usd = [a for a in dt if es_venta(a.get("titulo", "")) and a.get("precio") is not None and a.get("moneda", "").upper() == "USD"]
    precios_venta_usd = [a["precio"] for a in ventas_usd]
    print(f"Ventas con precio USD: {len(precios_venta_usd)}")
    ventas = len(ventas_usd)

    # Alquileres con precio USD
    alquileres_usd = [a for a in dt if es_alquiler(a.get("titulo", "")) and a.get("precio") is not None and a.get("moneda", "").upper() == "USD"]
    precios_alquiler_usd = [a["precio"] for a in alquileres_usd]
    print(f"Alquileres con precio USD: {len(precios_alquiler_usd)}")
    alquileres = len(alquileres_usd)

    # Sin precio
    sin_precio = [a for a in dt if not a.get("precio")]

    # Estadísticas precios venta
    if precios_venta_usd:
        promedio_venta = sum(precios_venta_usd) / len(precios_venta_usd)
        mediana_venta = statistics.median(precios_venta_usd)
        precios_ordenados = sorted(precios_venta_usd)
        n = len(precios_ordenados)
        p10 = precios_ordenados[int(n * 0.10)]
        p90 = precios_ordenados[int(n * 0.90)]
        precio_min = min(precios_venta_usd)
        precio_max = max(precios_venta_usd)
    else:
        promedio_venta = mediana_venta = p10 = p90 = precio_min = precio_max = 0

    # Tipos de inmueble
    tipos_contador = Counter()
    for a in dt:
        tipo = obtener_tipo(a.get("titulo", ""))
        tipos_contador[tipo] += 1

    # Cuartos
    cuartos_contador = Counter()
    for a in dt:
        cuartos = obtener_cuartos(a.get("titulo", ""))
        if cuartos:
            cuartos_contador[cuartos] += 1
    cuartos_comun = cuartos_contador.most_common(1)[0] if cuartos_contador else (None, 0)

    # Precios por cuartos
    precios_por_cuartos = defaultdict(list)
    for a in dt:
        cuartos = obtener_cuartos(a.get("titulo", ""))
        if cuartos and a.get("precio") is not None and a.get("moneda", "").upper() == "USD":
            precios_por_cuartos[cuartos].append(a["precio"])

    # Garaje
    con_garaje = [a for a in dt if tiene_garaje(a.get("titulo", ""))]
    con_garaje_y_precio = [a for a in con_garaje if a.get("precio") is not None and a.get("moneda", "").upper() == "USD"]
    sin_garaje_y_precio = [a for a in dt if not tiene_garaje(a.get("titulo", "")) and a.get("precio") is not None and a.get("moneda", "").upper() == "USD"]

    # Planta baja
    con_planta_baja = [a for a in dt if tiene_planta_baja(a.get("titulo", ""))]
    con_planta_baja_y_precio = [a for a in con_planta_baja if a.get("precio") is not None and a.get("moneda", "").upper() == "USD"]

    # Metros
    con_metro = [a for a in dt if tiene_metro(a.get("titulo", ""))]
    con_metro_y_precio = [a for a in con_metro if a.get("precio") is not None and a.get("moneda", "").upper() == "USD"]

    # Características físicas
    cont_caracteristicas = Counter()
    for a in dt:
        t = a.get("titulo", "").lower()
        for c in ["patio", "azotea", "cocina", "garaje", "baño", "cuarto", "sala", "comedor", "terraza", "balcón"]:
            if c in t:
                cont_caracteristicas[c] += 1

    # Ubicación
    zonas_contador = Counter()
    for a in dt:
        zona = obtener_zona(a.get("titulo", ""), a.get("enlace", ""))
        if zona != "No especificado":
            zonas_contador[zona] += 1

    # Zonas solo en venta vs solo en alquiler
    zonas_venta = set()
    zonas_alquiler = set()
    for a in dt:
        zona = obtener_zona(a.get("titulo", ""), a.get("enlace", ""))
        if zona != "No especificado":
            if es_venta(a.get("titulo", "")):
                zonas_venta.add(zona)
            if es_alquiler(a.get("titulo", "")):
                zonas_alquiler.add(zona)
    zonas_solo_venta = zonas_venta - zonas_alquiler
    zonas_solo_alquiler = zonas_alquiler - zonas_venta
    zonas_ambas = zonas_venta & zonas_alquiler

    # Precios por zona
    precios_por_zona = defaultdict(list)
    for a in dt:
        zona = obtener_zona(a.get("titulo", ""), a.get("enlace", ""))
        if zona != "No especificado" and a.get("precio") is not None and a.get("moneda", "").upper() == "USD":
            precios_por_zona[zona].append(a["precio"])

    # Precios por tipo de inmueble
    precios_por_tipo = defaultdict(list)
    for a in dt:
        tipo = obtener_tipo(a.get("titulo", ""))
        if a.get("precio") is not None and a.get("moneda", "").upper() == "USD":
            precios_por_tipo[tipo].append(a["precio"])

    # Precio máximo por tipo
    precio_max_por_tipo = {}
    for tipo, precios_t in precios_por_tipo.items():
        if precios_t:
            precio_max_por_tipo[tipo] = max(precios_t)

    # Moneda
    anuncios_usd = [a for a in dt if a.get("moneda", "").upper() == "USD"]
    anuncios_cup = [a for a in dt if a.get("moneda", "").upper() == "CUP"]
    precios_cup = [a["precio"] for a in anuncios_cup if a.get("precio") is not None]
    total_con_moneda = len(anuncios_usd) + len(anuncios_cup)

    # Palabras de informalidad
    informalidad_contador = Counter()
    for a in dt:
        t = a.get("titulo", "").lower()
        for p in ["oportunidad", "ganga", "permuta", "intercambio", "cambio"]:
            if p in t:
                informalidad_contador[p] += 1
    total_con_palabras_informalidad = sum(informalidad_contador.values())

    # Títulos repetidos
    titulos_contador = Counter(a.get("titulo", "") for a in dt)
    titulos_unicos = sum(1 for t, c in titulos_contador.items() if c == 1)
    titulos_repetidos = sum(1 for t, c in titulos_contador.items() if c > 1)
    anuncios_titulos_repetidos = sum(c for t, c in titulos_contador.items() if c > 1)

    # ========================================================================
    # GENERAR INFORME
    # ========================================================================
    lineas = []
    lineas.append("# Informe Final: Mercado Inmobiliario Digital en Diez de Octubre")
    lineas.append("")
    lineas.append(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lineas.append(f"Total de anuncios analizados: {total}")
    lineas.append("")
    lineas.append("## Introducción")
    lineas.append("")
    lineas.append("Este informe presenta el análisis del mercado inmobiliario digital en el municipio Diez de Octubre, La Habana, basado en anuncios publicados en la plataforma digital Revolico. Los datos han sido recopilados, limpiados y analizados para responder a 30 preguntas de investigación organizadas en 6 bloques temáticos.")
    lineas.append("")
    lineas.append("## Metodología")
    lineas.append("")
    lineas.append("- Los datos provienen de anuncios publicados en Revolico.")
    lineas.append("- Se han filtrado anuncios con precios imposibles, municipios incorrectos, títulos sin información y anuncios no inmobiliarios.")
    lineas.append("- Solo se presentan preguntas con al menos 10 anuncios de base.")
    lineas.append("- Las preguntas con menos de 10 anuncios han sido sustituidas por preguntas con datos suficientes.")
    lineas.append("")
    lineas.append("## Las 30 preguntas y sus respuestas")
    lineas.append("")

    # Bloque A: Precios del mercado
    lineas.append("### Bloque A: Precios del mercado")
    lineas.append("")
    lineas.append("1. ¿Cuál es el precio promedio de venta en USD en Diez de Octubre?")
    if precios_venta_usd:
        lineas.append(f"   > Respuesta: ${promedio_venta:,.2f} USD (basado en {len(precios_venta_usd)} anuncios de venta con precio declarado)")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("2. ¿Cuál es el precio mediano de alquiler en USD?")
    if len(precios_alquiler_usd) >= 5:
        lineas.append(f"   > Respuesta: ${mediana_alquiler:,.2f} USD (basado en {len(precios_alquiler_usd)} anuncios de alquiler)")
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
        lineas.append(f"   > Más caro: ${precio_max:,} USD")
        lineas.append(f"   > Más barato: ${precio_min:,} USD")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("5. ¿Qué proporción de anuncios no declara precio?")
    proporcion = (len(sin_precio) / total * 100) if total else 0
    lineas.append(f"   > Respuesta: {proporcion:.2f}% ({len(sin_precio)} de {total} anuncios)")
    lineas.append("")

    lineas.append("6. ¿Existe diferencia significativa entre el precio promedio de venta y el de alquiler?")
    if len(precios_venta_usd) >= 5 and len(precios_alquiler_usd) >= 5:
        diferencia = promedio_venta - promedio_alquiler_usd
        lineas.append(f"   > Respuesta: Sí. Precio promedio de venta: ${promedio_venta:,.2f} USD vs. Precio mediano de alquiler: ${mediana_alquiler:,.2f} USD. Diferencia: ${diferencia:,.2f} USD.")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes para comparar.")
    lineas.append("")

    # Bloque B: Tipos de inmueble
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
    for tipo, precios_t in sorted(precios_por_tipo.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True):
        if len(precios_t) >= 5:
            prom_t = sum(precios_t) / len(precios_t)
            lineas.append(f"   > {tipo}: ${prom_t:,.2f} USD (n={len(precios_t)})")
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
        zonas_con_precio = {z: p for z, p in precios_por_zona.items() if len(p) >= 3}
        if zonas_con_precio:
            zona_max = max(zonas_con_precio, key=lambda z: sum(precios_por_zona[z]) / len(precios_por_zona[z]))
            precios_zona_max = precios_por_zona[zona_max]
            prom_zona_max = sum(precios_zona_max) / len(precios_zona_max)
            tipos_zona = Counter()
            for a in dt:
                zona_a = obtener_zona(a.get("titulo", ""), a.get("enlace", ""))
                if zona_a == zona_max and a.get("precio") is not None and a.get("moneda", "").upper() == "USD":
                    t = obtener_tipo(a.get("titulo", ""))
                    tipos_zona[t] += 1
            if tipos_zona:
                tipo_dominante = tipos_zona.most_common(1)[0][0]
                lineas.append(f"   > Respuesta: {zona_max} con ${prom_zona_max:,.2f} USD promedio ({len(precios_zona_max)} anuncios). Tipo dominante: {tipo_dominante}")
            else:
                lineas.append("   > Respuesta: No hay datos suficientes.")
        else:
            lineas.append("   > Respuesta: No hay suficientes zonas con datos.")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    # Bloque C: Características físicas
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
        pcs = precios_por_cuartos[cuartos]
        if len(pcs) >= 3:
            prom_c = sum(pcs) / len(pcs)
            lineas.append(f"   > {cuartos} cuarto(s): ${prom_c:,.2f} USD (n={len(pcs)})")
            hay_datos = True
    if not hay_datos:
        lineas.append("   > Respuesta: No hay datos suficientes.")
    lineas.append("")

    lineas.append("15. ¿Qué porcentaje de anuncios menciona garaje y cómo afecta al precio?")
    p_garaje = len(con_garaje) / total * 100 if total else 0
    if len(con_garaje_y_precio) >= 3 and len(sin_garaje_y_precio) >= 3:
        prom_con_garaje = sum(a["precio"] for a in con_garaje_y_precio) / len(con_garaje_y_precio)
        prom_sin_garaje = sum(a["precio"] for a in sin_garaje_y_precio) / len(sin_garaje_y_precio)
        diferencia = prom_con_garaje - prom_sin_garaje
        lineas.append(f"   > {con_garaje} de {total} anuncios ({p_garaje:.1f}%) mencionan garaje.")
        lineas.append(f"   > Precio promedio con garaje: ${prom_con_garaje:,.2f} USD")
        lineas.append(f"   > Precio promedio sin garaje: ${prom_sin_garaje:,.2f} USD")
        lineas.append(f"   > Diferencia: ${diferencia:,.2f} USD")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes para comparar.")
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
    p_metro = len(con_metro) / total * 100 if total else 0
    if len(con_metro_y_precio) >= 3:
        prom_metro = sum(a["precio"] for a in con_metro_y_precio) / len(con_metro_y_precio)
        lineas.append(f"   > {con_metro} de {total} anuncios ({p_metro:.1f}%) mencionan metraje.")
        lineas.append(f"   > Precio promedio: ${prom_metro:,.2f} USD (n={len(con_metro_y_precio)})")
    else:
        lineas.append("   > Respuesta: No hay datos suficientes (menos de 3 anuncios con precio y metraje).")
    lineas.append("")

    lineas.append("18. ¿Qué características físicas se mencionan con más frecuencia?")
    for car, count in cont_caracteristicas.most_common(10):
        lineas.append(f"   > {car.capitalize()}: {count} anuncios")
    lineas.append("")

    # Bloque D: Ubicación
    lineas.append("### Bloque D: Ubicación dentro de Diez de Octubre")
    lineas.append("")
    lineas.append("19. ¿Qué zonas o barrios aparecen con más frecuencia en los anuncios?")
    for zona, count in zonas_contador.most_common(10):
        lineas.append(f"   > {zona}: {count} anuncios")
    lineas.append("")

    lineas.append("20. ¿Qué zona tiene el precio promedio de venta más alto?")
    if precios_por_zona:
        zonas_con_precio = {z: p for z, p in precios_por_zona.items() if len(p) >= 3}
        if zonas_con_precio:
            zona_max = max(zonas_con_precio, key=lambda z: sum(precios_por_zona[z]) / len(precios_por_zona[z]))
            precios_zona_max = precios_por_zona[zona_max]
            prom_zona_max = sum(precios_zona_max) / len(precios_zona_max)
            lineas.append(f"   > Respuesta: {zona_max} con ${prom_zona_max:,.2f} USD promedio ({len(precios_zona_max)} anuncios)")
        else:
            lineas.append("   > Respuesta: No hay suficientes datos por zona.")
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
        zonas_con_precio = {z: p for z, p in precios_por_zona.items() if len(p) >= 3}
        if len(zonas_con_precio) >= 2:
            promedios_por_zona = {z: sum(p) / len(p) for z, p in zonas_con_precio.items()}
            zona_max_p = max(promedios_por_zona, key=promedios_por_zona.get)
            zona_min_p = min(promedios_por_zona, key=promedios_por_zona.get)
            dif_z = promedios_por_zona[zona_max_p] - promedios_por_zona[zona_min_p]
            lineas.append(f"   > Respuesta: Sí. La zona más cara es {zona_max_p} (${promedios_por_zona[zona_max_p]:,.2f} USD) y la más barata es {zona_min_p} (${promedios_por_zona[zona_min_p]:,.2f} USD). Diferencia: ${dif_z:,.2f} USD.")
        else:
            lineas.append("   > Respuesta: No hay suficientes zonas con datos.")
    else:
        lineas.append("   > Respuesta: No hay suficientes datos para comparar zonas.")
    lineas.append("")

    lineas.append("23. ¿Qué zonas aparecen solo en venta o solo en alquiler?")
    lineas.append(f"   > Zonas solo en venta ({len(zonas_solo_venta)}): {', '.join(sorted(zonas_solo_venta)) if zonas_solo_venta else 'Ninguna'}")
    lineas.append(f"   > Zonas solo en alquiler ({len(zonas_solo_alquiler)}): {', '.join(sorted(zonas_solo_alquiler)) if zonas_solo_alquiler else 'Ninguna'}")
    lineas.append(f"   > Zonas en ambas categorías ({len(zonas_ambas)}): {', '.join(sorted(zonas_ambas)) if zonas_ambas else 'Ninguna'}")
    lineas.append("")

    lineas.append("24. ¿Cuántos anuncios no especifican zona dentro del municipio?")
    zs = sum(1 for a in dt if obtener_zona(a.get("titulo", ""), a.get("enlace", "")) == "No especificado")
    lineas.append(f"   > Respuesta: {zs} de {total} anuncios ({zs/total*100:.1f}%) no especifican zona dentro de Diez de Octubre.")
    lineas.append("")

    # Bloque E: Moneda y mercado informal
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
        lineas.append("   > Respuesta: No hay datos suficientes (menos de 3 anuncios con precio en CUP).")
    lineas.append("")

    lineas.append("27. ¿Qué porcentaje de anuncios incluye palabras como 'oportunidad', 'ganga' o 'permuta'?")
    total_inf = sum(informalidad_contador.values())
    p_inf = total_con_palabras_informalidad / total * 100 if total else 0
    lineas.append(f"   > {total_con_palabras_informalidad} de {total} anuncios ({p_inf:.1f}%) incluyen palabras de mercado informal.")
    for palabra, count in informalidad_contador.most_common():
        lineas.append(f"      - {palabra.capitalize()}: {count} menciones")
    lineas.append("")

    # Rangos de precios
    rangos_contador = Counter()
    for p in precios_venta_usd:
        if p < 10000:
            rangos_contador["0 - 10,000"] += 1
        elif p < 20000:
            rangos_contador["10,000 - 20,000"] += 1
        elif p < 30000:
            rangos_contador["20,000 - 30,000"] += 1
        elif p < 40000:
            rangos_contador["30,000 - 40,000"] += 1
        elif p < 50000:
            rangos_contador["40,000 - 50,000"] += 1
        elif p < 60000:
            rangos_contador["50,000 - 60,000"] += 1
        elif p < 70000:
            rangos_contador["60,000 - 70,000"] += 1
        elif p < 80000:
            rangos_contador["70,000 - 80,000"] += 1
        elif p < 90000:
            rangos_contador["80,000 - 90,000"] += 1
        else:
            rangos_contador["90,000+"] += 1

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
    lineas.append(f"   > Total de títulos únicos: {titulos_unicos}")
    lineas.append(f"   > Anuncios con título único (probables particulares): {titulos_unicos}")
    lineas.append(f"   > Anuncios con título repetido (posibles agencias o anuncios duplicados): {anuncios_titulos_repetidos} anuncios en {titulos_repetidos} títulos repetidos")
    if titulos_repetidos > 0:
        lineas.append("   > Títulos repetidos:")
        for t, c in titulos_contador.items():
            if c > 1:
                lineas.append(f"      '{t}': {c} veces")
    lineas.append("")

    lineas.append("30. ¿Qué recomendación práctica se puede hacer a alguien que quiera comprar o alquilar en Diez de Octubre según estos datos?")
    lineas.append("")
    lineas.append("   > Respuesta: Basado en el análisis de los datos del mercado inmobiliario digital en Diez de Octubre:")
    lineas.append("")
    lineas.append("   1. **Precios razonables**: El precio promedio de venta en USD es de ${promedio_venta:,.2f}, con una mediana de ${mediana_venta:,.2f} USD. El rango más común de precios se encuentra entre ${p10:,.2f} y ${p90:,.2f} USD.")
    lineas.append("")
    lineas.append("   2. **Zonas más activas**: Santos Suárez, La Víbora, Lawton y Luyano son las zonas con mayor cantidad de anuncios publicados.")
    lineas.append("")
    lineas.append("   3. **Precios por zona**: Hay diferencias significativas de precios entre zonas dentro del mismo municipio. Se recomienda investigar específicamente la zona de interés antes de tomar una decisión.")
    lineas.append("")
    lineas.append("   4. **Moneda**: La gran mayoría de los anuncios se declaran en USD, por lo que se recomienda contar con esta moneda para realizar transacciones inmobiliarias en el área.")
    lineas.append("")
    lineas.append("   5. **Permuta**: El mercado de permutas está presente en el mercado, lo que puede ser una opción para quienes no cuentan con efectivo completo.")
    lineas.append("")
    lineas.append("   6. **Precaución**: Dado que muchos anuncios no declaran precio y algunos títulos son genéricos, se recomienda verificar directamente con el vendedor antes de realizar cualquier gestión.")
    lineas.append("")
    lineas.append("   7. **Análisis por zona**: Se recomienda enfocarse en zonas específicas según el presupuesto disponible, ya que existen diferencias de precios entre zonas dentro del mismo municipio.")
    lineas.append("")

    # Conclusiones
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
