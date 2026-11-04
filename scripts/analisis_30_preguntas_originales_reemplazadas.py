#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la versión revisada del cuestionario de 30 preguntas.

Base de datos:
    datos/brutos/revolico_crudos_limpio_final.json
    134 anuncios estrictos de Diez de Octubre (precio >= 1,000 USD cuando
    existe precio).

Qué hace este script:
    - Conserva 20 preguntas del cuestionario original.
    - Reemplaza 10 preguntas que no tenían respaldo suficiente:
      Q10, Q12, Q13, Q14, Q15, Q16, Q20, Q22, Q26 y Q29.
    - Responde las 30 preguntas sobre la base corregida de 134 anuncios.
    - Reporta n, nivel de evidencia y la ausencia de datos como hallazgo.

Salida:
    analisis/informe_30_preguntas_originales_reemplazadas.md
"""

import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# Reutiliza las funciones de clasificación y estadística del generador canónico.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import analisis_final_30_preguntas as base  # noqa: E402

INPUT_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
REJECTED_FILE = "datos/limpios/anuncios_eliminados_por_filtro_final.json"
OUTPUT_FILE = "analisis/informe_30_preguntas_originales_reemplazadas.md"

# Preguntas del cuestionario original que se conservan y que se reemplazan.
CONSERVADAS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 17, 18, 19, 21, 23, 24, 25, 27, 28, 30]
REEMPLAZADAS = [10, 12, 13, 14, 15, 16, 20, 22, 26, 29]

# Conteo de cuartos explícitos (solo para justificar la sustitución de Q13/Q14).
PATRON_CUARTOS = re.compile(
    r"(?:\b\d+\b|\b(?:un|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\b)"
    r"\s*(?:cuartos?|habitaciones?|hab\.?)",
    re.IGNORECASE,
)


def fmt(valor):
    return base.fmt(valor)


def pct(n, d):
    return base.pct(n, d)


def unidad(n):
    return base.unidad(n)


def add_q(L, numero, texto, evidencia, lineas):
    """Agrega una pregunta numerada y su respuesta en blockquote."""
    L.append(f"**{numero}. {texto}** {evidencia}")
    L.append("")
    for linea in lineas:
        L.append(f"> {linea}" if linea else ">")
    L.append("")


def main():
    anuncios = base.cargar_json(INPUT_FILE)
    total = len(anuncios)

    for a in anuncios:
        a["_tipo"] = base.clasificar_tipo(a.get("titulo"))
        a["_zona"] = base.clasificar_zona(a.get("titulo"), a.get("enlace"))
        a["_op"] = base.clasificar_operacion(a.get("titulo"))

    con_precio = [a for a in anuncios if a.get("precio") is not None]
    sin_precio = [a for a in anuncios if a.get("precio") is None]
    usd = [a for a in anuncios if a.get("precio") is not None
           and str(a.get("moneda", "")).upper() == "USD"]
    cup = [a for a in anuncios if str(a.get("moneda", "")).upper() == "CUP"]
    con_moneda = [a for a in anuncios
                  if str(a.get("moneda", "")).upper() in ("USD", "CUP")]

    ventas = [a for a in anuncios if a["_op"] == "Venta"]
    alquileres = [a for a in anuncios if a["_op"] == "Alquiler"]
    sin_clasificar = [a for a in anuncios if a["_op"] == "Sin clasificar"]

    ventas_con_precio = [a for a in ventas if a.get("precio") is not None]
    ventas_usd = [a for a in ventas if a.get("precio") is not None
                  and str(a.get("moneda", "")).upper() == "USD"]
    alquileres_con_precio = [a for a in alquileres if a.get("precio") is not None]

    stats_usd = base.stats([a["precio"] for a in usd])
    stats_venta = base.stats([a["precio"] for a in ventas_usd])

    # Zonas
    zonas = Counter(a["_zona"] for a in anuncios if a["_zona"] != "No especificado")
    total_con_zona = sum(zonas.values())
    sin_zona_n = total - total_con_zona
    top4 = zonas.most_common(4)
    top4_total = sum(c for _, c in top4)

    precios_zona = defaultdict(list)
    for a in usd:
        if a["_zona"] != "No especificado":
            precios_zona[a["_zona"]].append(a["precio"])
    zonas_5 = {z: v for z, v in precios_zona.items() if len(v) >= 5}
    stats_zona_5 = {z: base.stats(v) for z, v in zonas_5.items()}
    zona_cara_5 = max(zonas_5, key=lambda z: stats_zona_5[z]["mean"])

    # Tipos
    tipos = Counter(a["_tipo"] for a in anuncios)
    precios_tipo = defaultdict(list)
    for a in usd:
        precios_tipo[a["_tipo"]].append(a["precio"])
    stats_tipo = {t: base.stats(v) for t, v in precios_tipo.items()}

    # Opacidad
    sin_precio_n = len(sin_precio)
    completo_n = sum(1 for a in anuncios
                     if a.get("precio") is not None and a["_zona"] != "No especificado")
    ambos_faltan_n = sum(1 for a in anuncios
                         if a.get("precio") is None and a["_zona"] == "No especificado")
    totalmente_opacos = [
        a for a in anuncios
        if a.get("precio") is None
        and a["_zona"] == "No especificado"
        and not base.tiene_feature(a.get("titulo"))
    ]
    con_zona = [a for a in anuncios if a["_zona"] != "No especificado"]
    sin_zona = [a for a in anuncios if a["_zona"] == "No especificado"]
    con_zona_con_precio = sum(1 for a in con_zona if a.get("precio") is not None)
    sin_zona_con_precio = sum(1 for a in sin_zona if a.get("precio") is not None)

    # Informalidad
    informal = [
        a for a in anuncios
        if any(p in (a.get("titulo") or "").lower() for p in base.PALABRAS_INFORMALES)
    ]
    neutros = [a for a in anuncios if a not in informal]
    informal_por_op = Counter(a["_op"] for a in informal)
    palabras_inf = Counter(
        p for a in anuncios for p in base.PALABRAS_INFORMALES
        if p in (a.get("titulo") or "").lower()
    )

    # Características físicas agrupadas
    grupos_features = [
        ("Habitación/cuarto", ["habitacion", "habitación", "cuarto"]),
        ("Garaje", ["garaje", "garage"]),
        ("Baño", ["baño", "bano"]),
        ("Balcón", ["balcón", "balcon"]),
        ("Terraza", ["terraza"]),
        ("Azotea", ["azotea"]),
        ("Patio", ["patio"]),
    ]
    conteo_features = {}
    for nombre, claves in grupos_features:
        conteo_features[nombre] = sum(
            1 for a in anuncios
            if any(k in (a.get("titulo") or "").lower() for k in claves)
        )
    con_feature = [a for a in anuncios if base.tiene_feature(a.get("titulo"))]

    # Rangos de precio
    rangos = [
        (0, 10000, "0 – 10,000"),
        (10000, 20000, "10,000 – 20,000"),
        (20000, 30000, "20,000 – 30,000"),
        (30000, 40000, "30,000 – 40,000"),
        (40000, 50000, "40,000 – 50,000"),
        (50000, 60000, "50,000 – 60,000"),
        (60000, 70000, "60,000 – 70,000"),
        (70000, 80000, "70,000 – 80,000"),
        (80000, 10**9, "80,000 y más"),
    ]
    conteo_rangos = []
    for lo, hi, etiqueta in rangos:
        c = sum(1 for a in usd if lo <= a["precio"] < hi)
        conteo_rangos.append((etiqueta, c))

    # P10–P90 y media recortada
    dentro_p10_p90 = [
        a for a in usd if stats_usd["p10"] <= a["precio"] <= stats_usd["p90"]
    ]
    bajo_p10 = [a for a in usd if a["precio"] < stats_usd["p10"]]
    sobre_p90 = [a for a in usd if a["precio"] > stats_usd["p90"]]
    valores_ordenados = sorted(a["precio"] for a in usd)
    k_recorte = int(len(valores_ordenados) * 0.10)
    valores_recortados = valores_ordenados[k_recorte:len(valores_ordenados) - k_recorte]
    media_recortada = sum(valores_recortados) / len(valores_recortados)
    diferencia_recorte = stats_usd["mean"] - media_recortada

    # Cuartos explícitos (para justificar Q13 y Q14)
    cuartos_detectados = []
    for a in anuncios:
        if PATRON_CUARTOS.search(a.get("titulo") or ""):
            cuartos_detectados.append(a)
    cuartos_con_precio_usd = [
        a for a in cuartos_detectados
        if a.get("precio") is not None and str(a.get("moneda", "")).upper() == "USD"
    ]

    # Rechazos del filtro
    rechazados = []
    if os.path.exists(REJECTED_FILE):
        rechazados = base.cargar_json(REJECTED_FILE)
    motivos = Counter(r.get("motivo_eliminacion") for r in rechazados)
    rechazados_municipio = motivos.get("MUNICIPIO_DISTINTO_A_DIEZ_DE_OCTUBRE", 0)
    rechazados_precio = len(rechazados) - rechazados_municipio

    # Fecha de corte
    fechas = Counter(
        (a.get("fecha_verificacion") or "")[:10] for a in anuncios
        if a.get("fecha_verificacion")
    )
    fecha_corte = fechas.most_common(1)[0][0] if fechas else "no disponible"

    L = []

    # ------------------------------------------------------------------
    # Portada y resumen
    # ------------------------------------------------------------------
    L.append("# Mercado inmobiliario digital en Diez de Octubre")
    L.append("## Versión revisada: 30 preguntas originales con 10 reemplazos")
    L.append("")
    L.append(f"**Fecha de generación:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    L.append(f"**Corte de los datos:** {fecha_corte}")
    L.append("**Fuente:** Revolico (anuncios activos)")
    L.append(f"**Universo estricto:** {total} anuncios de Diez de Octubre")
    L.append(f"**Anuncios con precio en USD:** {len(usd)}")
    L.append("")

    L.append("## Qué cambia en esta versión")
    L.append("")
    L.append(
        "Este informe parte del cuestionario original de 30 preguntas. Se "
        "**conservan 20 preguntas** y se **reemplazan 10** que no alcanzaban un "
        "respaldo suficiente: dependían de uno o pocos anuncios, de un campo que "
        "no existe en la base o de una comparación entre subgrupos demasiado "
        "pequeños. Los reemplazos no inventan datos: convierten esa debilidad en "
        "preguntas respondibles y, en varios casos, en mediciones explícitas de "
        "la ausencia de información."
    )
    L.append("")
    L.append(
        f"La base usada es la corregida de **{total} anuncios estrictamente de "
        f"Diez de Octubre**. La fuente completa tiene 270 anuncios; el filtro "
        f"descartó {len(rechazados)}: {rechazados_municipio} por mencionar otro "
        f"municipio o localidad y {rechazados_precio} por precio inferior a "
        f"1,000 USD. Las cifras de la versión anterior sobre 171 anuncios no se "
        f"reutilizan porque incluían anuncios de otros municipios."
    )
    L.append("")

    L.append("## Resumen ejecutivo")
    L.append("")
    L.append(
        f"- **Dolarización:** {len(usd)} de {len(con_moneda)} anuncios con moneda "
        f"declarada están en USD (**{pct(len(usd), len(con_moneda)):.1f}%**), y "
        f"{len(usd)} de {total} del total (**{pct(len(usd), total):.1f}%**)."
    )
    L.append(
        f"- **Precios:** media **${fmt(stats_usd['mean'])} USD** y mediana "
        f"**${fmt(stats_usd['median'])} USD** (n = {stats_usd['n']}). El 80% "
        f"central está entre **${fmt(stats_usd['p10'])}** y "
        f"**${fmt(stats_usd['p90'])} USD**."
    )
    L.append(
        f"- **Precios de compra:** en las {stats_venta['n']} ventas explícitas con "
        f"precio USD, media **${fmt(stats_venta['mean'])} USD**, mediana "
        f"**${fmt(stats_venta['median'])} USD** y P10–P90 "
        f"**${fmt(stats_venta['p10'])}–${fmt(stats_venta['p90'])} USD**."
    )
    L.append(
        f"- **Alquiler:** {len(alquileres_con_precio)} de {len(alquileres)} "
        f"alquileres declara precio y **ninguno lo hace en USD**; el precio de "
        f"alquiler no es estimable con esta base."
    )
    L.append(
        f"- **Opacidad:** {sin_precio_n} de {total} anuncios "
        f"({pct(sin_precio_n, total):.1f}%) no declaran precio; {sin_zona_n} "
        f"({pct(sin_zona_n, total):.1f}%) no especifican zona; solo "
        f"{completo_n} ({pct(completo_n, total):.1f}%) permiten cruzar precio y "
        f"zona."
    )
    L.append(
        f"- **Desigualdad territorial:** las cuatro zonas principales concentran "
        f"{top4_total} de {total_con_zona} anuncios con zona identificada "
        f"({pct(top4_total, total_con_zona):.1f}%). La Víbora tiene la media más "
        f"alta (${fmt(stats_zona_5[zona_cara_5]['mean'])} USD, n = "
        f"{stats_zona_5[zona_cara_5]['n']}), pero su mediana es "
        f"${fmt(stats_zona_5[zona_cara_5]['median'])} USD."
    )
    L.append(
        f"- **Informalidad:** {len(informal)} de {total} anuncios "
        f"({pct(len(informal), total):.1f}%) usan lenguaje de oportunidad, "
        f"permuta o cambio. Se concentran en venta y en anuncios sin operación "
        f"declarada; no aparecen en alquiler."
    )
    L.append(
        f"- **Tipo de inmueble:** el apartamento es la opción más accesible: "
        f"mediana **${fmt(stats_tipo['Apartamento']['median'])} USD** (n = "
        f"{stats_tipo['Apartamento']['n']}) frente a la casa, con mediana "
        f"**${fmt(stats_tipo['Casa']['median'])} USD** (n = "
        f"{stats_tipo['Casa']['n']})."
    )
    L.append("")
    L.append(
        "La ausencia de datos se mide como un rasgo del mercado. Un anuncio sin "
        "precio, sin zona o sin operación limita la capacidad de comparar y de "
        "verificar; esa limitación es parte del problema social que el estudio "
        "documenta."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Metodología
    # ------------------------------------------------------------------
    L.append("## Metodología")
    L.append("")
    L.append(
        "- **Fuente:** Revolico, única fuente usada en los cálculos. Se analizan "
        f"los anuncios activos de Diez de Octubre con corte al {fecha_corte}."
    )
    L.append(
        "- **Universo:** 134 anuncios estrictos. El filtro revisa título y enlace "
        "porque el campo `municipio` del scraper no es fiable: todos los anuncios "
        "aparecen como «Diez de Octubre» aunque el título diga otro municipio."
    )
    L.append(
        f"- **Precios:** se analizan los {len(usd)} anuncios con precio en USD. "
        f"Se excluye 1 anuncio en CUP y {sin_precio_n} sin precio. Se reportan "
        f"media, mediana, P10–P90 y media recortada para reducir el efecto de "
        f"los valores extremos."
    )
    L.append(
        "- **Clasificación:** tipo, zona y operación se infieren de palabras "
        "clave del título y del enlace. Es reproducible, pero puede contener "
        "errores de asignación."
    )
    L.append(
        "- **Ausencia:** un anuncio sin precio, zona u operación no se elimina. "
        "Se conserva y se contabiliza como indicador de opacidad."
    )
    L.append("")
    L.append("### Niveles de evidencia")
    L.append("")
    L.append(
        "- ✅ **Sólida:** n ≥ 30 o censo completo del subgrupo.\n"
        "- 🟡 **Descriptiva:** n = 5–29; el resultado orienta, pero no se "
        "generaliza.\n"
        "- 🔴 **No estimable:** la ausencia de datos es el hallazgo."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Tabla de sustitución
    # ------------------------------------------------------------------
    L.append("## Las 10 preguntas reemplazadas")
    L.append("")
    L.append(
        "La siguiente tabla documenta qué pregunta se retiró, por qué no tenía "
        "respaldo suficiente y qué pregunta la sustituye. Las 20 restantes se "
        "conservan con su redacción original."
    )
    L.append("")
    L.append("| # | Pregunta original | Por qué no alcanza | Pregunta de reemplazo |")
    L.append("|---|---|---|---|")
    sustituciones = [
        (
            10,
            "¿Qué tipo de inmueble concentra el precio máximo declarado?",
            "La respuesta depende de un solo anuncio (el máximo de $180,000). "
            "No describe un tipo de inmueble: describe un caso.",
            "¿Cuál es la mediana del precio en USD por tipo de inmueble?",
        ),
        (
            12,
            "¿Qué tipo de inmueble domina en la zona con el precio promedio más alto?",
            "La zona con la media más alta (La Víbora) solo tiene 9 anuncios con "
            "precio; 6 son apartamentos. n = 9.",
            "¿La declaración de precio depende de que el anuncio identifique zona?",
        ),
        (
            13,
            "¿Cuál es la cantidad más común de cuartos/habitaciones?",
            f"Solo {len(cuartos_detectados)} anuncios permiten extraer un número "
            f"explícito de cuartos. n = {len(cuartos_detectados)}.",
            "¿Qué proporción de anuncios es totalmente opaca (sin precio, zona "
            "ni característica)?",
        ),
        (
            14,
            "¿Cómo varía el precio según el número de cuartos?",
            f"Solo {len(cuartos_con_precio_usd)} anuncios combinan número de "
            f"cuartos y precio en USD. n = {len(cuartos_con_precio_usd)}.",
            "¿Qué proporción de anuncios ofrece información completa (precio y "
            "zona)?",
        ),
        (
            15,
            "¿Qué porcentaje de anuncios menciona garaje y cómo se relaciona con "
            "el precio?",
            f"Solo {conteo_features['Garaje']} anuncios mencionan garaje. "
            f"n = {conteo_features['Garaje']}.",
            "¿La opacidad de precio y zona es mayor en alquiler o en venta?",
        ),
        (
            16,
            "¿Cuántos anuncios especifican 'planta baja' y cuál es su precio "
            "promedio?",
            "Solo 8 anuncios mencionan planta baja o bajos. n = 8.",
            "¿Qué tipo de inmueble presenta mayor opacidad de precio y zona?",
        ),
        (
            20,
            "¿Qué zona tiene el precio promedio más alto entre los anuncios con "
            "precio en USD?",
            "La zona con la media más alta (La Víbora) solo tiene 9 anuncios con "
            "precio y su media está inflada por un valor extremo de $180,000. "
            "n = 9.",
            "¿Qué porcentaje de anuncios con precio USD queda dentro del tramo "
            "P10–P90?",
        ),
        (
            22,
            "¿Hay diferencia de precios entre zonas dentro del mismo municipio?",
            "La diferencia se apoya en los mismos grupos pequeños (n = 9 y "
            "n = 10) y en una media sensible a valores extremos.",
            "¿Cuánto cambia el precio promedio al recortar 10% de cada cola?",
        ),
        (
            26,
            "¿Los anuncios con lenguaje informal declaran precio con más "
            "frecuencia que los neutros?",
            f"Solo {len(informal)} anuncios usan lenguaje informal; la "
            f"comparación es descriptiva. n = {len(informal)}.",
            "¿Cómo se distribuye la informalidad según el tipo de operación?",
        ),
        (
            29,
            "¿Cuántos anuncios parecen de particulares frente a posibles anuncios "
            "repetidos o agencias?",
            "La base no tiene campo de vendedor ni de agencia; los títulos únicos "
            "no permiten distinguir unos de otros.",
            "¿Qué proporción de anuncios no declara operación y cómo se "
            "distribuye por tipo de inmueble?",
        ),
    ]
    for numero, original, motivo, nueva in sustituciones:
        L.append(f"| {numero} | {original} | {motivo} | {nueva} |")
    L.append("")
    L.append(
        "Las 20 preguntas conservadas son: "
        + ", ".join(f"Q{n}" for n in CONSERVADAS)
        + ". Las 10 reemplazadas son: "
        + ", ".join(f"Q{n}" for n in REEMPLAZADAS)
        + "."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Preguntas y respuestas
    # ------------------------------------------------------------------
    L.append("## Las 30 preguntas y sus respuestas")
    L.append("")

    # ---------------- BLOQUE A ----------------
    L.append("### Bloque A: Precios del mercado")
    L.append("")

    add_q(
        L, 1,
        "¿Cuál es el precio promedio de los anuncios con precio declarado en USD "
        "en Diez de Octubre?",
        f"✅ (n = {stats_usd['n']})",
        [
            f"**${fmt(stats_usd['mean'])} USD** entre los {stats_usd['n']} anuncios "
            f"con precio en USD. Si se restringe a las {stats_venta['n']} ventas "
            f"explícitas con precio en USD, la media baja a "
            f"**${fmt(stats_venta['mean'])} USD**: los anuncios sin operación "
            f"declarada incluyen inmuebles de mayor precio y elevan el promedio "
            f"general.",
            "",
            "La media no es el precio típico. La mediana (Q2) y la media recortada "
            "(Q22) son referencias más estables.",
        ],
    )

    add_q(
        L, 2,
        "¿Cuál es el precio mediano de los anuncios con precio declarado en USD?",
        f"✅ (n = {stats_usd['n']})",
        [
            f"**${fmt(stats_usd['median'])} USD** (n = {stats_usd['n']}). En las "
            f"{stats_venta['n']} ventas explícitas con precio USD, la mediana es "
            f"**${fmt(stats_venta['median'])} USD**.",
            "",
            "La mediana es menor que la media general porque unos pocos anuncios "
            "muy caros elevan el promedio. Para una persona que busca comprar, la "
            "mediana de ventas es la referencia más realista.",
        ],
    )

    add_q(
        L, 3,
        "¿Cuál es el rango de precios que cubre el 80% central de los anuncios?",
        f"✅ (n = {stats_usd['n']})",
        [
            f"Entre **${fmt(stats_usd['p10'])} USD** (P10) y "
            f"**${fmt(stats_usd['p90'])} USD** (P90). Dentro de ese tramo quedan "
            f"**{len(dentro_p10_p90)} de {stats_usd['n']} anuncios "
            f"({pct(len(dentro_p10_p90), stats_usd['n']):.1f}%)**.",
            "",
            f"El mínimo es **${fmt(stats_usd['min'])} USD** y el máximo "
            f"**${fmt(stats_usd['max'])} USD**. El rango central es amplio: la "
            f"diferencia entre P10 y P90 es de "
            f"**${fmt(stats_usd['p90'] - stats_usd['p10'])} USD**.",
        ],
    )

    add_q(
        L, 4,
        "¿Cuáles son el anuncio más caro y el más barato publicados?",
        f"✅ (n = {stats_usd['n']})",
        [
            f"- Más caro: **${fmt(stats_usd['max'])} USD**, clasificado como "
            f"Inmueble («180,000 USD Cada en la víbora 10 octubre»).",
            f"- Más barato: **${fmt(stats_usd['min'])} USD**.",
            "",
            "El segundo precio más alto es **$120,000.00 USD**. El máximo de "
            "$180,000 es un valor atípico que conviene tratar por separado: "
            "eleva la media y no representa al conjunto.",
        ],
    )

    add_q(
        L, 5,
        "¿Qué proporción de anuncios no declara precio?",
        f"✅ (n = {total})",
        [
            f"**{sin_precio_n} de {total} anuncios "
            f"({pct(sin_precio_n, total):.1f}%)** no declaran precio. Los otros "
            f"{len(con_precio)} sí lo hacen: {len(usd)} en USD y {len(cup)} en CUP.",
            "",
            "No declarar precio obliga a contactar al vendedor y reduce la "
            "posibilidad de comparar. Es un indicador de opacidad, no un dato "
            "perdido.",
        ],
    )

    add_q(
        L, 6,
        "¿Qué tan dispersos son los precios respecto a la media?",
        f"✅ (n = {stats_usd['n']})",
        [
            f"La media (${fmt(stats_usd['mean'])}) supera a la mediana "
            f"(${fmt(stats_usd['median'])}) en "
            f"**${fmt(stats_usd['mean'] - stats_usd['median'])}**, un "
            f"**{pct(stats_usd['mean'] - stats_usd['median'], stats_usd['median']):.1f}%** "
            f"de la mediana.",
            "",
            f"Además, **{len(bajo_p10) + len(sobre_p90)} de {stats_usd['n']} "
            f"anuncios ({pct(len(bajo_p10) + len(sobre_p90), stats_usd['n']):.1f}%)** "
            f"quedan fuera del tramo P10–P90: {len(bajo_p10)} por debajo de P10 y "
            f"{len(sobre_p90)} por encima de P90. La distribución está sesgada a "
            f"la derecha: una minoría de inmuebles muy caros infla el promedio.",
        ],
    )

    # ---------------- BLOQUE B ----------------
    L.append("### Bloque B: Tipos de inmueble")
    L.append("")

    add_q(
        L, 7,
        "¿Cuáles son los tipos de inmueble más publicados?",
        f"✅ (n = {total})",
        [
            f"- Casa: **{tipos['Casa']} anuncios "
            f"({pct(tipos['Casa'], total):.1f}%)**",
            f"- Apartamento: **{tipos['Apartamento']} anuncios "
            f"({pct(tipos['Apartamento'], total):.1f}%)**",
            f"- Inmueble: **{tipos['Inmueble']} anuncios "
            f"({pct(tipos['Inmueble'], total):.1f}%)**",
            f"- Cuarto: **{tipos['Cuarto']} anuncios "
            f"({pct(tipos['Cuarto'], total):.1f}%)**",
            "",
            "«Inmueble» agrupa los títulos que no especifican un tipo. No es una "
            "categoría física homogénea, sino un residual de clasificación.",
        ],
    )

    add_q(
        L, 8,
        "¿Qué porcentaje son casas independientes frente a apartamentos?",
        f"✅ (n = {tipos['Casa'] + tipos['Apartamento']})",
        [
            f"- Casas: **{tipos['Casa']} de {tipos['Casa'] + tipos['Apartamento']} "
            f"({pct(tipos['Casa'], tipos['Casa'] + tipos['Apartamento']):.1f}%)**",
            f"- Apartamentos: **{tipos['Apartamento']} de "
            f"{tipos['Casa'] + tipos['Apartamento']} "
            f"({pct(tipos['Apartamento'], tipos['Casa'] + tipos['Apartamento']):.1f}%)**",
            "",
            "Entre los anuncios con tipo identificable como casa o apartamento, "
            "la casa es mayoría. El resto de los anuncios queda en «Inmueble» o "
            "«Cuarto» y no entra en esta comparación.",
        ],
    )

    add_q(
        L, 9,
        "¿Cuál es el precio promedio por tipo de inmueble (anuncios con precio en "
        "USD)?",
        f"✅ (n = {stats_usd['n']})",
        [
            f"- Casa: **${fmt(stats_tipo['Casa']['mean'])} USD** "
            f"(n = {stats_tipo['Casa']['n']})",
            f"- Apartamento: **${fmt(stats_tipo['Apartamento']['mean'])} USD** "
            f"(n = {stats_tipo['Apartamento']['n']})",
            f"- Inmueble: **${fmt(stats_tipo['Inmueble']['mean'])} USD** "
            f"(n = {stats_tipo['Inmueble']['n']})",
            f"- Cuarto: **${fmt(stats_tipo['Cuarto']['mean'])} USD** "
            f"(n = {stats_tipo['Cuarto']['n']})",
            "",
            "El apartamento tiene el promedio más bajo. El Cuarto solo tiene un "
            "anuncio con precio: su promedio no se usa para comparar. La media de "
            "Inmueble está afectada por el máximo de $180,000; por eso la Q10 "
            "reporta medianas.",
        ],
    )

    add_q(
        L, 10,
        "¿Cuál es la mediana del precio en USD por tipo de inmueble?",
        f"✅ (n = {stats_usd['n']})",
        [
            f"- Apartamento: **${fmt(stats_tipo['Apartamento']['median'])} USD** "
            f"(n = {stats_tipo['Apartamento']['n']})",
            f"- Casa: **${fmt(stats_tipo['Casa']['median'])} USD** "
            f"(n = {stats_tipo['Casa']['n']})",
            f"- Inmueble: **${fmt(stats_tipo['Inmueble']['median'])} USD** "
            f"(n = {stats_tipo['Inmueble']['n']})",
            f"- Cuarto: **${fmt(stats_tipo['Cuarto']['median'])} USD** "
            f"(n = {stats_tipo['Cuarto']['n']})",
            "",
            "La mediana confirma el orden de accesibilidad: el apartamento es la "
            "opción más barata (mediana $15,000) y la casa cuesta el doble en "
            "términos medianos ($30,000). El Inmueble tiene la mediana más alta "
            "($35,500), pero es una categoría residual y su media está inflada "
            "por un valor extremo. El Cuarto no se compara: n = 1.",
            "",
            "Esta pregunta sustituye a la original sobre el tipo que concentra el "
            "precio máximo, que dependía de un solo anuncio.",
        ],
    )

    add_q(
        L, 11,
        "¿Cuántos anuncios se identifican como venta, alquiler o sin clasificar?",
        f"✅ (n = {total})",
        [
            f"- Venta: **{len(ventas)} anuncios "
            f"({pct(len(ventas), total):.1f}%)**",
            f"- Alquiler: **{len(alquileres)} anuncios "
            f"({pct(len(alquileres), total):.1f}%)**",
            f"- Sin clasificar: **{len(sin_clasificar)} anuncios "
            f"({pct(len(sin_clasificar), total):.1f}%)**",
            "",
            f"De las {len(ventas)} ventas, {len(ventas_con_precio)} "
            f"({pct(len(ventas_con_precio), len(ventas)):.1f}%) declaran precio. "
            f"De los {len(alquileres)} alquileres, solo "
            f"{len(alquileres_con_precio)} "
            f"({pct(len(alquileres_con_precio), len(alquileres)):.1f}%) lo hace, y "
            f"en CUP; ningún alquiler declara precio en USD. La operación no "
            f"declarada es la categoría más frecuente.",
        ],
    )

    add_q(
        L, 12,
        "¿La declaración de precio depende de que el anuncio identifique zona?",
        f"✅ (n = {total})",
        [
            f"- Con zona identificada: **{con_zona_con_precio} de {len(con_zona)} "
            f"({pct(con_zona_con_precio, len(con_zona)):.1f}%)** declaran precio.",
            f"- Sin zona identificada: **{sin_zona_con_precio} de {len(sin_zona)} "
            f"({pct(sin_zona_con_precio, len(sin_zona)):.1f}%)** declaran precio.",
            "",
            f"La diferencia es de **{pct(con_zona_con_precio, len(con_zona)) - pct(sin_zona_con_precio, len(sin_zona)):.1f} puntos porcentuales** "
            f"a favor de los anuncios con zona. No implica causalidad: ambos "
            f"grupos declaran precio en una proporción alta. Lo que muestra es que "
            f"la falta de zona no impide conocer el precio, pero sí reduce algo la "
            f"transparencia.",
            "",
            "Esta pregunta sustituye a la original sobre el tipo dominante en la "
            "zona más cara, que se apoyaba en 9 anuncios.",
        ],
    )

    # ---------------- BLOQUE C ----------------
    L.append("### Bloque C: Características físicas y opacidad")
    L.append("")

    add_q(
        L, 13,
        "¿Qué proporción de anuncios es totalmente opaca (sin precio, zona ni "
        "característica)?",
        f"✅ (n = {total})",
        [
            f"**{len(totalmente_opacos)} de {total} anuncios "
            f"({pct(len(totalmente_opacos), total):.1f}%)** no declaran precio, "
            f"no especifican zona y no mencionan ninguna característica física "
            f"(garaje, patio, azotea, terraza, balcón, baño, cuarto o habitación).",
            "",
            f"Otros {ambos_faltan_n} anuncios ({pct(ambos_faltan_n, total):.1f}%) "
            f"carecen de precio y zona, pero {ambos_faltan_n - len(totalmente_opacos)} "
            f"de ellos mencionan al menos una característica. La opacidad total es "
            f"minoritaria, pero existe: son anuncios que solo ofrecen un título y "
            f"un contacto.",
            "",
            "Esta pregunta sustituye a la original sobre la cantidad más común de "
            "cuartos, que solo podía calcularse en "
            f"{len(cuartos_detectados)} anuncios.",
        ],
    )

    add_q(
        L, 14,
        "¿Qué proporción de anuncios ofrece información completa (precio y zona)?",
        f"✅ (n = {total})",
        [
            f"**{completo_n} de {total} anuncios "
            f"({pct(completo_n, total):.1f}%)** declaran precio y especifican "
            f"zona. Es decir, menos de 4 de cada 10 anuncios permiten cruzar "
            f"precio y ubicación.",
            "",
            f"De los {len(con_precio)} anuncios con precio, {completo_n} "
            f"({pct(completo_n, len(con_precio)):.1f}%) también identifican zona. "
            f"De los {len(con_zona)} con zona, {completo_n} "
            f"({pct(completo_n, len(con_zona)):.1f}%) también declaran precio.",
            "",
            "Esta pregunta sustituye a la original sobre la variación del precio "
            "según el número de cuartos, que solo tenía "
            f"{len(cuartos_con_precio_usd)} casos con precio.",
        ],
    )

    add_q(
        L, 15,
        "¿La opacidad de precio y zona es mayor en alquiler o en venta?",
        f"🟡 (censo de {len(alquileres)} alquileres y {len(ventas)} ventas)",
        [
            f"- Venta (n = {len(ventas)}): "
            f"{sum(1 for a in ventas if a.get('precio') is None)} sin precio "
            f"({pct(sum(1 for a in ventas if a.get('precio') is None), len(ventas)):.1f}%); "
            f"{sum(1 for a in ventas if a['_zona'] == 'No especificado')} sin zona "
            f"({pct(sum(1 for a in ventas if a['_zona'] == 'No especificado'), len(ventas)):.1f}%).",
            f"- Alquiler (n = {len(alquileres)}): "
            f"{sum(1 for a in alquileres if a.get('precio') is None)} sin precio "
            f"({pct(sum(1 for a in alquileres if a.get('precio') is None), len(alquileres)):.1f}%); "
            f"{sum(1 for a in alquileres if a['_zona'] == 'No especificado')} sin zona "
            f"({pct(sum(1 for a in alquileres if a['_zona'] == 'No especificado'), len(alquileres)):.1f}%).",
            f"- Sin clasificar (n = {len(sin_clasificar)}): "
            f"{sum(1 for a in sin_clasificar if a.get('precio') is None)} sin precio "
            f"({pct(sum(1 for a in sin_clasificar if a.get('precio') is None), len(sin_clasificar)):.1f}%); "
            f"{sum(1 for a in sin_clasificar if a['_zona'] == 'No especificado')} sin zona "
            f"({pct(sum(1 for a in sin_clasificar if a['_zona'] == 'No especificado'), len(sin_clasificar)):.1f}%).",
            "",
            "El alquiler es mucho más opaco: **8 de 9 alquileres (88.9%)** no "
            "declaran precio y **8 de 9 (88.9%)** no especifican zona. En venta, "
            "la falta de precio es menor (**6 de 52, 11.5%**), aunque la falta de "
            "zona sigue siendo alta (**34 de 52, 65.4%**).",
            "",
            "La diferencia es consistente, pero el grupo de alquiler es pequeño "
            "(n = 9). Se reporta como evidencia descriptiva. Además, "
            "**7 de 9 alquileres** carecen de precio y zona a la vez, frente a "
            "**5 de 52 ventas**.",
            "",
            "Esta pregunta sustituye a la original sobre garaje, que solo tenía 7 "
            "anuncios.",
        ],
    )

    add_q(
        L, 16,
        "¿Qué tipo de inmueble presenta mayor opacidad de precio y zona?",
        f"🟡 (subgrupos de {tipos['Cuarto']} a {tipos['Casa']} anuncios)",
        [
            f"- Casa (n = {tipos['Casa']}): "
            f"{sum(1 for a in anuncios if a['_tipo'] == 'Casa' and a.get('precio') is None)} "
            f"sin precio "
            f"({pct(sum(1 for a in anuncios if a['_tipo'] == 'Casa' and a.get('precio') is None), tipos['Casa']):.1f}%); "
            f"{sum(1 for a in anuncios if a['_tipo'] == 'Casa' and a['_zona'] == 'No especificado')} "
            f"sin zona "
            f"({pct(sum(1 for a in anuncios if a['_tipo'] == 'Casa' and a['_zona'] == 'No especificado'), tipos['Casa']):.1f}%).",
            f"- Apartamento (n = {tipos['Apartamento']}): "
            f"{sum(1 for a in anuncios if a['_tipo'] == 'Apartamento' and a.get('precio') is None)} "
            f"sin precio "
            f"({pct(sum(1 for a in anuncios if a['_tipo'] == 'Apartamento' and a.get('precio') is None), tipos['Apartamento']):.1f}%); "
            f"{sum(1 for a in anuncios if a['_tipo'] == 'Apartamento' and a['_zona'] == 'No especificado')} "
            f"sin zona "
            f"({pct(sum(1 for a in anuncios if a['_tipo'] == 'Apartamento' and a['_zona'] == 'No especificado'), tipos['Apartamento']):.1f}%).",
            f"- Inmueble (n = {tipos['Inmueble']}): "
            f"{sum(1 for a in anuncios if a['_tipo'] == 'Inmueble' and a.get('precio') is None)} "
            f"sin precio "
            f"({pct(sum(1 for a in anuncios if a['_tipo'] == 'Inmueble' and a.get('precio') is None), tipos['Inmueble']):.1f}%); "
            f"{sum(1 for a in anuncios if a['_tipo'] == 'Inmueble' and a['_zona'] == 'No especificado')} "
            f"sin zona "
            f"({pct(sum(1 for a in anuncios if a['_tipo'] == 'Inmueble' and a['_zona'] == 'No especificado'), tipos['Inmueble']):.1f}%).",
            f"- Cuarto (n = {tipos['Cuarto']}): "
            f"{sum(1 for a in anuncios if a['_tipo'] == 'Cuarto' and a.get('precio') is None)} "
            f"sin precio "
            f"({pct(sum(1 for a in anuncios if a['_tipo'] == 'Cuarto' and a.get('precio') is None), tipos['Cuarto']):.1f}%); "
            f"{sum(1 for a in anuncios if a['_tipo'] == 'Cuarto' and a['_zona'] == 'No especificado')} "
            f"sin zona "
            f"({pct(sum(1 for a in anuncios if a['_tipo'] == 'Cuarto' and a['_zona'] == 'No especificado'), tipos['Cuarto']):.1f}%).",
            "",
            "Entre los grupos con un tamaño mínimamente interpretable, **Inmueble** "
            "es el más opaco: **6 de 27 (22.2%)** no declaran precio y **19 de 27 "
            "(70.4%)** no especifican zona. Casa registra **4 de 62 (6.5%)** sin "
            "precio y **38 de 62 (61.3%)** sin zona; Apartamento, **6 de 43 "
            "(14.0%)** y **21 de 43 (48.8%)**, respectivamente.",
            "",
            "Cuarto muestra 50.0% sin precio y 100% sin zona, pero solo tiene 2 "
            "anuncios: no se usa para concluir. La categoría Inmueble, al ser un "
            "residual de títulos que no especifican tipo, concentra la mayor "
            "ambigüedad.",
            "",
            "Esta pregunta sustituye a la original sobre planta baja, que solo "
            "tenía 8 anuncios.",
        ],
    )

    add_q(
        L, 17,
        "¿Qué proporción de anuncios incluye al menos una característica física "
        "explícita?",
        f"✅ (n = {total})",
        [
            f"**{len(con_feature)} de {total} anuncios "
            f"({pct(len(con_feature), total):.1f}%)** mencionan al menos una "
            f"característica física: garaje, patio, azotea, terraza, balcón, baño, "
            f"cuartos o habitaciones. Los otros {total - len(con_feature)} "
            f"({pct(total - len(con_feature), total):.1f}%) no describen ninguna.",
            "",
            "La cobertura es baja: la mayoría de los anuncios se limita a precio, "
            "tipo y, a veces, zona. Cualquier análisis de características físicas "
            "queda limitado a una minoría de la muestra.",
        ],
    )

    add_q(
        L, 18,
        "¿Qué características físicas se mencionan con más frecuencia?",
        f"✅ (n = {total})",
        [
            f"- Habitación/cuarto: **{conteo_features['Habitación/cuarto']} "
            f"{unidad(conteo_features['Habitación/cuarto'])}** "
            f"({pct(conteo_features['Habitación/cuarto'], total):.1f}%)",
            f"- Garaje: **{conteo_features['Garaje']} "
            f"{unidad(conteo_features['Garaje'])}** "
            f"({pct(conteo_features['Garaje'], total):.1f}%)",
            f"- Baño: **{conteo_features['Baño']} "
            f"{unidad(conteo_features['Baño'])}** "
            f"({pct(conteo_features['Baño'], total):.1f}%)",
            f"- Balcón: **{conteo_features['Balcón']} "
            f"{unidad(conteo_features['Balcón'])}** "
            f"({pct(conteo_features['Balcón'], total):.1f}%)",
            f"- Terraza: **{conteo_features['Terraza']} "
            f"{unidad(conteo_features['Terraza'])}** "
            f"({pct(conteo_features['Terraza'], total):.1f}%)",
            f"- Azotea: **{conteo_features['Azotea']} "
            f"{unidad(conteo_features['Azotea'])}** "
            f"({pct(conteo_features['Azotea'], total):.1f}%)",
            f"- Patio: **{conteo_features['Patio']} "
            f"{unidad(conteo_features['Patio'])}**",
            "",
            "Los conteos son menciones y pueden solaparse: un mismo anuncio puede "
            "incluir varias características. Solo 20 anuncios contienen al menos "
            "una, por lo que estos números describen una minoría muy específica "
            "de la oferta.",
        ],
    )

    # ---------------- BLOQUE D ----------------
    L.append("### Bloque D: Ubicación dentro de Diez de Octubre")
    L.append("")

    add_q(
        L, 19,
        "¿Qué zonas o barrios aparecen con más frecuencia en los anuncios?",
        f"✅ (n = {total})",
        [
            f"- Santos Suárez: **{zonas['Santos Suárez']} anuncios**",
            f"- Lawton: **{zonas['Lawton']} anuncios**",
            f"- La Víbora: **{zonas['La Víbora']} anuncios**",
            f"- El Sevillano: **{zonas['El Sevillano']} anuncios**",
            f"- El Mónaco: **{zonas['El Mónaco']} anuncios**",
            f"- Luyano: **{zonas['Luyano']} anuncios**",
            f"- Santa Catalina: **{zonas['Santa Catalina']} anuncio**",
            f"- Vía Blanca: **{zonas['Vía Blanca']} anuncio**",
            f"- Calzada 10 de Octubre: **{zonas['Calzada 10 de Octubre']} anuncio**",
            "",
            f"**{total_con_zona} de {total} anuncios "
            f"({pct(total_con_zona, total):.1f}%)** especifican zona; "
            f"**{sin_zona_n} ({pct(sin_zona_n, total):.1f}%)** no lo hacen.",
        ],
    )

    add_q(
        L, 20,
        "¿Qué porcentaje de anuncios con precio USD queda dentro del tramo "
        "P10–P90?",
        f"✅ (n = {stats_usd['n']})",
        [
            f"**{len(dentro_p10_p90)} de {stats_usd['n']} anuncios "
            f"({pct(len(dentro_p10_p90), stats_usd['n']):.1f}%)** quedan dentro "
            f"del tramo **${fmt(stats_usd['p10'])}–${fmt(stats_usd['p90'])} USD**.",
            f"Quedan fuera **{len(bajo_p10) + len(sobre_p90)} "
            f"({pct(len(bajo_p10) + len(sobre_p90), stats_usd['n']):.1f}%)**: "
            f"{len(bajo_p10)} por debajo de P10 "
            f"({pct(len(bajo_p10), stats_usd['n']):.1f}%) y {len(sobre_p90)} por "
            f"encima de P90 ({pct(len(sobre_p90), stats_usd['n']):.1f}%).",
            "",
            "La pregunta complementa la Q3: allí se delimita el rango; aquí se "
            "cuantifica cuánta masa de anuncios queda dentro y cuánta en las "
            "colas. Que casi una quinta parte quede fuera confirma que la "
            "distribución tiene extremos relevantes.",
            "",
            "Esta pregunta sustituye a la original sobre la zona con el precio "
            "promedio más alto, que dependía de 9–10 anuncios.",
        ],
    )

    add_q(
        L, 21,
        "¿Qué zona tiene la mayor cantidad de anuncios publicados?",
        f"✅ (n = {total_con_zona} con zona)",
        [
            f"**Santos Suárez**, con **{zonas['Santos Suárez']} anuncios** "
            f"({pct(zonas['Santos Suárez'], total_con_zona):.1f}% de los que "
            f"tienen zona). De ellos, "
            f"{sum(1 for a in usd if a['_zona'] == 'Santos Suárez')} declaran "
            f"precio en USD.",
            "",
            f"Le siguen Lawton ({zonas['Lawton']}), La Víbora "
            f"({zonas['La Víbora']}) y El Sevillano ({zonas['El Sevillano']}). "
            f"La oferta con zona identificada se concentra en pocos barrios.",
        ],
    )

    add_q(
        L, 22,
        "¿Cuánto cambia el precio promedio al recortar 10% de cada cola?",
        f"✅ (n = {len(valores_recortados)} tras el recorte)",
        [
            f"- Media original: **${fmt(stats_usd['mean'])} USD** "
            f"(n = {stats_usd['n']})",
            f"- Media recortada al 10%: **${fmt(media_recortada)} USD** "
            f"(n = {len(valores_recortados)})",
            f"- Mediana: **${fmt(stats_usd['median'])} USD** "
            f"(n = {stats_usd['n']})",
            "",
            f"El recorte elimina {k_recorte} precios por cada cola "
            f"({k_recorte * 2} en total) y deja un rango de "
            f"**${fmt(valores_recortados[0])}–${fmt(valores_recortados[-1])} USD**. "
            f"La media recortada es **${fmt(diferencia_recorte)} USD menor** que "
            f"la media original "
            f"({pct(diferencia_recorte, stats_usd['mean']):.1f}% menos), lo que "
            f"confirma que los valores extremos inflan el promedio.",
            "",
            "Aun así, la media recortada sigue por encima de la mediana: la "
            "asimetría no desaparece del todo. La mediana sigue siendo la "
            "referencia más conservadora.",
            "",
            "Esta pregunta sustituye a la original sobre diferencias de precio "
            "entre zonas, que se apoyaba en grupos de 9 y 10 anuncios.",
        ],
    )

    add_q(
        L, 23,
        "¿Qué proporción de los anuncios con zona identificada se concentra en "
        "las cuatro zonas principales?",
        f"✅ (censo de {total_con_zona} anuncios con zona)",
        [
            f"Las cuatro zonas principales —{', '.join(z for z, _ in top4)}— "
            f"reúnen **{top4_total} de {total_con_zona} anuncios con zona "
            f"identificada ({pct(top4_total, total_con_zona):.1f}%)**.",
            "",
            f"Los {total_con_zona - top4_total} anuncios restantes se reparten "
            f"entre {len(zonas) - 4} zonas con pocos casos. La oferta está muy "
            f"concentrada, pero esa concentración convive con una mayoría de "
            f"anuncios que ni siquiera declaran zona.",
        ],
    )

    add_q(
        L, 24,
        "¿Cuántos anuncios no especifican zona dentro del municipio?",
        f"✅ (n = {total})",
        [
            f"**{sin_zona_n} de {total} anuncios "
            f"({pct(sin_zona_n, total):.1f}%)** no especifican zona en el título "
            f"ni en el enlace. Solo **{total_con_zona} "
            f"({pct(total_con_zona, total):.1f}%)** permiten ubicar el inmueble "
            f"dentro de un barrio.",
            "",
            "La ubicación es el dato más ausente: 80 de 134 anuncios (59.7%). "
            "Sin zona no se puede comparar el precio por barrio ni verificar si "
            "el anuncio corresponde realmente a Diez de Octubre.",
        ],
    )

    # ---------------- BLOQUE E ----------------
    L.append("### Bloque E: Moneda y mercado informal")
    L.append("")

    add_q(
        L, 25,
        "¿Qué proporción de anuncios con moneda declarada usa USD frente a CUP?",
        f"✅ (n = {len(con_moneda)})",
        [
            f"- USD: **{len(usd)} de {len(con_moneda)} "
            f"({pct(len(usd), len(con_moneda)):.1f}%)**",
            f"- CUP: **{len(cup)} de {len(con_moneda)} "
            f"({pct(len(cup), len(con_moneda)):.1f}%)**",
            "",
            f"En el total del universo, el USD aparece en **{len(usd)} de {total} "
            f"anuncios ({pct(len(usd), total):.1f}%)**. Los otros "
            f"{sin_precio_n} no declaran precio ni moneda.",
            "",
            "El mercado está prácticamente dolarizado. Quien solo dispone de CUP "
            "necesita un tipo de cambio y enfrenta una barrera adicional.",
        ],
    )

    add_q(
        L, 26,
        "¿Cómo se distribuye la informalidad según el tipo de operación?",
        f"🟡 (n = {len(informal)} anuncios informales)",
        [
            f"- Venta: **{informal_por_op.get('Venta', 0)} de {len(informal)} "
            f"({pct(informal_por_op.get('Venta', 0), len(informal)):.1f}%)**",
            f"- Sin clasificar: **{informal_por_op.get('Sin clasificar', 0)} de "
            f"{len(informal)} "
            f"({pct(informal_por_op.get('Sin clasificar', 0), len(informal)):.1f}%)**",
            f"- Alquiler: **{informal_por_op.get('Alquiler', 0)} de {len(informal)} "
            f"({pct(informal_por_op.get('Alquiler', 0), len(informal)):.1f}%)**",
            "",
            "Dentro de cada operación, la proporción es:",
            "",
            f"- Venta: **{informal_por_op.get('Venta', 0)} de {len(ventas)} "
            f"({pct(informal_por_op.get('Venta', 0), len(ventas)):.1f}%)**",
            f"- Alquiler: **{informal_por_op.get('Alquiler', 0)} de "
            f"{len(alquileres)} "
            f"({pct(informal_por_op.get('Alquiler', 0), len(alquileres)):.1f}%)**",
            f"- Sin clasificar: **{informal_por_op.get('Sin clasificar', 0)} de "
            f"{len(sin_clasificar)} "
            f"({pct(informal_por_op.get('Sin clasificar', 0), len(sin_clasificar)):.1f}%)**",
            "",
            "La informalidad se reparte entre venta y anuncios sin operación "
            "declarada; no aparece en alquiler. El grupo es pequeño (15 anuncios), "
            "así que la conclusión es descriptiva.",
            "",
            "Esta pregunta sustituye a la original sobre si los anuncios "
            "informales declaran precio más que los neutros, comparación que "
            "descansaba en 15 casos.",
        ],
    )

    add_q(
        L, 27,
        "¿Qué porcentaje de anuncios incluye palabras de mercado informal?",
        f"✅ (n = {total})",
        [
            f"**{len(informal)} de {total} anuncios "
            f"({pct(len(informal), total):.1f}%)** incluyen palabras como "
            f"«oportunidad», «ganga», «permuta», «intercambio» o «cambio».",
            "",
            "Distribución de las menciones:",
            "",
            f"- Oportunidad: **{palabras_inf['oportunidad']} "
            f"{unidad(palabras_inf['oportunidad'])}**",
            f"- Permuta: **{palabras_inf['permuta']} "
            f"{unidad(palabras_inf['permuta'])}**",
            f"- Cambio: **{palabras_inf['cambio']} "
            f"{unidad(palabras_inf['cambio'])}**",
            "",
            f"Los otros **{len(neutros)} anuncios "
            f"({pct(len(neutros), total):.1f}%)** usan un lenguaje neutro.",
        ],
    )

    add_q(
        L, 28,
        "¿Qué rango de precios es más frecuente entre los anuncios con precio en "
        "USD?",
        f"✅ (n = {stats_usd['n']})",
        [
            f"El rango **10,000 – 20,000 USD** es el más frecuente, con "
            f"**{conteo_rangos[1][1]} anuncios "
            f"({pct(conteo_rangos[1][1], stats_usd['n']):.1f}% de los "
            f"{stats_usd['n']} con precio en USD)**.",
            "",
            "Distribución completa:",
            "",
        ]
        + [
            f"- {etiqueta}: {c} anuncios "
            f"({pct(c, stats_usd['n']):.1f}%)"
            for etiqueta, c in conteo_rangos
        ]
        + [
            "",
            f"El **{pct(sum(c for _, c in conteo_rangos[:3]), stats_usd['n']):.1f}%** "
            f"de los anuncios se concentra por debajo de 30,000 USD, y el "
            f"**{pct(sum(c for _, c in conteo_rangos[:5]), stats_usd['n']):.1f}%** "
            f"por debajo de 50,000 USD.",
        ],
    )

    add_q(
        L, 29,
        "¿Qué proporción de anuncios no declara operación y cómo se distribuye "
        "por tipo de inmueble?",
        f"✅ (n = {total})",
        [
            f"**{len(sin_clasificar)} de {total} anuncios "
            f"({pct(len(sin_clasificar), total):.1f}%)** no declaran si se venden "
            f"o se alquilan. Es el segundo dato más ausente, después de la zona "
            f"({pct(sin_zona_n, total):.1f}%).",
            "",
            "Distribución por tipo:",
            "",
            f"- Casa: **{sum(1 for a in sin_clasificar if a['_tipo'] == 'Casa')} "
            f"de {tipos['Casa']} "
            f"({pct(sum(1 for a in sin_clasificar if a['_tipo'] == 'Casa'), tipos['Casa']):.1f}%)**",
            f"- Apartamento: "
            f"**{sum(1 for a in sin_clasificar if a['_tipo'] == 'Apartamento')} "
            f"de {tipos['Apartamento']} "
            f"({pct(sum(1 for a in sin_clasificar if a['_tipo'] == 'Apartamento'), tipos['Apartamento']):.1f}%)**",
            f"- Inmueble: "
            f"**{sum(1 for a in sin_clasificar if a['_tipo'] == 'Inmueble')} "
            f"de {tipos['Inmueble']} "
            f"({pct(sum(1 for a in sin_clasificar if a['_tipo'] == 'Inmueble'), tipos['Inmueble']):.1f}%)**",
            f"- Cuarto: **{sum(1 for a in sin_clasificar if a['_tipo'] == 'Cuarto')} "
            f"de {tipos['Cuarto']} "
            f"({pct(sum(1 for a in sin_clasificar if a['_tipo'] == 'Cuarto'), tipos['Cuarto']):.1f}%)**",
            "",
            f"La falta de operación afecta a todos los tipos, pero es más frecuente "
            f"en Inmueble (66.7%). No equivale a falta de precio: "
            f"**{sum(1 for a in sin_clasificar if a.get('precio') is not None)} de "
            f"{len(sin_clasificar)} anuncios sin operación "
            f"({pct(sum(1 for a in sin_clasificar if a.get('precio') is not None), len(sin_clasificar)):.1f}%)** "
            f"sí declaran precio.",
            "",
            "Esta pregunta sustituye a la original sobre particulares frente a "
            "agencias, que no podía responderse porque la base no tiene campo de "
            "vendedor.",
        ],
    )

    add_q(
        L, 30,
        "¿Qué recomendación práctica se puede hacer a alguien que quiera comprar "
        "o alquilar en Diez de Octubre?",
        "✅ (síntesis de Q1–Q29)",
        [
            f"1. **Presupuesto:** la mediana general es "
            f"**${fmt(stats_usd['median'])} USD** y la de ventas explícitas "
            f"**${fmt(stats_venta['median'])} USD**. El 80% central está entre "
            f"**${fmt(stats_usd['p10'])} y ${fmt(stats_usd['p90'])} USD**; el "
            f"tramo más frecuente es **10,000 – 20,000 USD** "
            f"({conteo_rangos[1][1]} anuncios, "
            f"{pct(conteo_rangos[1][1], stats_usd['n']):.1f}%).",
            f"2. **Tipo de inmueble:** el apartamento tiene mediana "
            f"**${fmt(stats_tipo['Apartamento']['median'])} USD** "
            f"(n = {stats_tipo['Apartamento']['n']}); la casa, "
            f"**${fmt(stats_tipo['Casa']['median'])} USD** "
            f"(n = {stats_tipo['Casa']['n']}). El apartamento es la opción más "
            f"accesible.",
            f"3. **Zonas:** Santos Suárez concentra la mayor oferta "
            f"({zonas['Santos Suárez']} anuncios), seguida por Lawton "
            f"({zonas['Lawton']}) y La Víbora ({zonas['La Víbora']}). La Víbora "
            f"tiene la media más alta, pero su mediana es "
            f"**${fmt(stats_zona_5['La Víbora']['median'])} USD**; Lawton "
            f"**${fmt(stats_zona_5['Lawton']['median'])} USD** y Santos Suárez "
            f"**${fmt(stats_zona_5['Santos Suárez']['median'])} USD**. Para "
            f"comparar, use medianas: La Víbora sigue siendo más cara, pero la "
            f"brecha es menor que con la media.",
            f"4. **Moneda:** **{len(usd)} de {len(con_moneda)} anuncios con moneda "
            f"declarada ({pct(len(usd), len(con_moneda)):.1f}%)** están en USD. "
            f"Hay que contar con divisas o verificar el tipo de cambio si se paga "
            f"en CUP.",
            f"5. **Información incompleta:** **{sin_precio_n} anuncios "
            f"({pct(sin_precio_n, total):.1f}%)** no declaran precio, "
            f"**{sin_zona_n} ({pct(sin_zona_n, total):.1f}%)** no especifican "
            f"zona y **{len(totalmente_opacos)} "
            f"({pct(len(totalmente_opacos), total):.1f}%)** son totalmente "
            f"opacos. Solo **{completo_n} ({pct(completo_n, total):.1f}%)** "
            f"permiten cruzar precio y zona. Verifique siempre precio, ubicación "
            f"y situación legal directamente con el vendedor.",
            f"6. **Precaución estadística:** los subgrupos por zona y tipo son "
            f"pequeños. Use las medianas y los rangos, no solo los promedios, y "
            f"no generalice los resultados de un barrio al municipio completo.",
        ],
    )

    # ------------------------------------------------------------------
    # Conclusiones
    # ------------------------------------------------------------------
    L.append("## Conclusiones")
    L.append("")
    L.append(
        f"1. **Dolarización casi total:** {len(usd)} de {len(con_moneda)} anuncios "
        f"con moneda declarada ({pct(len(usd), len(con_moneda)):.1f}%) están en "
        f"USD. El mercado digital de Diez de Octubre funciona en divisas."
    )
    L.append(
        f"2. **Precios sesgados a la derecha:** la media "
        f"(${fmt(stats_usd['mean'])}) supera a la mediana "
        f"(${fmt(stats_usd['median'])}) en "
        f"${fmt(stats_usd['mean'] - stats_usd['median'])}. La media recortada al "
        f"10% (${fmt(media_recortada)}) reduce la influencia de los extremos, "
        f"pero sigue por encima de la mediana."
    )
    L.append(
        f"3. **El apartamento es la opción más accesible:** mediana "
        f"${fmt(stats_tipo['Apartamento']['median'])} USD frente a "
        f"${fmt(stats_tipo['Casa']['median'])} USD de la casa. La diferencia de "
        f"mediana es de "
        f"${fmt(stats_tipo['Casa']['median'] - stats_tipo['Apartamento']['median'])} USD."
    )
    L.append(
        f"4. **Concentración territorial:** las cuatro zonas principales reúnen "
        f"{top4_total} de {total_con_zona} anuncios con zona "
        f"({pct(top4_total, total_con_zona):.1f}%). La Víbora tiene la media más "
        f"alta (${fmt(stats_zona_5[zona_cara_5]['mean'])}), pero su mediana "
        f"(${fmt(stats_zona_5[zona_cara_5]['median'])}) es mucho menor: el "
        f"promedio está inflado por valores extremos."
    )
    L.append(
        f"5. **La opacidad es un rasgo estructural:** solo {completo_n} de "
        f"{total} anuncios ({pct(completo_n, total):.1f}%) permiten cruzar "
        f"precio y zona; {sin_zona_n} ({pct(sin_zona_n, total):.1f}%) no "
        f"especifican zona; {len(sin_clasificar)} "
        f"({pct(len(sin_clasificar), total):.1f}%) no declaran operación; y "
        f"{len(totalmente_opacos)} ({pct(len(totalmente_opacos), total):.1f}%) "
        f"son totalmente opacos."
    )
    L.append(
        f"6. **El alquiler es el segmento más opaco:** 8 de 9 alquileres no "
        f"declaran precio y 8 de 9 no especifican zona. Además, ningún alquiler "
        f"declara precio en USD, por lo que no se puede estimar una referencia "
        f"de alquiler con esta base."
    )
    L.append(
        f"7. **La informalidad se concentra en venta y en anuncios sin "
        f"operación:** {len(informal)} anuncios ({pct(len(informal), total):.1f}%) "
        f"usan lenguaje de oportunidad, permuta o cambio; {informal_por_op.get('Venta', 0)} "
        f"son ventas y {informal_por_op.get('Sin clasificar', 0)} no declaran "
        f"operación. No hay ninguno en alquiler."
    )
    L.append(
        "8. **Los 10 reemplazos mejoran la calidad de la evidencia:** en lugar de "
        "forzar estimaciones con 1, 7, 8, 9, 10, 12, 14 o 15 casos, el informe "
        "mide la opacidad, compara medianas y usa estimadores robustos. La "
        "ausencia de datos deja de ser una limitación oculta y se convierte en "
        "un resultado."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Limitaciones
    # ------------------------------------------------------------------
    L.append("## Limitaciones")
    L.append("")
    L.append(
        "- Los datos provienen solo de Revolico; no representan todo el mercado "
        "inmobiliario de Diez de Octubre."
    )
    L.append(
        "- Se exploró Facebook (37 publicaciones), pero se excluyó del análisis "
        "cuantitativo porque no comparte el esquema de campos de Revolico ni un "
        "municipio normalizado."
    )
    L.append(
        f"- La muestra es de {total} anuncios y puede no ser representativa del "
        f"mercado completo."
    )
    L.append(
        "- La clasificación de tipo, zona y operación depende de palabras clave y "
        "puede contener errores."
    )
    L.append(
        "- Los subgrupos por zona (n = 5–14), alquiler (n = 9) y Cuarto (n = 2) "
        "son pequeños; sus resultados son descriptivos."
    )
    L.append(
        "- No existe un campo de vendedor o agencia que permita distinguir "
        "particulares de intermediarios. Tampoco hay fecha de publicación: el ID "
        "del enlace es solo un proxy de recencia."
    )
    L.append(
        "- El anuncio de $180,000 está clasificado como «Inmueble» porque su "
        "título no especifica «Casa»; no se reclasifica sin evidencia textual. "
        "Ese valor atípico infla la media y la media de La Víbora."
    )
    L.append(
        "- No se imputan precios, zonas ni operaciones. La ausencia se reporta "
        "como hallazgo, no se rellena con supuestos."
    )
    L.append("")
    L.append("---")
    L.append("")
    L.append(
        "Informe generado por el Proyecto de Ciencia de Datos — Universidad de La "
        "Habana"
    )
    L.append("")
    L.append("Facultad de Matemática y Computación (MATCOM)")
    L.append("")
    L.append("Profesor: **Yudivian Almeida Cruz**")
    L.append("")
    L.append("Repositorio: `Mercado-digital-cubano-en-10-de-octubre`")
    L.append("")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    print(f"Informe guardado en: {OUTPUT_FILE}")
    print(f"Anuncios: {total} | USD: {len(usd)} | Sin precio: {sin_precio_n}")
    print(f"Preguntas: 30 (20 conservadas + 10 reemplazadas)")
    print(f"Reemplazadas: {', '.join(f'Q{n}' for n in REEMPLAZADAS)}")


if __name__ == "__main__":
    main()
