#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el informe final con las 30 preguntas de investigación del mercado
inmobiliario digital en Diez de Octubre, La Habana.

Criterios:
- Base: 171 anuncios limpios de Revolico en Diez de Octubre.
- Precios: 136 anuncios en USD (1 en CUP, 34 sin precio).
- Preguntas con respuestas insuficientes sustituidas por preguntas con datos.
- Cada respuesta indica el tamaño de muestra (n) que la sustenta.

Lee:  datos/brutos/revolico_crudos_limpio_final.json
Escribe: analisis/informe_final.md
"""

import json
import math
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime

INPUT_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
OUTPUT_FILE = "analisis/informe_final.md"

FEATURES = [
    "garaje", "garage", "patio", "azotea", "terraza",
    "balcón", "balcon", "baño", "bano", "cuarto", "habitación", "habitacion",
]


def cargar_datos():
    with open(INPUT_FILE, encoding="utf-8") as f:
        return json.load(f)


def es_venta(titulo):
    t = (titulo or "").lower()
    venta = ["vendo", "se vende", "venta", "vende", "permuta", "permuto"]
    alquiler = ["alquiler", "alquila", "se alquila", "renta"]
    return any(p in t for p in venta) and not any(p in t for p in alquiler)


def es_alquiler(titulo):
    t = (titulo or "").lower()
    alquiler = ["alquiler", "alquila", "se alquila", "renta"]
    venta = ["vendo", "se vende", "venta", "vende"]
    return any(p in t for p in alquiler) and not any(p in t for p in venta)


def obtener_tipo(titulo):
    t = (titulo or "").lower()
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
    texto = ((titulo or "") + " " + (enlace or "")).lower()
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
        ("Vía Blanca", ["vía blanca", "via blanca"]),
        ("Calzada 10 de Octubre", ["calzada 10 de octubre", "calzada diez de octubre"]),
    ]
    for nombre, variantes in zonas:
        for variante in variantes:
            if variante in texto:
                return nombre
    return "No especificado"


def obtener_cuartos(titulo):
    t = (titulo or "").lower()
    for patron in [r"(\d+)/4", r"(\d+)\s*cuartos?", r"(\d+)\s*hab", r"(\d+)\s*recámara"]:
        m = re.search(patron, t)
        if m:
            return int(m.group(1))
    return None


def tiene_alguna_feature(titulo):
    t = (titulo or "").lower()
    return any(f in t for f in FEATURES)


def precio_usd(anuncio):
    return (
        anuncio.get("precio") is not None
        and str(anuncio.get("moneda", "")).upper() == "USD"
    )


def percentil(valores_ordenados, p):
    """Percentil con interpolación lineal."""
    n = len(valores_ordenados)
    if n == 0:
        return 0
    k = (n - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return valores_ordenados[f]
    return valores_ordenados[f] * (c - k) + valores_ordenados[c] * (k - f)


def fmt(valor):
    return f"{valor:,.2f}"


def unidad(n):
    return "anuncio" if n == 1 else "anuncios"


def main():
    anuncios = cargar_datos()
    total = len(anuncios)

    # ---------------------------------------------------------------
    # Clasificaciones y subconjuntos
    # ---------------------------------------------------------------
    for a in anuncios:
        a["_tipo"] = obtener_tipo(a.get("titulo"))
        a["_zona"] = obtener_zona(a.get("titulo"), a.get("enlace"))

    usd = [a for a in anuncios if precio_usd(a)]
    precios = [a["precio"] for a in usd]
    precios_ordenados = sorted(precios)
    n_usd = len(precios)

    promedio = sum(precios) / n_usd if n_usd else 0
    mediana = statistics.median(precios) if precios else 0
    p10 = percentil(precios_ordenados, 0.10)
    p90 = percentil(precios_ordenados, 0.90)
    precio_min = min(precios) if precios else 0
    precio_max = max(precios) if precios else 0

    en_rango = [p for p in precios if p10 <= p <= p90]
    promedio_rango = sum(en_rango) / len(en_rango) if en_rango else 0
    mediana_rango = statistics.median(en_rango) if en_rango else 0
    fuera_rango = n_usd - len(en_rango)

    sin_precio = [a for a in anuncios if a.get("precio") is None]
    cup = [a for a in anuncios if str(a.get("moneda", "")).upper() == "CUP"]

    # Tipos
    tipos = Counter(a["_tipo"] for a in anuncios)

    # Precio por tipo
    precios_tipo = defaultdict(list)
    for a in usd:
        precios_tipo[a["_tipo"]].append(a["precio"])

    tipos_excluidos = sorted(
        ((t, len(v)) for t, v in precios_tipo.items() if len(v) < 5),
        key=lambda x: x[1],
    )

    # Zonas
    zonas = Counter(a["_zona"] for a in anuncios if a["_zona"] != "No especificado")
    total_con_zona = sum(zonas.values())
    sin_zona = total - total_con_zona

    precios_zona = defaultdict(list)
    for a in usd:
        if a["_zona"] != "No especificado":
            precios_zona[a["_zona"]].append(a["precio"])

    # Venta / alquiler / sin clasificar
    ventas = [a for a in anuncios if es_venta(a.get("titulo"))]
    alquileres = [a for a in anuncios if es_alquiler(a.get("titulo"))]
    sin_clasificar = total - len(ventas) - len(alquileres)
    alquileres_usd = [a for a in alquileres if precio_usd(a)]
    alquileres_cup = [
        a for a in alquileres
        if a.get("precio") is not None
        and str(a.get("moneda", "")).upper() == "CUP"
    ]

    # Subconjunto de ventas explícitas con precio en USD (para contrastar)
    ventas_usd = [a for a in ventas if precio_usd(a)]
    precios_ventas = [a["precio"] for a in ventas_usd]
    prom_ventas = sum(precios_ventas) / len(precios_ventas) if precios_ventas else 0
    mediana_ventas = statistics.median(precios_ventas) if precios_ventas else 0

    # Cuartos
    cuartos_ads = [(a, obtener_cuartos(a.get("titulo"))) for a in anuncios]
    cuartos_ads = [(a, c) for a, c in cuartos_ads if c]
    cuartos_conteo = Counter(c for _, c in cuartos_ads)
    cuartos_moda = cuartos_conteo.most_common(1)[0] if cuartos_conteo else (0, 0)
    cuartos_promedio = (
        sum(c for _, c in cuartos_ads) / len(cuartos_ads) if cuartos_ads else 0
    )

    precios_cuartos = defaultdict(list)
    for a, c in cuartos_ads:
        if precio_usd(a):
            precios_cuartos[c].append(a["precio"])

    # Garaje
    con_garaje = [
        a for a in anuncios
        if "garaje" in (a.get("titulo") or "").lower()
        or "garage" in (a.get("titulo") or "").lower()
    ]
    garaje_usd = [a for a in con_garaje if precio_usd(a)]
    sin_garaje_usd = [a for a in usd if a not in con_garaje]
    prom_garaje = (
        sum(a["precio"] for a in garaje_usd) / len(garaje_usd) if garaje_usd else 0
    )
    prom_sin_garaje = (
        sum(a["precio"] for a in sin_garaje_usd) / len(sin_garaje_usd)
        if sin_garaje_usd else 0
    )
    dif_garaje = prom_garaje - prom_sin_garaje

    # Planta baja
    planta_baja = [
        a for a in anuncios
        if "planta baja" in (a.get("titulo") or "").lower()
        or "bajos" in (a.get("titulo") or "").lower()
    ]
    planta_baja_usd = [a for a in planta_baja if precio_usd(a)]
    prom_planta_baja = (
        sum(a["precio"] for a in planta_baja_usd) / len(planta_baja_usd)
        if planta_baja_usd else 0
    )

    # Características físicas
    con_feature = [a for a in anuncios if tiene_alguna_feature(a.get("titulo"))]
    feature_conteo = Counter()
    for a in anuncios:
        t = (a.get("titulo") or "").lower()
        for f in ["garaje", "cuarto", "baño", "terraza", "balcón", "azotea", "sala", "patio"]:
            if f in t:
                feature_conteo[f] += 1

    # Moneda
    con_moneda = [a for a in anuncios if str(a.get("moneda", "")).upper() in ("USD", "CUP")]

    # Lenguaje informal
    palabras_inf = ["oportunidad", "ganga", "permuta", "intercambio", "cambio"]
    con_informal = [
        a for a in anuncios
        if any(p in (a.get("titulo") or "").lower() for p in palabras_inf)
    ]
    sin_informal = [a for a in anuncios if a not in con_informal]
    informal_con_precio = sum(1 for a in con_informal if a.get("precio") is not None)
    neutro_con_precio = sum(1 for a in sin_informal if a.get("precio") is not None)
    pct_informal_precio = 100 * informal_con_precio / len(con_informal) if con_informal else 0
    pct_neutro_precio = 100 * neutro_con_precio / len(sin_informal) if sin_informal else 0
    informal_contador = Counter(
        p for a in anuncios for p in palabras_inf
        if p in (a.get("titulo") or "").lower()
    )

    # Títulos
    titulos = Counter(a.get("titulo", "") for a in anuncios)
    titulos_unicos = sum(1 for c in titulos.values() if c == 1)
    titulos_repetidos = sum(1 for c in titulos.values() if c > 1)

    # Rangos de precio
    bins = [
        (0, 10000, "0 - 10,000"),
        (10000, 20000, "10,000 - 20,000"),
        (20000, 30000, "20,000 - 30,000"),
        (30000, 40000, "30,000 - 40,000"),
        (40000, 50000, "40,000 - 50,000"),
        (50000, 60000, "50,000 - 60,000"),
        (60000, 70000, "60,000 - 70,000"),
        (70000, 80000, "70,000 - 80,000"),
        (80000, float("inf"), "80,000+"),
    ]
    rangos = Counter()
    for p in precios:
        for lo, hi, etiqueta in bins:
            if lo <= p < hi:
                rangos[etiqueta] += 1
                break
    rango_top = rangos.most_common(1)[0] if rangos else ("", 0)

    # Top zonas
    top4_zonas = zonas.most_common(4)
    top4_total = sum(c for _, c in top4_zonas)
    pct_top4 = 100 * top4_total / total_con_zona if total_con_zona else 0

    # Zonas con al menos 5 anuncios con precio (evita promedios de n = 1)
    zonas_5 = {
        z: p for z, p in precios_zona.items() if len(p) >= 5
    }
    zona_cara = max(zonas_5, key=lambda z: sum(zonas_5[z]) / len(zonas_5[z]))
    zona_barata = min(zonas_5, key=lambda z: sum(zonas_5[z]) / len(zonas_5[z]))
    prom_zona_cara = sum(zonas_5[zona_cara]) / len(zonas_5[zona_cara])
    prom_zona_barata = sum(zonas_5[zona_barata]) / len(zonas_5[zona_barata])
    tipos_zona_cara = Counter(
        a["_tipo"] for a in usd if a["_zona"] == zona_cara
    )
    tipo_dominante = tipos_zona_cara.most_common(1)[0][0]

    # Zonas con al menos 10 anuncios con precio
    zonas_10 = {
        z: p for z, p in precios_zona.items() if len(p) >= 10
    }
    zona_10_cara = max(zonas_10, key=lambda z: sum(zonas_10[z]) / len(zonas_10[z]))
    zona_10_barata = min(zonas_10, key=lambda z: sum(zonas_10[z]) / len(zonas_10[z]))
    prom_10_cara = sum(zonas_10[zona_10_cara]) / len(zonas_10[zona_10_cara])
    prom_10_barata = sum(zonas_10[zona_10_barata]) / len(zonas_10[zona_10_barata])

    # ---------------------------------------------------------------
    # Informe
    # ---------------------------------------------------------------
    L = []
    L.append("# Informe Final: Mercado Inmobiliario Digital en Diez de Octubre")
    L.append("")
    L.append(f"**Fecha de generación:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    L.append(f"**Universo analizado:** {total} anuncios limpios de Revolico")
    L.append(f"**Anuncios con precio en USD:** {n_usd}")
    L.append("")
    L.append("## Introducción")
    L.append("")
    L.append(
        "Este informe analiza el mercado inmobiliario digital del municipio Diez de "
        "Octubre, La Habana, a partir de anuncios publicados en Revolico. Se responden "
        "30 preguntas de investigación organizadas en cinco bloques temáticos (A–E). "
        "Las preguntas cuyas respuestas no alcanzaban una base mínima de datos fueron "
        "sustituidas por preguntas alternativas respondibles con la información disponible."
    )
    L.append("")
    L.append("## Metodología")
    L.append("")
    L.append("- Se trabajó con 171 anuncios previamente limpiados: solo Diez de Octubre y precio mínimo de 1,000 USD cuando existe precio.")
    L.append("- Los análisis de precio usan los 136 anuncios con precio declarado en USD; se excluye 1 anuncio en CUP y 34 sin precio.")
    L.append("- Para reducir el efecto de valores extremos se reporta el rango P10–P90 y la mediana junto a la media.")
    L.append("- Cada respuesta indica su tamaño de muestra (n). Los subgrupos con n < 10 se presentan como evidencia descriptiva, no como conclusión firme.")
    L.append("- La clasificación de tipo, zona y características se infiere de palabras clave del título y del enlace.")
    L.append("")
    L.append("## Fuente y universo de datos")
    L.append("")
    L.append("- **Revolico (fuente principal):** 171 anuncios limpios del municipio Diez de Octubre. Es la única fuente usada en los cálculos de este informe.")
    L.append("- **Anuario Estadístico de Cuba (ONEI):** se consulta como contexto general del municipio; no se usa para calcular precios ni proporciones de la muestra digital.")
    L.append("- **Facebook (fuente explorada, no integrada):** se revisaron 37 publicaciones de grupos de compraventa. Se excluyeron del análisis cuantitativo porque no comparten el esquema de campos de Revolico (precio anidado, ubicación en texto libre y sin municipio normalizado) y no permiten aplicar el mismo filtro municipal y de limpieza. Incorporarlas sin normalizar habría mezclado universos distintos. Se conservan en `datos/limpios/datos_unificados_facebook_revolico.json` para una ampliación futura.")
    L.append("")
    L.append("## Preguntas sustituidas")
    L.append("")
    L.append("Cinco preguntas del cuestionario original no podían responderse con una base mínima de datos. Se sustituyeron por preguntas equivalentes y respondibles:")
    L.append("")
    L.append("| # | Pregunta original | Motivo de la sustitución | Pregunta nueva |")
    L.append("|---|---|---|---|")
    L.append("| 2 | ¿Cuál es la mediana del precio de alquiler? | Solo 2 anuncios de alquiler declaran precio (1 USD y 1 CUP). | ¿Cuál es el precio mediano de los anuncios con precio en USD? |")
    L.append("| 6 | ¿Es más caro comprar que alquilar? | Solo 1 alquiler tiene precio en USD; no hay base para comparar. | ¿Qué tan dispersos son los precios respecto a la media? |")
    L.append("| 17 | ¿Cuál es el precio promedio por metro cuadrado? | Solo 3 anuncios mencionan metraje. | ¿Qué proporción de anuncios incluye al menos una característica física explícita? |")
    L.append("| 23 | ¿Qué zonas concentran más anuncios de venta y de alquiler? | Solo una zona tiene algún anuncio de alquiler. | ¿Qué proporción de los anuncios con zona identificada se concentra en las cuatro zonas principales? |")
    L.append("| 26 | ¿Cuál es el precio promedio en CUP? | Solo 1 anuncio declara precio en CUP. | ¿Los anuncios con lenguaje informal declaran precio con más frecuencia que los neutros? |")
    L.append("")
    L.append("Además de esas cinco sustituciones, la **Q1** se reformuló de «precio promedio de venta» a «precio promedio de los anuncios con precio declarado en USD», porque solo 50 anuncios de venta explícita declaran precio en USD. Por la misma razón, **Q20** y **Q28** se expresan sobre anuncios con precio en USD. Cuando aporta información, se reporta por separado el subconjunto de ventas explícitas con precio en USD (Q1, Q2 y Q11).")
    L.append("")
    L.append("## Las 30 preguntas y sus respuestas")
    L.append("")

    # ---------------- BLOQUE A ----------------
    L.append("### Bloque A: Precios del mercado")
    L.append("")
    L.append("**1. ¿Cuál es el precio promedio de los anuncios con precio declarado en USD en Diez de Octubre?**")
    L.append("")
    L.append(f"> **${fmt(promedio)} USD** (n = {n_usd}). Si se excluyen los valores extremos y se calcula sobre el tramo P10–P90, el promedio baja a **${fmt(promedio_rango)} USD** (n = {len(en_rango)}). Si se restringe a los {len(ventas_usd)} anuncios de venta explícita que declaran precio en USD, el promedio es **${fmt(prom_ventas)} USD**.")
    L.append("")
    L.append("**2. ¿Cuál es el precio mediano de los anuncios con precio declarado en USD?**")
    L.append("")
    L.append(f"> **${fmt(mediana)} USD** (n = {n_usd}). La mediana es menor que la media porque unos pocos anuncios muy caros elevan el promedio. En el subconjunto de ventas explícitas con precio en USD, la mediana es **${fmt(mediana_ventas)} USD** (n = {len(ventas_usd)}).")
    L.append("")
    L.append("**3. ¿Cuál es el rango de precios que cubre el 80% central de los anuncios?**")
    L.append("")
    L.append(f"> Entre **${fmt(p10)} USD** (P10) y **${fmt(p90)} USD** (P90). Dentro de ese tramo se concentran **{len(en_rango)} de {n_usd} anuncios ({100*len(en_rango)/n_usd:.1f}%)**.")
    L.append("")
    L.append("**4. ¿Cuáles son el anuncio más caro y el más barato publicados?**")
    L.append("")
    L.append(f"> Más caro: **${fmt(precio_max)} USD**. Más barato: **${fmt(precio_min)} USD**.")
    L.append("")
    L.append("**5. ¿Qué proporción de anuncios no declara precio?**")
    L.append("")
    L.append(f"> **{len(sin_precio)} de {total} anuncios ({100*len(sin_precio)/total:.2f}%)** no declaran precio. Esto obliga a contactar al vendedor para conocerlo.")
    L.append("")
    L.append("**6. ¿Qué tan dispersos son los precios respecto a la media?**")
    L.append("")
    L.append(f"> La media (${fmt(promedio)}) supera a la mediana (${fmt(mediana)}) en **${fmt(promedio-mediana)}**, un {100*(promedio-mediana)/mediana:.1f}% de la mediana. Además, **{fuera_rango} anuncios ({100*fuera_rango/n_usd:.1f}%)** quedan fuera del tramo P10–P90. La distribución está sesgada a la derecha: hay una minoría de inmuebles de lujo que infla el promedio.")
    L.append("")

    # ---------------- BLOQUE B ----------------
    L.append("### Bloque B: Tipos de inmueble")
    L.append("")
    L.append("**7. ¿Cuáles son los tipos de inmueble más publicados?**")
    L.append("")
    for tipo, count in tipos.most_common():
        L.append(f"> - {tipo}: **{count} anuncios** ({100*count/total:.1f}%)")
    L.append("")
    L.append("**8. ¿Qué porcentaje son casas independientes frente a apartamentos?**")
    L.append("")
    casas = tipos.get("Casa", 0)
    aptos = tipos.get("Apartamento", 0)
    base_tipos = casas + aptos
    L.append(f"> Casas: **{casas} ({100*casas/base_tipos:.1f}%)**. Apartamentos: **{aptos} ({100*aptos/base_tipos:.1f}%)** (n = {base_tipos} anuncios con tipo identificable entre ambos).")
    L.append("")
    L.append("**9. ¿Cuál es el precio promedio por tipo de inmueble (anuncios con precio en USD)?**")
    L.append("")
    for tipo, vals in sorted(precios_tipo.items(), key=lambda x: -sum(x[1]) / len(x[1])):
        if len(vals) >= 5:
            L.append(f"> - {tipo}: **${fmt(sum(vals)/len(vals))} USD** (n = {len(vals)})")
    L.append("> ")
    if tipos_excluidos:
        detalle_excluidos = ", ".join(f"{t} ({n})" for t, n in tipos_excluidos)
        L.append(f"> Se excluyen los tipos con menos de 5 anuncios con precio: {detalle_excluidos}.")
    L.append("")
    L.append("**10. ¿Qué tipo de inmueble concentra el precio máximo declarado?**")
    L.append("")
    tipo_max = max(precios_tipo, key=lambda t: max(precios_tipo[t]))
    anuncio_max = max(usd, key=lambda a: a["precio"])
    segundo_max = sorted(precios)[-2]
    L.append(f"> **{tipo_max}**, la categoría que agrupa los títulos que no especifican un tipo, con el anuncio «{anuncio_max.get('titulo', '')}» a **${fmt(max(precios_tipo[tipo_max]))} USD**. Es un valor atípico: el segundo precio más alto es **${fmt(segundo_max)} USD**.")
    L.append("")
    L.append("**11. ¿Cuántos anuncios se identifican como venta, alquiler o sin clasificar?**")
    L.append("")
    L.append(f"> Venta: **{len(ventas)} anuncios ({100*len(ventas)/total:.1f}%)**. Alquiler: **{len(alquileres)} ({100*len(alquileres)/total:.1f}%)**. Sin clasificar por título: **{sin_clasificar} ({100*sin_clasificar/total:.1f}%)**. De los {len(alquileres)} alquileres, solo {len(alquileres_usd)} declara precio en USD y {len(alquileres_cup)} en CUP; por eso no se puede comparar estadísticamente el precio de alquiler con el de venta.")
    L.append("")
    L.append("**12. ¿Qué tipo de inmueble domina en la zona con el precio promedio más alto?**")
    L.append("")
    L.append(f"> Entre las zonas con al menos 5 anuncios con precio, **{zona_cara}** tiene el promedio más alto: **${fmt(prom_zona_cara)} USD** (n = {len(zonas_5[zona_cara])}). El tipo dominante es **{tipo_dominante}** ({tipos_zona_cara[tipo_dominante]} de {len(zonas_5[zona_cara])} anuncios con precio).")
    L.append("")

    # ---------------- BLOQUE C ----------------
    L.append("### Bloque C: Características físicas")
    L.append("")
    L.append("**13. ¿Cuál es la cantidad más común de cuartos/habitaciones?**")
    L.append("")
    L.append(f"> **{cuartos_moda[0]} cuartos**, presente en **{cuartos_moda[1]} de {len(cuartos_ads)} anuncios** que especifican el dato ({100*cuartos_moda[1]/len(cuartos_ads):.1f}%).")
    L.append("")
    L.append("**14. ¿Cómo varía el precio según el número de cuartos?**")
    L.append("")
    for c in sorted(precios_cuartos):
        vals = precios_cuartos[c]
        if c in (2, 3) and len(vals) >= 5:
            L.append(f"> - {c} cuartos: **${fmt(sum(vals)/len(vals))} USD** (n = {len(vals)})")
    L.append("> ")
    dif_cuartos = (
        sum(precios_cuartos[3]) / len(precios_cuartos[3])
        - sum(precios_cuartos[2]) / len(precios_cuartos[2])
    )
    L.append(f"> Los anuncios de 2 y 3 cuartos son los únicos subgrupos con al menos 5 casos. El precio promedio sube de 2 a 3 cuartos en **${fmt(dif_cuartos)} USD**.")
    L.append("")
    L.append("**15. ¿Qué porcentaje de anuncios menciona garaje y cómo se relaciona con el precio?**")
    L.append("")
    L.append(f"> **{len(con_garaje)} de {total} anuncios ({100*len(con_garaje)/total:.1f}%)** mencionan garaje. Entre los que declaran precio en USD, el promedio con garaje es **${fmt(prom_garaje)} USD** (n = {len(garaje_usd)}) frente a **${fmt(prom_sin_garaje)} USD** sin garaje (n = {len(sin_garaje_usd)}): una diferencia de **${fmt(dif_garaje)} USD** ({100*dif_garaje/prom_sin_garaje:.1f}% más). El subgrupo con garaje es pequeño (n = {len(garaje_usd)}), así que la diferencia es indicativa, no concluyente.")
    L.append("")
    L.append("**16. ¿Cuántos anuncios especifican 'planta baja' y cuál es su precio promedio?**")
    L.append("")
    L.append(f"> **{len(planta_baja)} anuncios ({100*len(planta_baja)/total:.1f}%)** mencionan planta baja o bajos; los **{len(planta_baja_usd)}** con precio en USD promedian **${fmt(prom_planta_baja)} USD**. Es un grupo pequeño (n = {len(planta_baja_usd)}), por lo que solo describe una tendencia.")
    L.append("")
    L.append("**17. ¿Qué proporción de anuncios incluye al menos una característica física explícita?**")
    L.append("")
    L.append(f"> **{len(con_feature)} de {total} anuncios ({100*len(con_feature)/total:.1f}%)** mencionan al menos una característica física (garaje, patio, azotea, terraza, balcón, baño, cuartos o habitaciones). De ellos, **{sum(1 for a in con_feature if precio_usd(a))}** declaran precio en USD.")
    L.append("")
    L.append("**18. ¿Qué características físicas se mencionan con más frecuencia?**")
    L.append("")
    for f, count in feature_conteo.most_common():
        L.append(f"> - {f.capitalize()}: **{count} {unidad(count)}**")
    L.append("")

    # ---------------- BLOQUE D ----------------
    L.append("### Bloque D: Ubicación dentro de Diez de Octubre")
    L.append("")
    L.append("**19. ¿Qué zonas o barrios aparecen con más frecuencia en los anuncios?**")
    L.append("")
    for z, count in zonas.most_common():
        L.append(f"> - {z}: **{count} {unidad(count)}**")
    L.append(f"> ")
    L.append(f"> **{sin_zona} de {total} anuncios ({100*sin_zona/total:.1f}%)** no especifican zona en el título.")
    L.append("")
    L.append("**20. ¿Qué zona tiene el precio promedio más alto entre los anuncios con precio en USD?**")
    L.append("")
    L.append(f"> Entre las zonas con al menos 5 anuncios con precio, **{zona_cara}** tiene el promedio más alto: **${fmt(prom_zona_cara)} USD** (n = {len(zonas_5[zona_cara])}). Si se exige n ≥ 10, la más cara es **{zona_10_cara}** (${fmt(prom_10_cara)} USD, n = {len(zonas_10[zona_10_cara])}).")
    L.append("")
    L.append("**21. ¿Qué zona tiene la mayor cantidad de anuncios publicados?**")
    L.append("")
    zona_top = zonas.most_common(1)[0]
    L.append(f"> **{zona_top[0]}**, con **{zona_top[1]} anuncios** ({sum(1 for a in anuncios if a['_zona'] == zona_top[0] and precio_usd(a))} de ellos con precio en USD).")
    L.append("")
    L.append("**22. ¿Hay diferencia de precios entre zonas dentro del mismo municipio?**")
    L.append("")
    L.append(f"> Sí. Entre las zonas con al menos 5 anuncios con precio, **{zona_cara}** promedia **${fmt(prom_zona_cara)} USD** (n = {len(zonas_5[zona_cara])}) y **{zona_barata}** promedia **${fmt(prom_zona_barata)} USD** (n = {len(zonas_5[zona_barata])}): una diferencia de **${fmt(prom_zona_cara-prom_zona_barata)} USD**. Si se comparan solo zonas con n ≥ 10, la diferencia entre {zona_10_cara} y {zona_10_barata} es de **${fmt(prom_10_cara-prom_10_barata)} USD**.")
    L.append("")
    L.append("**23. ¿Qué proporción de los anuncios con zona identificada se concentra en las cuatro zonas principales?**")
    L.append("")
    L.append(f"> Las cuatro zonas principales —{', '.join(z for z, _ in top4_zonas)}— reúnen **{top4_total} de {total_con_zona} anuncios con zona identificada ({pct_top4:.1f}%)**. La oferta está, por tanto, muy concentrada en pocos barrios.")
    L.append("")
    L.append("**24. ¿Cuántos anuncios no especifican zona dentro del municipio?**")
    L.append("")
    L.append(f"> **{sin_zona} de {total} anuncios ({100*sin_zona/total:.1f}%)** no especifican zona en el título ni en el enlace.")
    L.append("")

    # ---------------- BLOQUE E ----------------
    L.append("### Bloque E: Moneda y mercado informal")
    L.append("")
    L.append("**25. ¿Qué proporción de anuncios con moneda declarada usa USD frente a CUP?**")
    L.append("")
    L.append(f"> USD: **{len(usd)} de {len(con_moneda)} ({100*len(usd)/len(con_moneda):.1f}%)**. CUP: **{len(cup)} de {len(con_moneda)} ({100*len(cup)/len(con_moneda):.1f}%)**. Además, {len(sin_precio)} anuncios no declaran precio ni moneda. En el total del universo, el USD aparece en **{100*len(usd)/total:.1f}%** de los anuncios.")
    L.append("")
    L.append("**26. ¿Los anuncios con lenguaje informal declaran precio con más frecuencia que los anuncios con lenguaje neutro?**")
    L.append("")
    L.append(f"> Sí. Entre los **{len(con_informal)} anuncios** con palabras como 'oportunidad', 'ganga', 'permuta', 'intercambio' o 'cambio', **{informal_con_precio} ({pct_informal_precio:.1f}%)** declaran precio. Entre los **{len(sin_informal)} anuncios** con lenguaje neutro, lo hacen **{neutro_con_precio} ({pct_neutro_precio:.1f}%)**. La diferencia es de **{pct_informal_precio-pct_neutro_precio:.1f} puntos porcentuales**.")
    L.append("")
    L.append("**27. ¿Qué porcentaje de anuncios incluye palabras de mercado informal?**")
    L.append("")
    L.append(f"> **{len(con_informal)} de {total} anuncios ({100*len(con_informal)/total:.1f}%)**. Distribución: " + ", ".join(f"{p} ({c})" for p, c in informal_contador.most_common()) + ".")
    L.append("")
    L.append("**28. ¿Qué rango de precios es más frecuente entre los anuncios con precio en USD?**")
    L.append("")
    L.append(f"> El rango **{rango_top[0]} USD** es el más frecuente, con **{rango_top[1]} anuncios ({100*rango_top[1]/n_usd:.1f}% de los {n_usd} con precio en USD)**.")
    L.append("")
    L.append("> Distribución completa:")
    L.append(">")
    for lo, hi, etiqueta in bins:
        count = rangos.get(etiqueta, 0)
        if count:
            L.append(f"> - {etiqueta}: {count} anuncios ({100*count/n_usd:.1f}%)")
    L.append("")
    L.append("**29. ¿Cuántos anuncios parecen de particulares frente a posibles anuncios repetidos o agencias?**")
    L.append("")
    L.append(f"> La base no incluye un campo de vendedor que permita distinguir particulares de agencias. Como aproximación, **{titulos_unicos} de {total} títulos son únicos** y no hay títulos duplicados. La ausencia de duplicados exactos no muestra indicios de publicación masiva, pero tampoco descarta que una misma agencia use títulos distintos.")
    L.append("")
    L.append("**30. ¿Qué recomendación práctica se puede hacer a alguien que quiera comprar o alquilar en Diez de Octubre?**")
    L.append("")
    L.append(f"> 1. **Presupuesto:** la mediana de los anuncios con precio en USD es **${fmt(mediana)} USD** (en ventas explícitas con precio en USD, **${fmt(mediana_ventas)} USD**) y el 80% central de los precios está entre **${fmt(p10)} y ${fmt(p90)} USD**. El tramo más frecuente es **{rango_top[0]} USD** ({rango_top[1]} anuncios, {100*rango_top[1]/n_usd:.1f}%).")
    L.append(f"> 2. **Tipo de inmueble:** un apartamento promedia **${fmt(sum(precios_tipo['Apartamento'])/len(precios_tipo['Apartamento']))} USD** (n = {len(precios_tipo['Apartamento'])}) y una casa **${fmt(sum(precios_tipo['Casa'])/len(precios_tipo['Casa']))} USD** (n = {len(precios_tipo['Casa'])}); el apartamento es la opción más económica.")
    top3 = zonas.most_common(3)
    L.append(f"> 3. **Zonas:** {top3[0][0]} concentra la mayor oferta ({top3[0][1]} anuncios), seguida por {top3[1][0]} ({top3[1][1]}) y {top3[2][0]} ({top3[2][1]}). El promedio más alto entre zonas con al menos 5 anuncios con precio es {zona_cara} (**${fmt(prom_zona_cara)} USD**, n = {len(zonas_5[zona_cara])}), mientras que {zona_barata} (**${fmt(prom_zona_barata)} USD**, n = {len(zonas_5[zona_barata])}) es la alternativa más económica de ese grupo.")
    L.append(f"> 4. **Moneda:** el mercado está dolarizado: **{len(usd)} de {len(con_moneda)} anuncios con moneda declarada ({100*len(usd)/len(con_moneda):.1f}%)** usan USD. Hay que contar con divisas o verificar el tipo de cambio si se paga en CUP.")
    L.append(f"> 5. **Información incompleta:** **{len(sin_precio)} anuncios ({100*len(sin_precio)/total:.1f}%)** no declaran precio y **{sin_zona} ({100*sin_zona/total:.1f}%)** no especifican zona. Verifique siempre precio, ubicación y estado legal directamente con el vendedor.")
    L.append("> 6. **Precaución estadística:** los promedios por zona y por características se basan en subgrupos pequeños; úselos como orientación, no como precio de referencia definitivo.")
    L.append("")

    # ---------------- CONCLUSIONES ----------------
    L.append("## Conclusiones")
    L.append("")
    L.append(f"1. El mercado está dolarizado: {len(usd)} de {len(con_moneda)} anuncios con moneda declarada ({100*len(usd)/len(con_moneda):.1f}%) están en USD.")
    L.append(f"2. Los precios están sesgados a la derecha: la media (${fmt(promedio)}) supera a la mediana (${fmt(mediana)}) y {fuera_rango} anuncios ({100*fuera_rango/n_usd:.1f}%) quedan fuera del tramo P10–P90.")
    L.append(f"3. Las casas son el tipo más publicado ({casas} anuncios, {100*casas/total:.1f}%). Entre casa y apartamento, la casa es más cara en promedio (${fmt(sum(precios_tipo['Casa'])/len(precios_tipo['Casa']))} USD) que el apartamento (${fmt(sum(precios_tipo['Apartamento'])/len(precios_tipo['Apartamento']))} USD).")
    L.append(f"4. La oferta se concentra en pocas zonas: las cuatro principales reúnen {pct_top4:.1f}% de los anuncios con zona identificada.")
    L.append(f"5. Existen diferencias de precio entre zonas: {zona_cara} promedia ${fmt(prom_zona_cara)} USD y {zona_barata} ${fmt(prom_zona_barata)} USD (zonas con al menos 5 anuncios con precio).")
    L.append(f"6. La información está incompleta: {len(sin_precio)} anuncios ({100*len(sin_precio)/total:.1f}%) no declaran precio y {sin_zona} ({100*sin_zona/total:.1f}%) no especifican zona.")
    L.append("")
    L.append("## Limitaciones")
    L.append("")
    L.append("- Los datos provienen solo de Revolico; no representan todo el mercado inmobiliario de Diez de Octubre.")
    L.append("- Se exploró Facebook (37 publicaciones), pero se excluyó del análisis cuantitativo porque no comparte el esquema de campos de Revolico ni un municipio normalizado; integrarla exigiría una normalización y un filtro municipal adicionales.")
    L.append("- La muestra es de 171 anuncios y puede no ser representativa del mercado completo.")
    L.append("- La clasificación de tipo, zona y características depende de palabras clave y puede contener errores.")
    L.append("- Los precios de alquiler no se pudieron analizar: solo 1 anuncio de alquiler declara precio en USD y 1 en CUP.")
    L.append("- Los subgrupos por zona, garaje, planta baja y número de cuartos tienen tamaños pequeños; sus promedios son descriptivos.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("Informe generado por el Proyecto de Ciencia de Datos — Universidad de La Habana")
    L.append("")
    L.append("Facultad de Matemática y Computación (MATCOM)")
    L.append("")
    L.append("Profesor: Yudivian Almeida Cruz")
    L.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print(f"Informe guardado en: {OUTPUT_FILE}")
    print(f"Anuncios: {total} | USD: {n_usd} | Media: {fmt(promedio)} | Mediana: {fmt(mediana)}")
    print(f"P10-P90: {fmt(p10)} - {fmt(p90)} | En rango: {len(en_rango)}")


if __name__ == "__main__":
    main()
