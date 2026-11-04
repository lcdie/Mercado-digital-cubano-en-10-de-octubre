#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el informe final del mercado inmobiliario digital de Diez de Octubre.

Base de datos:
    datos/brutos/revolico_crudos_limpio_final.json
    134 anuncios estrictos (solo Diez de Octubre, precio >= 1,000 USD cuando
    existe precio). La base anterior de 171 anuncios incluía 37 anuncios de
    otros municipios y queda superseded.

Estructura del informe:
    - Problema social: opacidad, dolarización, desigualdad territorial e
      informalidad.
    - 30 preguntas en seis bloques: A precios, B territorio, C dolarización,
      D opacidad, E informalidad, F tipos de inmueble.
    - La ausencia de información se reporta como hallazgo, no solo como
      limitación.

Salida:
    analisis/informe_final.md
"""

import json
import math
import os
import statistics
from collections import Counter, defaultdict
from datetime import datetime

INPUT_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
REJECTED_FILE = "datos/limpios/anuncios_eliminados_por_filtro_final.json"
OUTPUT_FILE = "analisis/informe_final.md"

FEATURES = [
    "garaje", "garage", "patio", "azotea", "terraza",
    "balcón", "balcon", "baño", "bano", "cuarto", "habitación", "habitacion",
]

PALABRAS_INFORMALES = ["oportunidad", "ganga", "permuta", "intercambio", "cambio"]


# ---------------------------------------------------------------------------
# Utilidades de clasificación
# ---------------------------------------------------------------------------

def cargar_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def clasificar_tipo(titulo):
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


def clasificar_zona(titulo, enlace):
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
        if any(v in texto for v in variantes):
            return nombre
    return "No especificado"


def clasificar_operacion(titulo):
    t = (titulo or "").lower()
    venta = ["vendo", "se vende", "venta", "vende", "permuta", "permuto"]
    alquiler = ["alquiler", "alquila", "se alquila", "renta"]
    if any(p in t for p in venta) and not any(p in t for p in alquiler):
        return "Venta"
    if any(p in t for p in alquiler) and not any(p in t for p in venta):
        return "Alquiler"
    return "Sin clasificar"


# ---------------------------------------------------------------------------
# Utilidades estadísticas
# ---------------------------------------------------------------------------

def percentil(valores_ordenados, p):
    """Percentil con interpolación lineal."""
    n = len(valores_ordenados)
    if n == 0:
        return 0.0
    k = (n - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(valores_ordenados[f])
    return valores_ordenados[f] * (c - k) + valores_ordenados[c] * (k - f)


def stats(valores):
    """Devuelve n, media, mediana, P10, P90, mínimo y máximo."""
    valores = sorted(valores)
    n = len(valores)
    if n == 0:
        return None
    return {
        "n": n,
        "mean": sum(valores) / n,
        "median": statistics.median(valores),
        "p10": percentil(valores, 0.10),
        "p90": percentil(valores, 0.90),
        "min": min(valores),
        "max": max(valores),
    }


def fmt(valor):
    return f"{valor:,.2f}"


def pct(n, d):
    return 100.0 * n / d if d else 0.0


def unidad(n):
    return "anuncio" if n == 1 else "anuncios"


def tiene_feature(titulo):
    t = (titulo or "").lower()
    return any(f in t for f in FEATURES)


# ---------------------------------------------------------------------------
# Informe
# ---------------------------------------------------------------------------

def main():
    anuncios = cargar_json(INPUT_FILE)
    total = len(anuncios)

    # Clasificación de cada anuncio
    for a in anuncios:
        a["_tipo"] = clasificar_tipo(a.get("titulo"))
        a["_zona"] = clasificar_zona(a.get("titulo"), a.get("enlace"))
        a["_op"] = clasificar_operacion(a.get("titulo"))

    # Subconjuntos principales
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
    alquileres_usd = [a for a in alquileres if a.get("precio") is not None
                      and str(a.get("moneda", "")).upper() == "USD"]
    alquileres_cup = [a for a in alquileres
                      if a.get("precio") is not None
                      and str(a.get("moneda", "")).upper() == "CUP"]

    stats_usd = stats([a["precio"] for a in usd])
    stats_venta = stats([a["precio"] for a in ventas_usd])

    # Zonas
    zonas = Counter(a["_zona"] for a in anuncios if a["_zona"] != "No especificado")
    total_con_zona = sum(zonas.values())
    sin_zona_total = total - total_con_zona

    precios_zona = defaultdict(list)
    for a in usd:
        if a["_zona"] != "No especificado":
            precios_zona[a["_zona"]].append(a["precio"])

    zonas_5 = {z: v for z, v in precios_zona.items() if len(v) >= 5}
    zonas_10 = {z: v for z, v in precios_zona.items() if len(v) >= 10}

    stats_zona = {z: stats(v) for z, v in precios_zona.items()}
    stats_zona_5 = {z: stats(v) for z, v in zonas_5.items()}

    zona_cara = max(zonas_5, key=lambda z: stats_zona_5[z]["mean"])
    zona_barata = min(zonas_5, key=lambda z: stats_zona_5[z]["mean"])
    zona_mediana_alta = max(zonas_5, key=lambda z: stats_zona_5[z]["median"])
    zona_cara_10 = max(zonas_10, key=lambda z: stats_zona[z]["mean"])

    top4 = zonas.most_common(4)
    top4_total = sum(c for _, c in top4)

    # Tipos
    tipos = Counter(a["_tipo"] for a in anuncios)
    precios_tipo = defaultdict(list)
    for a in usd:
        precios_tipo[a["_tipo"]].append(a["precio"])
    stats_tipo = {t: stats(v) for t, v in precios_tipo.items()}
    tipos_comparables = [t for t in stats_tipo if stats_tipo[t]["n"] >= 10]

    # Opacidad
    sin_precio_n = len(sin_precio)
    sin_zona_n = sum(1 for a in anuncios if a["_zona"] == "No especificado")
    ambos_n = sum(1 for a in anuncios
                  if a.get("precio") is None and a["_zona"] == "No especificado")
    completo_n = sum(1 for a in anuncios
                     if a.get("precio") is not None and a["_zona"] != "No especificado")

    sin_feature = [a for a in anuncios if not tiene_feature(a.get("titulo"))]
    totalmente_opacos = [
        a for a in anuncios
        if a.get("precio") is None
        and a["_zona"] == "No especificado"
        and not tiene_feature(a.get("titulo"))
    ]

    # Informalidad
    informal = [
        a for a in anuncios
        if any(p in (a.get("titulo") or "").lower() for p in PALABRAS_INFORMALES)
    ]
    neutros = [a for a in anuncios if a not in informal]
    informal_con_precio = sum(1 for a in informal if a.get("precio") is not None)
    neutros_con_precio = sum(1 for a in neutros if a.get("precio") is not None)
    informal_por_op = Counter(a["_op"] for a in informal)
    palabras_inf = Counter(
        p for a in anuncios for p in PALABRAS_INFORMALES
        if p in (a.get("titulo") or "").lower()
    )

    # Dolarización
    usd_declarada = len(usd)
    pct_usd_declarada = pct(usd_declarada, len(con_moneda))
    pct_usd_total = pct(usd_declarada, total)
    usd_min = pct(usd_declarada, total)
    usd_max = pct(usd_declarada + sin_precio_n, total)

    # Anuncios rechazados por el filtro (para trazabilidad)
    rechazados = []
    if os.path.exists(REJECTED_FILE):
        rechazados = cargar_json(REJECTED_FILE)
    motivos_rechazo = Counter(r.get("motivo_eliminacion") for r in rechazados)
    rechazados_municipio = motivos_rechazo.get(
        "MUNICIPIO_DISTINTO_A_DIEZ_DE_OCTUBRE", 0
    )
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
    L.append("## Opacidad, dolarización, desigualdad territorial e informalidad")
    L.append("")
    L.append(f"**Fecha de generación:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    L.append(f"**Corte de los datos:** {fecha_corte}")
    L.append(f"**Fuente:** Revolico (anuncios activos)")
    L.append(f"**Universo estricto:** {total} anuncios de Diez de Octubre")
    L.append(f"**Anuncios con precio en USD:** {len(usd)}")
    L.append("")
    L.append("## Resumen ejecutivo")
    L.append("")
    L.append(
        f"La base final contiene **{total} anuncios** estrictamente de Diez de "
        f"Octubre. Respecto a los 171 anuncios del informe anterior, se retiraron "
        f"**37** que mencionaban otros municipios. Sobre la fuente completa de 270 "
        f"anuncios, el filtro descartó además {rechazados_precio} con precio "
        f"inferior a 1,000 USD (que no formaban parte de los 171). La base "
        f"corregida es la que se usa en todas las respuestas de este informe."
    )
    L.append("")
    L.append("Los hallazgos principales son:")
    L.append("")
    L.append(
        f"- **Dolarización:** {usd_declarada} de {len(con_moneda)} anuncios con "
        f"moneda declarada están en USD (**{pct_usd_declarada:.1f}%**), y "
        f"{usd_declarada} de {total} del total (**{pct_usd_total:.1f}%**)."
    )
    L.append(
        f"- **Precios de compra:** mediana **${fmt(stats_venta['median'])} USD**; "
        f"P10–P90 **${fmt(stats_venta['p10'])}–${fmt(stats_venta['p90'])} USD**; "
        f"media **${fmt(stats_venta['mean'])} USD** (n = {stats_venta['n']} ventas con precio USD)."
    )
    L.append(
        f"- **Alquiler:** {len(alquileres_con_precio)} de {len(alquileres)} "
        f"alquileres declaran precio y **ninguno lo hace en USD**; el precio de "
        f"alquiler no es estimable con esta base."
    )
    L.append(
        f"- **Opacidad:** {sin_precio_n} de {total} anuncios ({pct(sin_precio_n, total):.1f}%) "
        f"no declaran precio; {sin_zona_n} ({pct(sin_zona_n, total):.1f}%) no "
        f"especifican zona; solo {completo_n} ({pct(completo_n, total):.1f}%) "
        f"permiten cruzar precio y zona."
    )
    L.append(
        f"- **Desigualdad territorial:** las cuatro zonas principales concentran "
        f"{top4_total} de {total_con_zona} anuncios con zona identificada "
        f"({pct(top4_total, total_con_zona):.1f}%). La Víbora tiene la media más "
        f"alta (${fmt(stats_zona_5[zona_cara]['mean'])} USD, n = "
        f"{stats_zona_5[zona_cara]['n']}), pero su mediana es "
        f"${fmt(stats_zona_5[zona_cara]['median'])} USD."
    )
    L.append(
        f"- **Informalidad:** {len(informal)} de {total} anuncios "
        f"({pct(len(informal), total):.1f}%) usan lenguaje de oportunidad, "
        f"permuta o cambio. No aparecen en alquiler: se concentran en venta y "
        f"en anuncios sin operación declarada."
    )
    L.append(
        f"- **Tipo de inmueble:** el apartamento es la opción más accesible: "
        f"media **${fmt(stats_tipo['Apartamento']['mean'])} USD** y mediana "
        f"**${fmt(stats_tipo['Apartamento']['median'])} USD** (n = "
        f"{stats_tipo['Apartamento']['n']}), frente a la casa con media "
        f"**${fmt(stats_tipo['Casa']['mean'])} USD** y mediana "
        f"**${fmt(stats_tipo['Casa']['median'])} USD** (n = {stats_tipo['Casa']['n']})."
    )
    L.append("")
    L.append(
        "La ausencia de datos no se trata como un simple defecto: se mide y se "
        "reporta como un rasgo del mercado. Un anuncio sin precio, sin zona o "
        "sin operación limita la capacidad de comparar y de verificar, y esa "
        "limitación es parte del problema social que el estudio documenta."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Introducción
    # ------------------------------------------------------------------
    L.append("## Introducción: por qué este mercado es un problema social")
    L.append("")
    L.append(
        "El acceso a la vivienda en La Habana no depende solo de la oferta y la "
        "demanda. En un mercado digital con precios en divisas, ubicaciones "
        "incompletas y anuncios que no declaran si se vende o se alquila, la "
        "información se convierte en un recurso desigual. Quien tiene acceso a "
        "divisas, a contactos y a tiempo para verificar puede comparar; quien no "
        "lo tiene queda expuesto a la opacidad y a la intermediación informal."
    )
    L.append("")
    L.append("Este informe estudia cuatro dimensiones de ese problema:")
    L.append("")
    L.append(
        "1. **Precios:** ¿cuánto cuesta comprar y cuánto alquilar, y con qué "
        "dispersión? La media sola engaña; por eso se reportan mediana y P10–P90."
    )
    L.append(
        "2. **Territorio:** ¿la oferta y los precios se distribuyen de forma "
        "desigual entre los barrios del mismo municipio?"
    )
    L.append(
        "3. **Dolarización:** ¿en qué medida el mercado funciona en USD y qué "
        "implica para quien solo tiene CUP?"
    )
    L.append(
        "4. **Opacidad e informalidad:** ¿cuánta información falta y qué "
        "prácticas (lenguaje de oportunidad, permuta, anuncios sin operación) "
        "aparecen en los anuncios?"
    )
    L.append("")
    L.append(
        "El municipio Diez de Octubre es un caso relevante porque combina una "
        "alta densidad de vivienda, barrios con identidad propia (Santos Suárez, "
        "Lawton, La Víbora, Luyano, El Sevillano) y una presencia importante de "
        "anuncios digitales. La comparación entre barrios permite observar si el "
        "mercado reproduce o atenúa las desigualdades territoriales."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Metodología
    # ------------------------------------------------------------------
    L.append("## Metodología y corrección de la base")
    L.append("")
    L.append("### Fuente y universo")
    L.append("")
    L.append(
        "- **Revolico:** única fuente usada en los cálculos. Se analizan los "
        f"anuncios activos del municipio Diez de Octubre con corte al {fecha_corte}."
    )
    L.append(
        "- **Anuario Estadístico de Cuba (ONEI):** se consulta como contexto "
        "general del municipio; no se usa para calcular precios ni proporciones "
        "de la muestra digital."
    )
    L.append(
        "- **Facebook (fuente explorada, no integrada):** se revisaron 43 "
        "publicaciones de grupos de compraventa; 42 se conservan tras aplicar "
        "el mismo filtro municipal y de precio que a Revolico. No se incorporan "
        "al análisis cuantitativo porque no comparten el esquema de campos de "
        "Revolico (precio anidado, ubicación en texto libre y sin municipio "
        "normalizado) y no permiten aplicar el mismo filtro municipal. "
        "Mezclarlas sin normalizar habría introducido un sesgo difícil de medir."
    )
    L.append("")
    L.append("### Filtro estricto y contaminación de la base anterior")
    L.append("")
    L.append(
        "El campo `municipio` del scraper **no es fiable**: todos los anuncios "
        "aparecen como «Diez de Octubre», incluso cuando el título dice «Habana "
        "Vieja», «Boyeros», «Arroyo Naranjo» o «Santa Fe». Por eso el filtro "
        "revisa el título y el enlace, y la exclusión municipal tiene prioridad "
        "sobre el campo `municipio`."
    )
    L.append("")
    L.append(
        f"De la fuente inicial de 270 anuncios, el filtro conserva **{total}** y "
        f"descarta **{len(rechazados)}**: {rechazados_municipio} por mencionar "
        f"otro municipio o localidad y {rechazados_precio} por precio inferior a "
        f"1,000 USD. La versión anterior del informe usaba 171 anuncios; de ellos, "
        f"**37 mencionaban otros municipios** y fueron retirados. La base de 134 "
        f"es la base estrictamente municipal que se usa en esta versión."
    )
    L.append("")
    L.append("Ejemplos de anuncios retirados por pertenecer a otro municipio:")
    L.append("")
    L.append("| Anuncio (extracto) | Municipio o zona detectada |")
    L.append("|---|---|")
    L.append("| «Casa en cojímar» | Cojímar (Habana del Este) |")
    L.append("| «8,000 USD Casa 2do piso Poey Arroyo Naranjo» | Arroyo Naranjo |")
    L.append("| «20,000 USD Casa en Boyeros cerca del aeropuerto» | Boyeros |")
    L.append("| «56,000 USD CASA EN SANTA FE PRECIO 56MIL USD» | Santa Fe |")
    L.append("| «33,000 USD MUNICIPIO PLAZA» | Plaza de la Revolución |")
    L.append("| «45,000 USD Casa Independiente con patio en altahabana» | Altahabana |")
    L.append("| «Casa de renta en Río Cristal, Boyeros» | Boyeros |")
    L.append("| «CASA EN VENTA EN LA HABANA, PÁRRAGA (ARROYO NARANJO)» | Arroyo Naranjo |")
    L.append("| «Casa en Marianao» | Marianao |")
    L.append("")
    L.append(
        "La distinción es importante: estos 37 anuncios **no son ausencia de "
        "información**, son contaminación de la base. Una vez corregida, la "
        "ausencia se mide sobre los 134 anuncios que sí pertenecen al municipio."
    )
    L.append("")
    L.append("### Reglas de análisis")
    L.append("")
    L.append(
        f"- **Precios:** se analizan solo los {len(usd)} anuncios con precio "
        f"declarado en USD. Se excluye 1 anuncio en CUP y {sin_precio_n} sin "
        f"precio. Para reducir el efecto de valores extremos se reportan media, "
        f"mediana y rango P10–P90, siempre con el tamaño de muestra (n)."
    )
    L.append(
        "- **Subgrupos pequeños:** los grupos con n < 10 se presentan como "
        "evidencia descriptiva, no como conclusión firme. Las zonas con n < 5 "
        "no se usan para comparar promedios."
    )
    L.append(
        "- **Clasificación:** el tipo de inmueble, la zona y la operación se "
        "infieren de palabras clave del título y del enlace. Es una "
        "clasificación reproducible, pero puede contener errores de asignación."
    )
    L.append(
        "- **Ausencia:** un anuncio sin precio, sin zona o sin operación no se "
        "elimina del universo. Se conserva y se contabiliza como indicador de "
        "opacidad, porque su ausencia también describe el mercado."
    )
    L.append("")
    L.append("### Trazabilidad del cambio respecto a la versión anterior")
    L.append("")
    L.append(
        "La versión anterior respondía 30 preguntas sobre 171 anuncios. Esa base "
        "incluía 37 anuncios de otros municipios, por lo que sus cifras no eran "
        "estrictamente de Diez de Octubre y quedan supersedidas. Además, cinco "
        "preguntas originales no eran estimables con los datos disponibles "
        "(mediana del alquiler, comparación compra–alquiler, precio por metro "
        "cuadrado, zonas por operación y precio promedio en CUP). En esta versión "
        "esas preguntas se reemplazan por preguntas que sí pueden responderse, "
        "incluyendo varias que miden la ausencia de información."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Preguntas
    # ------------------------------------------------------------------
    L.append("## Las 30 preguntas y sus respuestas")
    L.append("")
    L.append(
        "Cada pregunta indica su nivel de evidencia: ✅ sólida (n ≥ 30 o censo "
        "completo del subgrupo), 🟡 descriptiva (n = 5–29) y 🔴 no estimable "
        "(la ausencia es el hallazgo)."
    )
    L.append("")

    # ---------------- BLOQUE A ----------------
    L.append("### Bloque A: Precios de referencia")
    L.append("")
    L.append(
        f"**A1. ¿Cuál es el precio promedio de compra en USD?** ✅ "
        f"(n = {stats_venta['n']})"
    )
    L.append("")
    L.append(
        f"> **${fmt(stats_venta['mean'])} USD** entre las {stats_venta['n']} "
        f"ventas explícitas con precio en USD. Si se incluyen todos los anuncios "
        f"con precio USD (ventas y anuncios sin operación declarada; no hay "
        f"alquileres en USD), la media sube a "
        f"**${fmt(stats_usd['mean'])} USD** (n = {stats_usd['n']}), porque los "
        f"anuncios sin operación declarada incluyen inmuebles de mayor precio. "
        f"La media de compra es una referencia, no el precio típico: la mediana "
        f"es bastante menor (A2)."
    )
    L.append("")
    L.append(
        f"**A2. ¿Cuál es la mediana y el rango P10–P90 del precio de compra en USD?** "
        f"✅ (n = {stats_venta['n']})"
    )
    L.append("")
    L.append(
        f"> Mediana **${fmt(stats_venta['median'])} USD**. El 80% central de las "
        f"ventas está entre **${fmt(stats_venta['p10'])} USD** (P10) y "
        f"**${fmt(stats_venta['p90'])} USD** (P90). El mínimo es "
        f"**${fmt(stats_venta['min'])} USD** y el máximo "
        f"**${fmt(stats_venta['max'])} USD**. La mediana es menor que la media "
        f"(${fmt(stats_venta['mean'])}), señal de una distribución sesgada a la "
        f"derecha: unos pocos anuncios muy caros elevan el promedio."
    )
    L.append("")
    L.append(
        f"**A3. ¿Cuál es el precio promedio o mediano del alquiler?** 🔴 "
        f"(no estimable)"
    )
    L.append("")
    L.append(
        f"> **No estimable.** Hay {len(alquileres)} anuncios de alquiler: "
        f"{len(alquileres_con_precio)} declara precio (uno solo, en CUP: "
        f"50,000 CUP) y {len(alquileres) - len(alquileres_con_precio)} no lo "
        f"declaran ({pct(len(alquileres) - len(alquileres_con_precio), len(alquileres)):.1f}%). "
        f"Ningún alquiler tiene precio en USD. No se puede calcular una media ni "
        f"una mediana en USD, y el único precio en CUP no es comparable sin un "
        f"tipo de cambio explícito. La ausencia de precio de alquiler es el "
        f"hallazgo, no una limitación menor."
    )
    L.append("")
    L.append(
        f"**A4. ¿Qué proporción de alquileres declara precio y en qué moneda?** "
        f"✅ (censo de {len(alquileres)} alquileres)"
    )
    L.append("")
    L.append(
        f"> **{len(alquileres_con_precio)} de {len(alquileres)} "
        f"({pct(len(alquileres_con_precio), len(alquileres)):.1f}%)** declaran "
        f"precio. Ese único anuncio está en **CUP** (50,000 CUP); "
        f"**0 de {len(alquileres)}** lo declaran en USD. Los otros "
        f"{len(alquileres) - len(alquileres_con_precio)} alquileres no permiten "
        f"conocer ni siquiera el orden de magnitud del precio."
    )
    L.append("")
    L.append(
        f"**A5. ¿La compra declara precio más que el alquiler?** ✅ "
        f"(censo de ventas y alquileres)"
    )
    L.append("")
    L.append(
        f"> Sí. **{len(ventas_con_precio)} de {len(ventas)} ventas "
        f"({pct(len(ventas_con_precio), len(ventas)):.1f}%)** declaran precio, "
        f"frente a **{len(alquileres_con_precio)} de {len(alquileres)} alquileres "
        f"({pct(len(alquileres_con_precio), len(alquileres)):.1f}%)**. La brecha "
        f"es de **{pct(len(ventas_con_precio), len(ventas)) - pct(len(alquileres_con_precio), len(alquileres)):.1f} puntos porcentuales**. "
        f"El mercado de compra es mucho más transparente en precio que el de "
        f"alquiler, que funciona casi por contacto directo."
    )
    L.append("")

    # ---------------- BLOQUE B ----------------
    L.append("### Bloque B: Desigualdades territoriales")
    L.append("")
    L.append(
        f"**B1. ¿Qué zonas concentran la mayor oferta?** ✅ "
        f"({total_con_zona} anuncios con zona identificada)"
    )
    L.append("")
    for z, c in zonas.most_common():
        L.append(f"> - {z}: **{c} {unidad(c)}** ({pct(c, total_con_zona):.1f}% de los anuncios con zona)")
    L.append(">")
    L.append(
        f"> **{total_con_zona} de {total} anuncios ({pct(total_con_zona, total):.1f}%)** "
        f"especifican zona; **{sin_zona_n} ({pct(sin_zona_n, total):.1f}%)** no lo "
        f"hacen. Las cuatro zonas principales —{', '.join(z for z, _ in top4)}— "
        f"reúnen **{top4_total} de {total_con_zona} ({pct(top4_total, total_con_zona):.1f}%)** "
        f"de la oferta con zona identificada: la información territorial está muy "
        f"concentrada en pocos barrios."
    )
    L.append("")
    L.append(
        f"**B2. ¿Qué zona tiene el precio promedio más alto?** 🟡 "
        f"(n = {stats_zona_5[zona_cara]['n']} en La Víbora)"
    )
    L.append("")
    L.append(
        f"> **{zona_cara}**, con una media de "
        f"**${fmt(stats_zona_5[zona_cara]['mean'])} USD** (n = "
        f"{stats_zona_5[zona_cara]['n']}). Es un resultado descriptivo: el grupo "
        f"tiene menos de 10 anuncios y su media está influida por un anuncio de "
        f"$180,000 USD. Si se exige n ≥ 10, la zona con media más alta es "
        f"**{zona_cara_10}** (${fmt(stats_zona[zona_cara_10]['mean'])} USD, "
        f"n = {stats_zona[zona_cara_10]['n']})."
    )
    L.append("")
    L.append(
        f"**B3. ¿Qué zona tiene la mediana más alta?** 🟡 "
        f"(n = {stats_zona_5[zona_mediana_alta]['n']} en La Víbora)"
    )
    L.append("")
    L.append(
        f"> **{zona_mediana_alta}**, con una mediana de "
        f"**${fmt(stats_zona_5[zona_mediana_alta]['median'])} USD** (n = "
        f"{stats_zona_5[zona_mediana_alta]['n']}). El orden completo de las "
        f"zonas con n ≥ 5 es:"
    )
    L.append(">")
    for z in sorted(zonas_5, key=lambda x: stats_zona_5[x]["median"], reverse=True):
        s = stats_zona_5[z]
        L.append(f"> - {z}: mediana **${fmt(s['median'])} USD** (n = {s['n']})")
    L.append(">")
    L.append(
        "> La mediana ordena las zonas de forma distinta a la media: La Víbora "
        "sigue primera, pero su ventaja se reduce mucho porque la mediana no se "
        "deja arrastrar por el anuncio de $180,000."
    )
    L.append("")
    L.append(
        f"**B4. ¿La brecha La Víbora–Lawton se mantiene al usar medianas?** 🟡 "
        f"(n = {stats_zona_5['La Víbora']['n']} y {stats_zona_5['Lawton']['n']})"
    )
    L.append("")
    L.append(
        f"> **No se mantiene con la misma magnitud.** Por media, La Víbora "
        f"(${fmt(stats_zona_5['La Víbora']['mean'])} USD) supera a Lawton "
        f"(${fmt(stats_zona_5['Lawton']['mean'])} USD) en "
        f"**${fmt(stats_zona_5['La Víbora']['mean'] - stats_zona_5['Lawton']['mean'])} USD**. "
        f"Por mediana, la diferencia es de solo "
        f"**${fmt(stats_zona_5['La Víbora']['median'] - stats_zona_5['Lawton']['median'])} USD** "
        f"(${fmt(stats_zona_5['La Víbora']['median'])} frente a "
        f"${fmt(stats_zona_5['Lawton']['median'])}). La brecha por media es unas "
        f"{(stats_zona_5['La Víbora']['mean'] - stats_zona_5['Lawton']['mean']) / (stats_zona_5['La Víbora']['median'] - stats_zona_5['Lawton']['median']):.1f} veces "
        f"mayor que la brecha por mediana. El anuncio de $180,000 USD en La Víbora "
        f"(y su P90 de ${fmt(stats_zona_5['La Víbora']['p90'])} USD) explica gran "
        f"parte de la diferencia: la media describe el extremo alto, no el precio "
        f"típico. Para comparar barrios conviene usar la mediana."
    )
    L.append("")
    L.append(
        f"**B5. ¿La falta de zona afecta igual a compra y alquiler?** ✅ "
        f"(censo de operaciones)"
    )
    L.append("")
    L.append(
        f"> No. La falta de zona es más grave en alquiler: "
        f"**{len(alquileres) - sum(1 for a in alquileres if a['_zona'] != 'No especificado')} de {len(alquileres)} "
        f"({pct(len(alquileres) - sum(1 for a in alquileres if a['_zona'] != 'No especificado'), len(alquileres)):.1f}%)** "
        f"alquileres no especifican zona, frente a "
        f"**{len(ventas) - sum(1 for a in ventas if a['_zona'] != 'No especificado')} de {len(ventas)} "
        f"({pct(len(ventas) - sum(1 for a in ventas if a['_zona'] != 'No especificado'), len(ventas)):.1f}%)** "
        f"ventas y **{len(sin_clasificar) - sum(1 for a in sin_clasificar if a['_zona'] != 'No especificado')} de {len(sin_clasificar)} "
        f"({pct(len(sin_clasificar) - sum(1 for a in sin_clasificar if a['_zona'] != 'No especificado'), len(sin_clasificar)):.1f}%)** "
        f"anuncios sin operación declarada. El alquiler combina las dos opacidades: "
        f"casi nunca declara precio y casi nunca declara zona."
    )
    L.append("")

    # ---------------- BLOQUE C ----------------
    L.append("### Bloque C: Dolarización")
    L.append("")
    L.append(
        f"**C1. ¿Qué porcentaje de anuncios con moneda declarada está en USD?** ✅ "
        f"(n = {len(con_moneda)})"
    )
    L.append("")
    L.append(
        f"> **{usd_declarada} de {len(con_moneda)} ({pct_usd_declarada:.1f}%)**. "
        f"El único anuncio con moneda declarada que no está en USD es un "
        f"alquiler en CUP (50,000 CUP). Los {sin_precio_n} anuncios sin precio no "
        f"declaran moneda y quedan fuera de este denominador."
    )
    L.append("")
    L.append(
        f"**C2. ¿Qué porcentaje del total está en USD?** ✅ (n = {total})"
    )
    L.append("")
    L.append(
        f"> **{usd_declarada} de {total} ({pct_usd_total:.1f}%)**. El resto se "
        f"reparte entre {sin_precio_n} anuncios sin precio ({pct(sin_precio_n, total):.1f}%) "
        f"y 1 anuncio en CUP ({pct(1, total):.1f}%). La dolarización es alta "
        f"incluso cuando se cuenta a los anuncios que no declaran precio."
    )
    L.append("")
    L.append(
        f"**C3. ¿La dolarización varía por tipo de inmueble?** ✅ "
        f"(anuncios con precio)"
    )
    L.append("")
    for t in ["Casa", "Apartamento", "Inmueble", "Cuarto"]:
        grupo = [a for a in anuncios if a["_tipo"] == t and a.get("precio") is not None]
        usd_grupo = [a for a in grupo if str(a.get("moneda", "")).upper() == "USD"]
        if grupo:
            L.append(
                f"> - {t}: **{len(usd_grupo)} de {len(grupo)} "
                f"({pct(len(usd_grupo), len(grupo)):.1f}%)** en USD"
            )
    L.append(">")
    L.append(
        "> La dolarización es prácticamente total en todos los tipos con precio. "
        "El único anuncio en CUP es un inmueble sin tipo específico (clasificado "
        "como «Inmueble») y de alquiler. No hay un tipo de inmueble que funcione "
        "principalmente en CUP."
    )
    L.append("")
    L.append(
        f"**C4. ¿La dolarización varía por zona?** ✅ "
        f"({sum(1 for a in usd if a['_zona'] != 'No especificado')} anuncios con precio y zona)"
    )
    L.append("")
    L.append(
        f"> **No se puede medir variación territorial:** los "
        f"**{sum(1 for a in usd if a['_zona'] != 'No especificado')} anuncios** "
        f"con precio y zona identificada están **todos en USD (100%)**. El único "
        f"anuncio en CUP no especifica zona. La conclusión no es que todas las "
        f"zonas estén dolarizadas por igual, sino que la base no permite "
        f"compararlas: la ausencia de zona en el anuncio en CUP impide saber si "
        f"hay barrios con precios en CUP."
    )
    L.append("")
    L.append(
        f"**C5. ¿Cuánto podría variar la dolarización si los anuncios sin precio "
        f"fueran CUP o USD?** ✅ (cota inferior y superior)"
    )
    L.append("")
    L.append(
        f"> La proporción de USD en el total está acotada entre "
        f"**{usd_min:.1f}%** y **{usd_max:.1f}%**. El límite inferior supone que "
        f"los {sin_precio_n} anuncios sin precio están en CUP; el superior, que "
        f"están en USD. La diferencia entre ambos escenarios es de "
        f"**{usd_max - usd_min:.1f} puntos porcentuales**. La ausencia de precio "
        f"y moneda impide conocer el valor exacto, pero permite afirmar que, en "
        f"cualquier escenario, más de cuatro quintas partes del mercado está en "
        f"USD o podría estarlo. Esa cota es un resultado, no una especulación."
    )
    L.append("")

    # ---------------- BLOQUE D ----------------
    L.append("### Bloque D: Opacidad de la información")
    L.append("")
    L.append(
        f"**D1. ¿Qué porcentaje no declara precio?** ✅ (n = {total})"
    )
    L.append("")
    L.append(
        f"> **{sin_precio_n} de {total} ({pct(sin_precio_n, total):.1f}%)**. "
        f"Son anuncios que no permiten comparar precios sin contactar al "
        f"vendedor. La ausencia es especialmente alta en alquiler (A4)."
    )
    L.append("")
    L.append(
        f"**D2. ¿Qué porcentaje no especifica zona?** ✅ (n = {total})"
    )
    L.append("")
    L.append(
        f"> **{sin_zona_n} de {total} ({pct(sin_zona_n, total):.1f}%)**. "
        f"Sin zona no se puede verificar la ubicación ni comparar barrios. Es la "
        f"dimensión más opaca del mercado: casi tres de cada cinco anuncios "
        f"omiten este dato."
    )
    L.append("")
    L.append(
        f"**D3. ¿Cuántos anuncios carecen de precio y zona a la vez?** ✅ "
        f"(n = {total})"
    )
    L.append("")
    L.append(
        f"> **{ambos_n} de {total} ({pct(ambos_n, total):.1f}%)**. En estos "
        f"anuncios no se puede saber ni cuánto cuesta ni dónde está. Son el "
        f"núcleo más opaco del mercado digital."
    )
    L.append("")
    L.append(
        f"**D4. ¿Qué porcentaje tiene información mínima completa (precio + zona)?** "
        f"✅ (n = {total})"
    )
    L.append("")
    L.append(
        f"> **{completo_n} de {total} ({pct(completo_n, total):.1f}%)**. Solo "
        f"algo más de un tercio de los anuncios permite cruzar precio y zona. "
        f"Ese es el subconjunto sobre el que se pueden hacer comparaciones "
        f"territoriales relativamente sólidas; el resto queda fuera por falta de "
        f"un dato básico."
    )
    L.append("")
    L.append(
        f"**D5. ¿La opacidad es mayor en alquiler que en venta?** ✅ "
        f"(censo de operaciones)"
    )
    L.append("")
    L.append(
        f"> Sí, sobre todo en precio. En **alquiler**, "
        f"**{len(alquileres) - len(alquileres_con_precio)} de {len(alquileres)} "
        f"({pct(len(alquileres) - len(alquileres_con_precio), len(alquileres)):.1f}%)** "
        f"no declaran precio y "
        f"**{len(alquileres) - sum(1 for a in alquileres if a['_zona'] != 'No especificado')} de {len(alquileres)} "
        f"({pct(len(alquileres) - sum(1 for a in alquileres if a['_zona'] != 'No especificado'), len(alquileres)):.1f}%)** "
        f"no declaran zona. En **venta**, "
        f"**{len(ventas) - len(ventas_con_precio)} de {len(ventas)} "
        f"({pct(len(ventas) - len(ventas_con_precio), len(ventas)):.1f}%)** "
        f"no declaran precio y "
        f"**{len(ventas) - sum(1 for a in ventas if a['_zona'] != 'No especificado')} de {len(ventas)} "
        f"({pct(len(ventas) - sum(1 for a in ventas if a['_zona'] != 'No especificado'), len(ventas)):.1f}%)** "
        f"no declaran zona. El alquiler es el segmento más opaco en ambas "
        f"dimensiones."
    )
    L.append("")

    # ---------------- BLOQUE E ----------------
    L.append("### Bloque E: Prácticas informales")
    L.append("")
    L.append(
        f"**E1. ¿Qué porcentaje usa lenguaje informal («oportunidad», «ganga», "
        f"«permuta», «intercambio» o «cambio»)?** ✅ (n = {total})"
    )
    L.append("")
    L.append(
        f"> **{len(informal)} de {total} ({pct(len(informal), total):.1f}%)**. "
        f"El lenguaje informal no es mayoritario, pero aparece en uno de cada "
        f"nueve anuncios. Es una señal de prácticas de intermediación y de "
        f"negociación que no se ajustan del todo al formato de una oferta "
        f"inmobiliaria formal."
    )
    L.append("")
    L.append(
        f"**E2. ¿Qué palabras informales dominan?** ✅ (n = {len(informal)})"
    )
    L.append("")
    for p, c in palabras_inf.most_common():
        L.append(f"> - «{p}»: **{c} {unidad(c)}**")
    L.append(">")
    L.append(
        "> «Oportunidad» es la palabra dominante; «permuta» y «cambio» aparecen "
        "en pocos anuncios. Las palabras «ganga» e «intercambio» no aparecen en "
        "la base. La informalidad se expresa más como reclamo comercial que como "
        "trueque explícito."
    )
    L.append("")
    L.append(
        f"**E3. ¿Los anuncios informales declaran precio más que los neutros?** "
        f"🟡 (n = {len(informal)} informales)"
    )
    L.append("")
    L.append(
        f"> **{informal_con_precio} de {len(informal)} "
        f"({pct(informal_con_precio, len(informal)):.1f}%)** de los informales "
        f"declaran precio, frente a **{neutros_con_precio} de {len(neutros)} "
        f"({pct(neutros_con_precio, len(neutros)):.1f}%)** de los neutros. La "
        f"diferencia es de **{pct(informal_con_precio, len(informal)) - pct(neutros_con_precio, len(neutros)):.1f} puntos porcentuales**. "
        f"El subgrupo informal es pequeño (n = {len(informal)}), así que la "
        f"diferencia es indicativa: no permite concluir que el lenguaje informal "
        f"implique mayor transparencia."
    )
    L.append("")
    L.append(
        f"**E4. ¿La informalidad se concentra en alguna operación?** ✅ "
        f"(censo de {len(informal)} anuncios informales)"
    )
    L.append("")
    for op in ["Venta", "Alquiler", "Sin clasificar"]:
        c = informal_por_op.get(op, 0)
        L.append(f"> - {op}: **{c} de {len(informal)} ({pct(c, len(informal)):.1f}%)**")
    L.append(">")
    L.append(
        "> La informalidad aparece en **venta** y en **anuncios sin operación "
        "declarada**; **no aparece en alquiler**. Esto refuerza la lectura de "
        "que el alquiler se gestiona por otros canales (contacto directo, redes "
        "cerradas) y no necesita el reclamo de «oportunidad» en el título."
    )
    L.append("")
    L.append(
        f"**E5. ¿Los anuncios sin clasificar son más opacos que los clasificados?** "
        f"✅ (censo de operaciones)"
    )
    L.append("")
    L.append(
        f"> **No.** Los anuncios sin operación declarada son, en esta base, más "
        f"completos que las ventas explícitas: "
        f"**{len(sin_clasificar) - sum(1 for a in sin_clasificar if a.get('precio') is None)} de {len(sin_clasificar)} "
        f"({pct(len(sin_clasificar) - sum(1 for a in sin_clasificar if a.get('precio') is None), len(sin_clasificar)):.1f}%)** "
        f"declaran precio y "
        f"**{sum(1 for a in sin_clasificar if a['_zona'] != 'No especificado')} de {len(sin_clasificar)} "
        f"({pct(sum(1 for a in sin_clasificar if a['_zona'] != 'No especificado'), len(sin_clasificar)):.1f}%)** "
        f"declaran zona. En venta, esas proporciones son "
        f"**{pct(len(ventas_con_precio), len(ventas)):.1f}%** y "
        f"**{pct(sum(1 for a in ventas if a['_zona'] != 'No especificado'), len(ventas)):.1f}%**; "
        f"en alquiler, **{pct(len(alquileres_con_precio), len(alquileres)):.1f}%** y "
        f"**{pct(sum(1 for a in alquileres if a['_zona'] != 'No especificado'), len(alquileres)):.1f}%**. "
        f"El grupo realmente opaco es el alquiler, no el de los anuncios sin "
        f"clasificar. La falta de etiqueta de operación no equivale a falta de "
        f"información."
    )
    L.append("")

    # ---------------- BLOQUE F ----------------
    L.append("### Bloque F: Tipos de inmueble y accesibilidad")
    L.append("")
    L.append(
        f"**F1. ¿Qué tipo de inmueble se publica más?** ✅ (n = {total})"
    )
    L.append("")
    for t, c in tipos.most_common():
        L.append(f"> - {t}: **{c} {unidad(c)}** ({pct(c, total):.1f}%)")
    L.append(">")
    L.append(
        "> La casa es el tipo más publicado, seguida del apartamento. Entre "
        "ambos suman la mayor parte de la oferta; el «Inmueble» agrupa títulos "
        "que no especifican un tipo concreto."
    )
    L.append("")
    L.append(
        f"**F2. ¿Qué tipo tiene el precio medio más bajo?** ✅ "
        f"(n = {stats_tipo['Apartamento']['n']} apartamentos)"
    )
    L.append("")
    for t in sorted(tipos_comparables, key=lambda x: stats_tipo[x]["mean"]):
        s = stats_tipo[t]
        L.append(f"> - {t}: media **${fmt(s['mean'])} USD** (n = {s['n']})")
    L.append(">")
    L.append(
        f"> El **apartamento** es la opción más accesible entre los tipos con "
        f"n ≥ 10: su media es **${fmt(stats_tipo['Apartamento']['mean'])} USD**, "
        f"frente a **${fmt(stats_tipo['Casa']['mean'])} USD** de la casa y "
        f"**${fmt(stats_tipo['Inmueble']['mean'])} USD** del inmueble sin tipo "
        f"específico. La diferencia entre apartamento y casa es de "
        f"**${fmt(stats_tipo['Casa']['mean'] - stats_tipo['Apartamento']['mean'])} USD**: "
        f"el apartamento cuesta aproximadamente "
        f"**{100 * (stats_tipo['Casa']['mean'] - stats_tipo['Apartamento']['mean']) / stats_tipo['Casa']['mean']:.1f}% menos** "
        f"que la casa en promedio. El cuarto tiene n = 1 y no se usa para comparar."
    )
    L.append("")
    L.append(
        f"**F3. ¿Qué tipo tiene la mediana más baja?** ✅ "
        f"(n = {stats_tipo['Apartamento']['n']} apartamentos)"
    )
    L.append("")
    for t in sorted(tipos_comparables, key=lambda x: stats_tipo[x]["median"]):
        s = stats_tipo[t]
        L.append(f"> - {t}: mediana **${fmt(s['median'])} USD** (n = {s['n']})")
    L.append(">")
    L.append(
        f"> El **apartamento** también tiene la mediana más baja: "
        f"**${fmt(stats_tipo['Apartamento']['median'])} USD**, frente a "
        f"**${fmt(stats_tipo['Casa']['median'])} USD** de la casa y "
        f"**${fmt(stats_tipo['Inmueble']['median'])} USD** del inmueble. La "
        f"mediana del apartamento es la mitad de la mediana de la casa. La "
        f"conclusión se mantiene al pasar de la media a la mediana, lo que la "
        f"hace más robusta frente a valores extremos."
    )
    L.append("")
    L.append(
        f"**F4. ¿La diferencia se mantiene en el rango P10–P90?** ✅ "
        f"(n = {stats_tipo['Apartamento']['n']}, {stats_tipo['Casa']['n']} y "
        f"{stats_tipo['Inmueble']['n']})"
    )
    L.append("")
    for t in sorted(tipos_comparables, key=lambda x: stats_tipo[x]["p10"]):
        s = stats_tipo[t]
        L.append(
            f"> - {t}: P10 **${fmt(s['p10'])} USD**, mediana "
            f"**${fmt(s['median'])} USD**, P90 **${fmt(s['p90'])} USD** (n = {s['n']})"
        )
    L.append(">")
    L.append(
        f"> Sí. El apartamento es más barato en los tres puntos de la "
        f"distribución: su P10 (${fmt(stats_tipo['Apartamento']['p10'])}) es "
        f"menor que el de la casa (${fmt(stats_tipo['Casa']['p10'])}) y que el "
        f"del inmueble (${fmt(stats_tipo['Inmueble']['p10'])}); su P90 "
        f"(${fmt(stats_tipo['Apartamento']['p90'])}) también es menor que el de "
        f"la casa (${fmt(stats_tipo['Casa']['p90'])}) y el del inmueble "
        f"(${fmt(stats_tipo['Inmueble']['p90'])}). El rango del apartamento es "
        f"más estrecho y desplazado hacia abajo. El P90 del apartamento "
        f"(${fmt(stats_tipo['Apartamento']['p90'])}) supera la mediana de la "
        f"casa (${fmt(stats_tipo['Casa']['median'])}), pero sigue muy por debajo "
        f"del P90 de la casa: las distribuciones se solapan, aunque el "
        f"apartamento es consistentemente más accesible."
    )
    L.append("")
    L.append(
        f"**F5. ¿Qué tipo concentra más opacidad de precio y zona?** ✅ "
        f"(censo por tipo)"
    )
    L.append("")
    for t in ["Inmueble", "Casa", "Apartamento", "Cuarto"]:
        grupo = [a for a in anuncios if a["_tipo"] == t]
        sp = sum(1 for a in grupo if a.get("precio") is None)
        sz = sum(1 for a in grupo if a["_zona"] == "No especificado")
        L.append(
            f"> - {t}: **{sp} de {len(grupo)} ({pct(sp, len(grupo)):.1f}%)** sin "
            f"precio; **{sz} de {len(grupo)} ({pct(sz, len(grupo)):.1f}%)** sin zona"
        )
    L.append(">")
    L.append(
        "> El **Inmueble** (títulos que no especifican un tipo concreto) "
        "concentra la mayor opacidad entre los tipos comparables: 22.2% sin "
        "precio y 70.4% sin zona. La casa tiene la menor proporción sin precio "
        "(6.5%), pero sigue teniendo 61.3% sin zona. El cuarto muestra 50% y "
        "100%, pero solo son 2 anuncios: es evidencia descriptiva, no una "
        "conclusión. La opacidad de zona afecta a todos los tipos; la de precio "
        "se concentra en el Inmueble y el Apartamento."
    )
    L.append("")

    # ------------------------------------------------------------------
    # La ausencia como hallazgo
    # ------------------------------------------------------------------
    L.append("## La ausencia como hallazgo")
    L.append("")
    L.append(
        "Los indicadores de ausencia no son un apéndice: son resultados del "
        "estudio. La tabla reúne los principales."
    )
    L.append("")
    L.append("| Indicador | Resultado | Lectura social |")
    L.append("|---|---:|---|")
    L.append(
        f"| Anuncios sin precio | **{sin_precio_n}/{total} ({pct(sin_precio_n, total):.1f}%)** | "
        f"No se puede comparar sin contactar al vendedor. |"
    )
    L.append(
        f"| Anuncios sin zona | **{sin_zona_n}/{total} ({pct(sin_zona_n, total):.1f}%)** | "
        f"No se puede verificar la ubicación ni comparar barrios. |"
    )
    L.append(
        f"| Sin precio y sin zona | **{ambos_n}/{total} ({pct(ambos_n, total):.1f}%)** | "
        f"Anuncios completamente opacos en precio y ubicación. |"
    )
    L.append(
        f"| Información completa (precio + zona) | **{completo_n}/{total} ({pct(completo_n, total):.1f}%)** | "
        f"Solo un tercio permite un análisis mínimo. |"
    )
    L.append(
        f"| Alquileres sin precio | **{len(alquileres) - len(alquileres_con_precio)}/{len(alquileres)} "
        f"({pct(len(alquileres) - len(alquileres_con_precio), len(alquileres)):.1f}%)** | "
        f"El mercado de alquiler es casi invisible en precios. |"
    )
    L.append(
        f"| Alquileres sin zona | **{len(alquileres) - sum(1 for a in alquileres if a['_zona'] != 'No especificado')}/{len(alquileres)} "
        f"({pct(len(alquileres) - sum(1 for a in alquileres if a['_zona'] != 'No especificado'), len(alquileres)):.1f}%)** | "
        f"Tampoco se puede ubicar la oferta de alquiler. |"
    )
    L.append(
        f"| Anuncios sin operación declarada | **{len(sin_clasificar)}/{total} "
        f"({pct(len(sin_clasificar), total):.1f}%)** | "
        f"Más de la mitad no dice si se vende o se alquila. |"
    )
    L.append(
        f"| Sin característica física explícita | **{len(sin_feature)}/{total} "
        f"({pct(len(sin_feature), total):.1f}%)** | "
        f"La descripción del inmueble es mínima. |"
    )
    L.append(
        f"| Totalmente opacos (sin precio, zona ni característica) | "
        f"**{len(totalmente_opacos)}/{total} ({pct(len(totalmente_opacos), total):.1f}%)** | "
        f"No hay ningún dato útil para comparar. |"
    )
    L.append(
        f"| Sin moneda declarada | **{sin_precio_n}/{total} "
        f"({pct(sin_precio_n, total):.1f}%)** | "
        f"No se sabe si el precio, cuando exista, será en USD o CUP. |"
    )
    L.append("")
    L.append(
        "La lectura social es directa: la opacidad no afecta a todos por igual. "
        "Quien puede llamar, visitar y verificar accede a la información que "
        "falta; quien depende del anuncio para comparar queda en desventaja. "
        "El alquiler, además, es el segmento con mayor ausencia de precio y zona, "
        "lo que sugiere que una parte importante de ese mercado opera por canales "
        "informales o de confianza previa."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Conclusiones
    # ------------------------------------------------------------------
    L.append("## Conclusiones")
    L.append("")
    L.append(
        f"1. **La base corregida es de {total} anuncios.** La versión anterior "
        f"(171) incluía 37 anuncios de otros municipios; sus cifras no eran "
        f"estrictamente de Diez de Octubre y quedan supersedidas. El filtro "
        f"estricto también descartó {rechazados_precio} anuncios con precio "
        f"inferior a 1,000 USD."
    )
    L.append(
        f"2. **El mercado está dolarizado.** {usd_declarada} de {len(con_moneda)} "
        f"anuncios con moneda declarada ({pct_usd_declarada:.1f}%) están en USD; "
        f"en el total, la proporción es {pct_usd_total:.1f}% y la cota superior "
        f"posible es {usd_max:.1f}%. Quien no tiene divisas enfrenta una barrera "
        f"de acceso estructural."
    )
    L.append(
        f"3. **El precio de compra típico es mucho menor que el promedio.** La "
        f"mediana de las ventas con precio USD es ${fmt(stats_venta['median'])} "
        f"USD, mientras que la media es ${fmt(stats_venta['mean'])} USD. El 80% "
        f"central está entre ${fmt(stats_venta['p10'])} y "
        f"${fmt(stats_venta['p90'])} USD (n = {stats_venta['n']}). La media sola "
        f"sobreestima el precio al que se concentra la oferta."
    )
    L.append(
        f"4. **El alquiler no tiene precio estimable.** Solo "
        f"{len(alquileres_con_precio)} de {len(alquileres)} alquileres declara "
        f"precio, y ninguno en USD. No se puede responder cuánto cuesta alquilar "
        f"con esta base; esa ausencia es un hallazgo sobre el funcionamiento del "
        f"segmento."
    )
    L.append(
        f"5. **La desigualdad territorial existe, pero hay que medirla con "
        f"medianas.** Las cuatro zonas principales concentran "
        f"{pct(top4_total, total_con_zona):.1f}% de los anuncios con zona. La "
        f"Víbora tiene la media más alta (${fmt(stats_zona_5[zona_cara]['mean'])} "
        f"USD, n = {stats_zona_5[zona_cara]['n']}), pero su mediana es "
        f"${fmt(stats_zona_5[zona_cara]['median'])} USD; frente a Lawton, la "
        f"brecha por media es ${fmt(stats_zona_5['La Víbora']['mean'] - stats_zona_5['Lawton']['mean'])} "
        f"USD y por mediana solo ${fmt(stats_zona_5['La Víbora']['median'] - stats_zona_5['Lawton']['median'])} "
        f"USD. El anuncio de $180,000 USD infla la media."
    )
    L.append(
        f"6. **La opacidad es masiva en zona y grave en precio.** "
        f"{pct(sin_zona_n, total):.1f}% no especifica zona, "
        f"{pct(sin_precio_n, total):.1f}% no declara precio y solo "
        f"{pct(completo_n, total):.1f}% permite cruzar ambos datos. El "
        f"{pct(ambos_n, total):.1f}% no tiene ninguno de los dos. La ausencia de "
        f"información es un mecanismo de desigualdad: quien no puede verificar "
        f"queda expuesto a la intermediación."
    )
    L.append(
        f"7. **La informalidad es visible pero no domina.** "
        f"{pct(len(informal), total):.1f}% usa lenguaje de oportunidad, permuta "
        f"o cambio. Se concentra en venta y en anuncios sin operación declarada; "
        f"no aparece en alquiler. Los informales declaran precio algo más que los "
        f"neutros ({pct(informal_con_precio, len(informal)):.1f}% frente a "
        f"{pct(neutros_con_precio, len(neutros)):.1f}%), pero el subgrupo es "
        f"pequeño y la diferencia no es concluyente."
    )
    L.append(
        f"8. **El apartamento es la opción más accesible.** Su media es "
        f"${fmt(stats_tipo['Apartamento']['mean'])} USD y su mediana "
        f"${fmt(stats_tipo['Apartamento']['median'])} USD (n = "
        f"{stats_tipo['Apartamento']['n']}), frente a la casa "
        f"(${fmt(stats_tipo['Casa']['mean'])} y "
        f"${fmt(stats_tipo['Casa']['median'])} USD; n = "
        f"{stats_tipo['Casa']['n']}). La diferencia se mantiene en P10–P90. "
        f"Entre los tipos con n ≥ 10, el Inmueble sin tipo específico es el más "
        f"opaco y el más caro en media, lo que sugiere que la falta de información "
        f"sobre el tipo se asocia con operaciones de mayor valor."
    )
    L.append("")
    L.append(
        "En conjunto, el mercado digital de Diez de Octubre no es un espacio "
        "transparente de precios y ubicaciones: es un mercado segmentado por "
        "divisas, por acceso a información y por barrios. La base corregida "
        "permite afirmar esto con mayor rigor que la versión anterior, y también "
        "permite identificar qué no se puede saber: el precio del alquiler, la "
        "zona de la mayoría de los anuncios y la operación de más de la mitad. "
        "Ese límite es parte del resultado."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Limitaciones
    # ------------------------------------------------------------------
    L.append("## Limitaciones")
    L.append("")
    L.append(
        "- **Fuente única:** los datos del informe provienen solo de Revolico; "
        "no representan todo el mercado inmobiliario de Diez de Octubre. Facebook "
        "se exploró (43 publicaciones; 42 tras filtro), pero no se integró por "
        "incompatibilidad de esquema y de normalización municipal."
    )
    L.append(
        f"- **Muestra:** {total} anuncios es una base pequeña y no "
        f"necesariamente representativa del universo de viviendas del municipio. "
        f"No hay serie temporal: el corte es único ({fecha_corte})."
    )
    L.append(
        "- **Clasificación por palabras clave:** el tipo, la zona y la operación "
        "se infieren del título y del enlace. Puede haber errores de asignación, "
        "especialmente en títulos ambiguos o sin palabras clave."
    )
    L.append(
        "- **Campos ausentes:** no hay datos de metros cuadrados, estado legal, "
        "número de baños, año de construcción, vendedor o agencia. No se puede "
        "calcular precio por m² ni distinguir particulares de intermediarios."
    )
    L.append(
        f"- **Alquiler:** solo {len(alquileres)} anuncios, {len(alquileres_con_precio)} "
        f"con precio y ninguno en USD. No se puede estimar un precio de alquiler "
        f"ni comparar compra y alquiler."
    )
    L.append(
        f"- **Zonas:** solo {total_con_zona} de {total} anuncios "
        f"({pct(total_con_zona, total):.1f}%) especifican zona. Los promedios "
        f"por barrio se basan en subgrupos pequeños (n = 5–14) y deben leerse "
        f"como evidencia descriptiva."
    )
    L.append(
        "- **CUP:** el único precio en CUP no se convierte a USD porque no se "
        "dispone de un tipo de cambio oficial o de mercado claramente definido "
        "para el corte. Se reporta como hallazgo, no como precio comparable."
    )
    L.append(
        "- **Sesgo de publicación:** los anuncios que no se publican, o que se "
        "publican en canales cerrados, no aparecen en la base. La opacidad "
        "medida es la del mercado digital visible, no la del mercado total."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Firma
    # ------------------------------------------------------------------
    L.append("---")
    L.append("")
    L.append("**Proyecto de Ciencia de Datos — Universidad de La Habana**")
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
    print(f"Ventas USD: n={stats_venta['n']} | media={fmt(stats_venta['mean'])} | "
          f"mediana={fmt(stats_venta['median'])} | "
          f"P10-P90={fmt(stats_venta['p10'])}-{fmt(stats_venta['p90'])}")
    print(f"Preguntas: 30 (A1-A5, B1-B5, C1-C5, D1-D5, E1-E5, F1-F5)")


if __name__ == "__main__":
    main()
