#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el informe final A-F del mercado inmobiliario digital de Diez de Octubre.

Base de datos:
    datos/limpios/unificado_confirmados_diez_octubre.json
    122 publicaciones confirmadas dentro del municipio por la verificación
    espacial con el polígono DPA 23.09 de datos/geo/lha.geojson:
    83 de Revolico + 39 de Facebook.

    La base de 134 anuncios de Revolico era una muestra *etiquetada* como
    Diez de Octubre, no verificada: 46 fichas declaraban otro municipio, 8 de
    ellas tenían un título con un reparto interno que las confirma y 5 no eran
    verificables. Este informe sustituye aquel universo por el de 122
    publicaciones confirmadas, aplicando el título como evidencia principal.

Entrada auxiliar:
    datos/limpios/verificacion_municipal_unificado.json

Salida:
    analisis/informe_final.md

Estructura:
    - Verificación municipal y cambio de universo.
    - 30 preguntas en seis bloques: A precios, B territorio, C dolarización,
      D opacidad, E informalidad, F tipos de inmueble.
    - La ausencia de información se reporta como hallazgo, no solo como
      limitación.
"""

import json
import math
import os
import statistics
from collections import Counter, defaultdict
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_CONFIRMADOS = os.path.join(
    RAIZ, "datos", "limpios", "unificado_confirmados_diez_octubre.json"
)
INPUT_VERIFICACION = os.path.join(
    RAIZ, "datos", "limpios", "verificacion_municipal_unificado.json"
)
INPUT_VERIF_REVOLICO = os.path.join(
    RAIZ, "datos", "limpios", "verificacion_municipal_revolico.json"
)
INPUT_VERIF_FACEBOOK = os.path.join(
    RAIZ, "datos", "limpios", "verificacion_municipal_facebook.json"
)
INPUT_DESCARTADOS = os.path.join(
    RAIZ, "datos", "limpios", "descartados_diez_octubre.json"
)
OUTPUT_FILE = os.path.join(RAIZ, "analisis", "informe_final.md")
REPORTE_VERIFICACION = "analisis/verificacion_municipal_geojson_20261104.md"

FEATURES = [
    "garaje", "garage", "patio", "azotea", "terraza",
    "balcón", "balcon", "baño", "bano", "cuarto", "habitación", "habitacion",
]

PALABRAS_INFORMALES = [
    "oportunidad", "ganga", "permuta", "intercambio", "cambio",
]

# Barrios y repartos usados como respaldo cuando el campo normalizado `zona`
# viene vacío pero el texto declarado del anuncio sí los menciona. El orden
# importa: los nombres más específicos van primero.
ZONAS = [
    ("Santos Suárez", ["santos suárez", "santos suarez", "santo suárez", "santo suarez"]),
    ("La Víbora", ["la víbora", "la vibora", "víbora", "vibora"]),
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


# ---------------------------------------------------------------------------
# Carga y normalización
# ---------------------------------------------------------------------------

def cargar_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Clasificadores reutilizados por limpiar_facebook.py y
# mezclar_facebook_revolico.py. Se conservan con la misma lógica de la base
# unificada para que regenerar el pipeline no cambie los registros.
# ---------------------------------------------------------------------------

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


def texto_anuncio(anuncio):
    """Todo el texto declarado, en minúsculas, para buscar señales."""
    detalles = anuncio.get("detalles_propiedad") or {}
    publicacion = anuncio.get("publicacion") or {}
    partes = [
        publicacion.get("titulo", ""),
        publicacion.get("enlace", ""),
        publicacion.get("grupo", ""),
        detalles.get("ubicacion", ""),
        detalles.get("zona", ""),
    ]
    for clave in ("distribucion", "detalles_estructura"):
        partes += detalles.get(clave) or []
    partes += anuncio.get("servicios_y_caracteristicas") or []
    partes += anuncio.get("equipamiento_incluido") or []
    return " ".join(str(p) for p in partes if p).lower()


def zona_normalizada(anuncio, texto):
    detalles = anuncio.get("detalles_propiedad") or {}
    zona = (detalles.get("zona") or "").strip()
    if zona and zona.lower() not in ("no especificado", "sin especificar"):
        return zona
    for nombre, variantes in ZONAS:
        if any(v in texto for v in variantes):
            return nombre
    return "No especificado"


def monto_de_precio(precio):
    """Usa `monto` y, si falta, `monto_actual` (caso Facebook con rebaja)."""
    if not isinstance(precio, dict):
        return None
    if precio.get("monto") is not None:
        return precio["monto"]
    return precio.get("monto_actual")


def cargar_anuncios_confirmados():
    anuncios = cargar_json(INPUT_CONFIRMADOS)
    verificacion = cargar_json(INPUT_VERIFICACION)

    # Defensivo: la base de confirmados ya viene filtrada, pero se comprueba
    # el resultado para que el informe no incluya un registro no confirmado.
    anuncios = [
        a for a in anuncios
        if (a.get("verificacion_municipal") or {}).get("resultado") == "SÍ"
    ]

    for a in anuncios:
        detalles = a.get("detalles_propiedad") or {}
        precio = a.get("precio") or {}
        publicacion = a.get("publicacion") or {}
        texto = texto_anuncio(a)

        a["_fuente"] = a.get("fuente") or "desconocida"
        a["_tipo"] = detalles.get("tipo") or "Inmueble"
        a["_zona"] = zona_normalizada(a, texto)
        a["_op"] = a.get("operacion") or "Sin clasificar"
        a["_precio"] = monto_de_precio(precio)
        a["_moneda"] = (precio.get("moneda") or "").upper()
        a["_texto"] = texto
        a["_titulo"] = publicacion.get("titulo") or ""

    return anuncios, verificacion


# ---------------------------------------------------------------------------
# Utilidades estadísticas
# ---------------------------------------------------------------------------

def percentil(valores_ordenados, p):
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


def f0(valor):
    return f"{valor:,.0f}"


def pct(n, d):
    return 100.0 * n / d if d else 0.0


def unidad(n):
    return "anuncio" if n == 1 else "anuncios"


def tiene_feature(texto):
    return any(f in (texto or "").lower() for f in FEATURES)


def contar_resultados(registros, solo_base_limpia=False):
    if solo_base_limpia:
        registros = [r for r in registros if r.get("en_base_limpia", True)]
    return Counter(r.get("resultado") for r in registros)


# ---------------------------------------------------------------------------
# Informe
# ---------------------------------------------------------------------------

def main():
    anuncios, verificacion = cargar_anuncios_confirmados()
    total = len(anuncios)

    # Subconjuntos principales
    con_precio = [a for a in anuncios if a["_precio"] is not None]
    sin_precio = [a for a in anuncios if a["_precio"] is None]
    usd = [a for a in anuncios if a["_precio"] is not None and a["_moneda"] == "USD"]
    cup = [a for a in anuncios if a["_precio"] is not None and a["_moneda"] == "CUP"]
    con_moneda = [a for a in anuncios if a["_moneda"] in ("USD", "CUP")]

    ventas = [a for a in anuncios if a["_op"] == "Venta"]
    alquileres = [a for a in anuncios if a["_op"] == "Alquiler"]
    sin_clasificar = [a for a in anuncios if a["_op"] == "Sin clasificar"]

    ventas_con_precio = [a for a in ventas if a["_precio"] is not None]
    ventas_usd = [a for a in ventas if a["_precio"] is not None and a["_moneda"] == "USD"]
    alquileres_con_precio = [a for a in alquileres if a["_precio"] is not None]
    alquileres_usd = [a for a in alquileres if a["_precio"] is not None and a["_moneda"] == "USD"]

    stats_usd = stats([a["_precio"] for a in usd])
    stats_venta = stats([a["_precio"] for a in ventas_usd])

    # Zonas
    zonas = Counter(a["_zona"] for a in anuncios if a["_zona"] != "No especificado")
    total_con_zona = sum(zonas.values())
    sin_zona_n = sum(1 for a in anuncios if a["_zona"] == "No especificado")

    precios_zona = defaultdict(list)
    for a in usd:
        if a["_zona"] != "No especificado":
            precios_zona[a["_zona"]].append(a["_precio"])

    stats_zona = {z: stats(v) for z, v in precios_zona.items()}
    zonas_5 = {z: s for z, s in stats_zona.items() if s["n"] >= 5}
    zonas_10 = {z: s for z, s in stats_zona.items() if s["n"] >= 10}
    zona_cara_5 = max(zonas_5, key=lambda z: zonas_5[z]["mean"])
    zona_cara_10 = max(zonas_10, key=lambda z: zonas_10[z]["mean"])
    zona_mediana_5 = max(zonas_5, key=lambda z: zonas_5[z]["median"])
    zona_mediana_10 = max(zonas_10, key=lambda z: zonas_10[z]["median"])

    top4 = zonas.most_common(4)
    top4_total = sum(c for _, c in top4)

    # Tipos
    tipos = Counter(a["_tipo"] for a in anuncios)
    precios_tipo = defaultdict(list)
    for a in usd:
        precios_tipo[a["_tipo"]].append(a["_precio"])
    stats_tipo = {t: stats(v) for t, v in precios_tipo.items()}
    tipos_comparables = [t for t in stats_tipo if stats_tipo[t]["n"] >= 10]

    # Opacidad
    sin_precio_n = len(sin_precio)
    ambos_n = sum(
        1 for a in anuncios
        if a["_precio"] is None and a["_zona"] == "No especificado"
    )
    completo_n = sum(
        1 for a in anuncios
        if a["_precio"] is not None and a["_zona"] != "No especificado"
    )
    sin_feature = [a for a in anuncios if not tiene_feature(a["_texto"])]
    totalmente_opacos = [
        a for a in anuncios
        if a["_precio"] is None
        and a["_zona"] == "No especificado"
        and not tiene_feature(a["_texto"])
    ]

    # Informalidad
    informal = [
        a for a in anuncios
        if any(p in a["_texto"] for p in PALABRAS_INFORMALES)
    ]
    neutros = [a for a in anuncios if a not in informal]
    informal_con_precio = sum(1 for a in informal if a["_precio"] is not None)
    neutros_con_precio = sum(1 for a in neutros if a["_precio"] is not None)
    informal_por_op = Counter(a["_op"] for a in informal)
    palabras_inf = Counter(
        p for a in anuncios for p in PALABRAS_INFORMALES if p in a["_texto"]
    )

    # Dolarización
    usd_declarada = len(usd)
    pct_usd_declarada = pct(usd_declarada, len(con_moneda))
    pct_usd_total = pct(usd_declarada, total)
    usd_min = pct(usd_declarada, total)
    usd_max = pct(usd_declarada + sin_precio_n, total)

    # Opacidad por operación y por tipo
    def sin_zona(grupo):
        return sum(1 for a in grupo if a["_zona"] == "No especificado")

    def sin_precio_grupo(grupo):
        return sum(1 for a in grupo if a["_precio"] is None)

    # Fecha de corte: la más frecuente entre las fechas no vacías.
    fechas = Counter(
        (a.get("fecha_verificacion") or "")[:10] for a in anuncios
        if a.get("fecha_verificacion")
    )
    fecha_corte = fechas.most_common(1)[0][0] if fechas else "no disponible"

    # Conteos de la verificación municipal
    conteo_rev = contar_resultados(cargar_json(INPUT_VERIF_REVOLICO))
    conteo_fb = contar_resultados(
        cargar_json(INPUT_VERIF_FACEBOOK), solo_base_limpia=True
    )
    conteo_uni = contar_resultados(verificacion)
    n_revolico = sum(1 for a in anuncios if a["_fuente"] == "revolico")
    n_facebook = sum(1 for a in anuncios if a["_fuente"] == "facebook")

    # Duplicado entre fuentes documentado en la base unificada
    duplicados = [
        a for a in anuncios if a.get("posibles_duplicados")
    ]

    # Cobertura por campo para el anexo. Se cuenta el dato tal como está en la
    # base: vacío o «No especificado» significa que el anuncio no lo declara.
    def tiene_dato(valor):
        return valor not in (None, "", "No especificado", "Sin especificar", [], {})

    n_habitaciones = sum(
        1 for a in anuncios
        if tiene_dato((a.get("detalles_propiedad") or {}).get("habitaciones"))
    )
    n_banos = sum(
        1 for a in anuncios
        if tiene_dato((a.get("detalles_propiedad") or {}).get("banos"))
    )
    n_area = sum(
        1 for a in anuncios
        if tiene_dato((a.get("detalles_propiedad") or {}).get("area_m2"))
    )
    n_telefono = sum(
        1 for a in anuncios
        if tiene_dato((a.get("contacto") or {}).get("telefono"))
    )
    n_enlace = sum(
        1 for a in anuncios
        if tiene_dato((a.get("publicacion") or {}).get("enlace"))
    )
    n_operacion_declarada = sum(
        1 for a in anuncios if a["_op"] != "Sin clasificar"
    )
    n_zona_cruda = sum(
        1 for a in anuncios
        if tiene_dato((a.get("detalles_propiedad") or {}).get("zona"))
    )

    descartados = cargar_json(INPUT_DESCARTADOS).get("registros", [])
    n_descartados = len(descartados)
    n_descartados_fuera = sum(
        1 for d in descartados if not d.get("en_universo_unificado")
    )

    L = []

    # ------------------------------------------------------------------
    # Portada y resumen
    # ------------------------------------------------------------------
    L.append("# Mercado inmobiliario digital en Diez de Octubre")
    L.append("## Opacidad, dolarización, desigualdad territorial e informalidad")
    L.append("")
    L.append(f"**Fecha de generación:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    L.append(f"**Corte de los datos:** {fecha_corte} (Revolico); Facebook sin fecha homogénea")
    L.append(
        f"**Universo:** {total} publicaciones confirmadas dentro del municipio "
        f"({n_revolico} de Revolico + {n_facebook} de Facebook)"
    )
    L.append("**Verificación espacial:** polígono municipal DPA `23.09` de `datos/geo/lha.geojson`")
    L.append("**Base de datos:** `datos/limpios/unificado_confirmados_diez_octubre.json`")
    L.append("")
    L.append("## Resumen ejecutivo")
    L.append("")
    L.append(
        f"Esta versión no usa los 134 anuncios que el scraper *etiquetaba* como "
        f"Diez de Octubre. Usa las **{total} publicaciones que la verificación "
        f"espacial confirmó dentro del municipio**: {n_revolico} de Revolico y "
        f"{n_facebook} de Facebook. De las 176 publicaciones unificadas, "
        f"{conteo_uni.get('NO', 0)} pertenecen a otro municipio y "
        f"{conteo_uni.get('INDETERMINADO', 0)} no son verificables; todas quedan "
        f"fuera. La clasificación aplica el **título como evidencia principal**: "
        f"si nombra Diez de Octubre o un reparto interno, confirma; si nombra un "
        f"lugar externo, descarta. La ficha y el resto del texto solo se usan "
        f"cuando el título no aporta señal. El detalle está en "
        f"`{REPORTE_VERIFICACION}`."
    )
    L.append(
        f"Los **{n_descartados} registros no incluidos** "
        f"({conteo_uni.get('NO', 0)} `NO`, "
        f"{conteo_uni.get('INDETERMINADO', 0)} `INDETERMINADO` y "
        f"{n_descartados_fuera} fuera del universo) se conservan íntegros en "
        f"`datos/limpios/descartados_diez_octubre.json` y `.csv`, con su motivo, "
        f"su registro original y el registro unificado exacto."
    )
    L.append("")
    L.append("Los hallazgos principales son:")
    L.append("")
    L.append(
        f"- **Dolarización:** {usd_declarada} de {len(con_moneda)} publicaciones "
        f"con moneda declarada están en USD (**{pct_usd_declarada:.1f}%**), y "
        f"{usd_declarada} de {total} del total (**{pct_usd_total:.1f}%**). El "
        f"único precio declarado en CUP es un alquiler."
    )
    L.append(
        f"- **Precios de compra:** mediana **${fmt(stats_venta['median'])} USD**; "
        f"P10–P90 **${fmt(stats_venta['p10'])}–${fmt(stats_venta['p90'])} USD**; "
        f"media **${fmt(stats_venta['mean'])} USD** "
        f"(n = {stats_venta['n']} ventas explícitas con precio en USD)."
    )
    L.append(
        f"- **Alquiler:** {len(alquileres_con_precio)} de {len(alquileres)} "
        f"alquileres declaran precio y **ninguno lo hace en USD**; el precio de "
        f"alquiler no es estimable con esta base."
    )
    L.append(
        f"- **Opacidad:** {sin_precio_n} de {total} publicaciones "
        f"({pct(sin_precio_n, total):.1f}%) no declaran precio; {sin_zona_n} "
        f"({pct(sin_zona_n, total):.1f}%) no especifican zona; solo {completo_n} "
        f"({pct(completo_n, total):.1f}%) permiten cruzar precio y zona."
    )
    L.append(
        f"- **Desigualdad territorial:** las cuatro zonas principales concentran "
        f"{top4_total} de {total_con_zona} publicaciones con zona identificada "
        f"({pct(top4_total, total_con_zona):.1f}%). Entre las zonas con n ≥ 10, "
        f"{zona_cara_10} tiene la media más alta "
        f"(${fmt(zonas_10[zona_cara_10]['mean'])} USD, "
        f"n = {zonas_10[zona_cara_10]['n']}) y {zona_mediana_10} la mediana más "
        f"alta (${fmt(zonas_10[zona_mediana_10]['median'])} USD, "
        f"n = {zonas_10[zona_mediana_10]['n']}); entre las de n ≥ 5, "
        f"{zona_cara_5} lidera la media "
        f"(${fmt(zonas_5[zona_cara_5]['mean'])} USD, "
        f"n = {zonas_5[zona_cara_5]['n']}), pero la mediana más alta sigue "
        f"siendo la de {zona_mediana_5} "
        f"(${fmt(zonas_5[zona_mediana_5]['median'])} USD, "
        f"n = {zonas_5[zona_mediana_5]['n']})."
    )
    L.append(
        f"- **Informalidad:** {len(informal)} de {total} publicaciones "
        f"({pct(len(informal), total):.1f}%) usan lenguaje de oportunidad, "
        f"permuta o cambio. Todas son de Revolico: Facebook no aporta texto "
        f"suficiente para medir esta dimensión, así que el dato es una cota "
        f"inferior."
    )
    L.append(
        f"- **Tipo de inmueble:** el apartamento es la opción más accesible: "
        f"media **${fmt(stats_tipo['Apartamento']['mean'])} USD** y mediana "
        f"**${fmt(stats_tipo['Apartamento']['median'])} USD** "
        f"(n = {stats_tipo['Apartamento']['n']}), frente a la casa con media "
        f"**${fmt(stats_tipo['Casa']['mean'])} USD** y mediana "
        f"**${fmt(stats_tipo['Casa']['median'])} USD** "
        f"(n = {stats_tipo['Casa']['n']})."
    )
    L.append("")
    L.append(
        "La ausencia de datos no se trata como un simple defecto: se mide y se "
        "reporta como un rasgo del mercado. Una publicación sin precio, sin zona "
        "o sin operación limita la capacidad de comparar y de verificar, y esa "
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
        "incompletas y publicaciones que no declaran si se vende o se alquila, la "
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
        "prácticas (lenguaje de oportunidad, permuta, publicaciones sin operación) "
        "aparecen en los anuncios?"
    )
    L.append("")
    L.append(
        "Diez de Octubre es un caso relevante porque combina alta densidad de "
        "vivienda, barrios con identidad propia (Santos Suárez, Lawton, La "
        "Víbora, Luyano, El Sevillano) y una presencia importante de anuncios "
        "digitales. La comparación entre barrios permite observar si el mercado "
        "reproduce o atenúa las desigualdades territoriales."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Metodología
    # ------------------------------------------------------------------
    L.append("## Metodología y verificación municipal")
    L.append("")
    L.append(f"### Por qué el universo es {total} y no 134")
    L.append("")
    L.append(
        "El campo `municipio` del scraper no es fiable: asigna «Diez de Octubre» "
        "a anuncios que en su ficha declaran otro municipio. Para corregirlo se "
        "usó el **título como evidencia principal**. Si el título nombra Diez de "
        "Octubre o un reparto interno, la publicación se confirma; si nombra un "
        "municipio, reparto o localidad externa, se descarta. Solo cuando el "
        "título no aporta señal se recurre a la ficha de Revolico y al resto del "
        "texto (enlace, grupo, ubicación o zona). Los topónimos se geocodificaron "
        "con Nominatim y se comprobaron punto-en-polígono contra "
        "`datos/geo/lha.geojson`."
    )
    L.append("")
    L.append("| Resultado | Revolico (n=134) | Facebook (n=42) | Unificado (n=176) |")
    L.append("|---|---:|---:|---:|")
    L.append(
        f"| SÍ, dentro de Diez de Octubre | {conteo_rev.get('SÍ', 0)} | "
        f"{conteo_fb.get('SÍ', 0)} | {conteo_uni.get('SÍ', 0)} |"
    )
    L.append(
        f"| NO, otro municipio | {conteo_rev.get('NO', 0)} | "
        f"{conteo_fb.get('NO', 0)} | {conteo_uni.get('NO', 0)} |"
    )
    L.append(
        f"| CONTRADICTORIO | {conteo_rev.get('CONTRADICTORIO', 0)} | "
        f"{conteo_fb.get('CONTRADICTORIO', 0)} | {conteo_uni.get('CONTRADICTORIO', 0)} |"
    )
    L.append(
        f"| INDETERMINADO | {conteo_rev.get('INDETERMINADO', 0)} | "
        f"{conteo_fb.get('INDETERMINADO', 0)} | {conteo_uni.get('INDETERMINADO', 0)} |"
    )
    L.append("")
    L.append(
        f"La base final son las **{conteo_uni.get('SÍ', 0)} publicaciones con "
        f"resultado SÍ**. Las {conteo_uni.get('NO', 0)} de otro municipio y las "
        f"{conteo_uni.get('INDETERMINADO', 0)} indeterminadas se excluyen. Los 8 "
        f"casos que la regla anterior marcaba como contradictorios tenían un "
        f"título con un reparto interno y se confirman por la regla de título. "
        f"Esa exclusión reduce el tamaño de la muestra, pero evita atribuir a "
        f"Diez de Octubre precios y zonas que pertenecen a otros municipios."
    )
    L.append(
        f"Los **{n_descartados} registros no incluidos** se conservan íntegros: "
        f"{conteo_uni.get('NO', 0)} `NO`, "
        f"{conteo_uni.get('INDETERMINADO', 0)} `INDETERMINADO` y "
        f"{n_descartados_fuera} que ya estaba fuera de la base unificada "
        f"(`facebook-27`). Cada uno guarda su motivo, la evidencia, el registro "
        f"original y el registro unificado exacto en "
        f"`datos/limpios/descartados_diez_octubre.json` y `.csv`."
    )
    L.append("")
    L.append(
        "La verificación tiene un límite explícito: el polígono es una "
        "simplificación de 11 vértices y no resuelve casos catastrales a pocos "
        "metros del borde. Además, la ficha se apoya en la ubicación que declara "
        "el anunciante, no en la dirección exacta de la propiedad. La regla de "
        "título puede confirmar un anuncio con ficha mal declarada, y los casos "
        "indeterminados son aquellos en los que ninguna evidencia alcanza para "
        "decidir."
    )
    L.append("")
    L.append("### Fuentes y normalización")
    L.append("")
    L.append(
        f"- **Revolico:** {n_revolico} publicaciones confirmadas. Aportan título, "
        f"enlace, fecha de verificación y, en la mayoría de los casos, precio "
        f"anidado en `precio.monto`."
    )
    L.append(
        f"- **Facebook:** {n_facebook} publicaciones confirmadas. Aportan precio "
        f"y descripción, pero muchas no tienen título ni texto crudo "
        f"homogéneo. Por eso la operación queda «sin clasificar» con más "
        f"frecuencia y la medición de lenguaje informal solo es posible en "
        f"Revolico."
    )
    L.append(
        "- **Precio:** se usa `precio.monto` y, cuando falta, `precio.monto_actual` "
        "(un caso de Facebook con rebaja: 15,000 USD). Los precios en CUP no se "
        "convierten a USD porque no hay un tipo de cambio único y defendible para "
        "el corte."
    )
    L.append(
        "- **Zona:** se usa el campo normalizado `detalles_propiedad.zona`. Si "
        "viene vacío o «No especificado», se busca el nombre del barrio o reparto "
        "en el texto declarado. No se infiere una zona que el anuncio no mencione."
    )
    L.append(
        "- **Tipo y operación:** se usan los campos normalizados "
        "`detalles_propiedad.tipo` y `operacion`. No se reclasifica la operación "
        "por el precio ni por el título: si el anuncio no la declara, queda "
        "«sin clasificar». Es una regla conservadora y reproducible."
    )
    L.append(
        "- **Subgrupos pequeños:** los grupos con n < 10 se presentan como "
        "evidencia descriptiva, no como conclusión firme. Las zonas con n < 5 no "
        "se usan para comparar promedios."
    )
    L.append(
        "- **Ausencia:** una publicación sin precio, sin zona o sin operación no "
        "se elimina del universo. Se conserva y se contabiliza como indicador de "
        "opacidad, porque su ausencia también describe el mercado."
    )
    L.append("")
    L.append("### Trazabilidad del cambio respecto al informe anterior")
    L.append("")
    L.append(
        "El informe anterior respondía 30 preguntas sobre 134 anuncios de "
        "Revolico etiquetados como Diez de Octubre. La verificación muestra que "
        "83 de esos 134 están confirmados en el municipio: 73 con ficha que "
        "declara Diez de Octubre y 10 por mención interna en el título. Esta "
        "versión recalcula el informe con las 122 publicaciones confirmadas e "
        "incorpora 39 de Facebook. No es una actualización de cifras: es un "
        "cambio de universo. Las cifras anteriores no deben compararse "
        "directamente con las de este informe."
    )
    L.append("")
    L.append(
        "Las 30 preguntas A1–F5 se conservan. Cinco preguntas originales del "
        "cuestionario base siguen sin ser estimables con estos datos (mediana del "
        "alquiler, comparación compra–alquiler, precio por metro cuadrado, zonas "
        "por operación y precio promedio en CUP); en su lugar se mantienen "
        "preguntas que miden la ausencia de información."
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
        f"ventas explícitas con precio en USD. Si se incluyen todas las "
        f"publicaciones con precio USD (ventas y publicaciones sin operación "
        f"declarada; no hay alquileres en USD), la media sube a "
        f"**${fmt(stats_usd['mean'])} USD** (n = {stats_usd['n']}), porque las "
        f"publicaciones sin operación declarada incluyen inmuebles de mayor "
        f"precio. La media de compra es una referencia, no el precio típico: la "
        f"mediana es bastante menor (A2)."
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
        f"derecha: unas pocas publicaciones muy caras elevan el promedio."
    )
    L.append("")
    L.append(
        f"**A3. ¿Cuál es el precio promedio o mediano del alquiler?** 🔴 "
        f"(no estimable)"
    )
    L.append("")
    L.append(
        f"> **No estimable.** Hay {len(alquileres)} publicaciones de alquiler: "
        f"{len(alquileres_con_precio)} declara precio (uno solo, en CUP: "
        f"50,000 CUP) y "
        f"{len(alquileres) - len(alquileres_con_precio)} no lo declaran "
        f"({pct(len(alquileres) - len(alquileres_con_precio), len(alquileres)):.1f}%). "
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
        f"conocer ni siquiera el orden de magnitud del precio. Con solo 3 casos, "
        f"la proporción es un censo del subgrupo, no una estimación del mercado."
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
        f"alquiler, que funciona casi por contacto directo. La conclusión es "
        f"descriptiva: el alquiler tiene solo {len(alquileres)} casos."
    )
    L.append("")

    # ---------------- BLOQUE B ----------------
    L.append("### Bloque B: Desigualdades territoriales")
    L.append("")
    L.append(
        f"**B1. ¿Qué zonas concentran la mayor oferta?** ✅ "
        f"({total_con_zona} publicaciones con zona identificada)"
    )
    L.append("")
    for z, c in zonas.most_common():
        L.append(
            f"> - {z}: **{c} {unidad(c)}** "
            f"({pct(c, total_con_zona):.1f}% de las publicaciones con zona)"
        )
    L.append(">")
    L.append(
        f"> **{total_con_zona} de {total} publicaciones "
        f"({pct(total_con_zona, total):.1f}%)** especifican zona; "
        f"**{sin_zona_n} ({pct(sin_zona_n, total):.1f}%)** no lo hacen. Las "
        f"cuatro zonas principales —{', '.join(z for z, _ in top4)}— reúnen "
        f"**{top4_total} de {total_con_zona} "
        f"({pct(top4_total, total_con_zona):.1f}%)** de la oferta con zona "
        f"identificada: la información territorial está concentrada en pocos "
        f"barrios."
    )
    L.append("")
    L.append(
        f"**B2. ¿Qué zona tiene el precio promedio más alto?** 🟡 "
        f"(n = {zonas_5[zona_cara_5]['n']} en {zona_cara_5})"
    )
    L.append("")
    L.append(
        f"> **{zona_cara_5}**, con una media de "
        f"**${fmt(zonas_5[zona_cara_5]['mean'])} USD** "
        f"(n = {zonas_5[zona_cara_5]['n']}). Es un resultado descriptivo: el "
        f"grupo tiene menos de 10 publicaciones y su media puede estar influida "
        f"por valores extremos. Si se exige n ≥ 10, la zona con media más alta "
        f"es **{zona_cara_10}** (${fmt(zonas_10[zona_cara_10]['mean'])} USD, "
        f"n = {zonas_10[zona_cara_10]['n']})."
    )
    L.append("")
    L.append("> Orden por media entre las zonas con n ≥ 5:")
    L.append(">")
    for z in sorted(zonas_5, key=lambda x: zonas_5[x]["mean"], reverse=True):
        s = zonas_5[z]
        L.append(
            f"> - {z}: media **${fmt(s['mean'])} USD**, mediana "
            f"**${fmt(s['median'])} USD** (n = {s['n']})"
        )
    L.append("")
    L.append(
        f"**B3. ¿Qué zona tiene la mediana más alta?** 🟡 "
        f"(n = {zonas_5[zona_mediana_5]['n']} en {zona_mediana_5})"
    )
    L.append("")
    L.append(
        f"> **{zona_mediana_5}**, con una mediana de "
        f"**${fmt(zonas_5[zona_mediana_5]['median'])} USD** "
        f"(n = {zonas_5[zona_mediana_5]['n']}). Si se exige n ≥ 10, la mediana "
        f"más alta corresponde a **{zona_mediana_10}** "
        f"(${fmt(zonas_10[zona_mediana_10]['median'])} USD, "
        f"n = {zonas_10[zona_mediana_10]['n']})."
    )
    L.append("")
    L.append("> Orden por mediana entre las zonas con n ≥ 5:")
    L.append(">")
    for z in sorted(zonas_5, key=lambda x: zonas_5[x]["median"], reverse=True):
        s = zonas_5[z]
        L.append(
            f"> - {z}: mediana **${fmt(s['median'])} USD** (n = {s['n']})"
        )
    L.append("")

    zona_a = "La Víbora"
    zona_b = "Lawton"
    if zona_a in stats_zona and zona_b in stats_zona:
        sa = stats_zona[zona_a]
        sb = stats_zona[zona_b]
        brecha_media = sa["mean"] - sb["mean"]
        brecha_mediana = sa["median"] - sb["median"]
        if brecha_mediana:
            veces = brecha_media / brecha_mediana
            comparacion = (
                f"La brecha por media es **{veces:.1f} veces** la brecha por "
                f"mediana."
            )
        else:
            comparacion = (
                "La brecha por mediana es cero o casi cero, mientras que la "
                "brecha por media es amplia."
            )
        L.append(
            f"**B4. ¿La brecha {zona_a}–{zona_b} se mantiene al usar medianas?** "
            f"🟡 (n = {sa['n']} y {sb['n']})"
        )
        L.append("")
        L.append(
            f"> **No se mantiene con la misma magnitud.** Por media, {zona_a} "
            f"(${fmt(sa['mean'])} USD) supera a {zona_b} "
            f"(${fmt(sb['mean'])} USD) en **${fmt(brecha_media)} USD**. Por "
            f"mediana, la diferencia es de solo **${fmt(brecha_mediana)} USD** "
            f"(${fmt(sa['median'])} frente a ${fmt(sb['median'])}). "
            f"{comparacion} El máximo de {zona_a} "
            f"(${fmt(sa['max'])} USD) y su P90 (${fmt(sa['p90'])} USD) explican "
            f"buena parte de la diferencia: la media describe el extremo alto, "
            f"no el precio típico. Para comparar barrios conviene usar la "
            f"mediana."
        )
        L.append("")

    L.append(
        f"**B5. ¿La falta de zona afecta igual a compra y alquiler?** ✅ "
        f"(censo de operaciones)"
    )
    L.append("")
    L.append(
        f"> No. La falta de zona es más frecuente en alquiler: "
        f"**{sin_zona(alquileres)} de {len(alquileres)} "
        f"({pct(sin_zona(alquileres), len(alquileres)):.1f}%)** alquileres no "
        f"especifican zona, frente a **{sin_zona(ventas)} de {len(ventas)} "
        f"({pct(sin_zona(ventas), len(ventas)):.1f}%)** ventas y "
        f"**{sin_zona(sin_clasificar)} de {len(sin_clasificar)} "
        f"({pct(sin_zona(sin_clasificar), len(sin_clasificar)):.1f}%)** "
        f"publicaciones sin operación declarada. El alquiler combina las dos "
        f"opacidades: casi nunca declara precio y casi nunca declara zona. Con "
        f"solo {len(alquileres)} alquileres, la evidencia es descriptiva."
    )
    L.append("")

    # ---------------- BLOQUE C ----------------
    L.append("### Bloque C: Dolarización")
    L.append("")
    L.append(
        f"**C1. ¿Qué porcentaje de publicaciones con moneda declarada está en USD?** "
        f"✅ (n = {len(con_moneda)})"
    )
    L.append("")
    L.append(
        f"> **{usd_declarada} de {len(con_moneda)} "
        f"({pct_usd_declarada:.1f}%)**. El único anuncio con moneda declarada "
        f"que no está en USD es un alquiler en CUP (50,000 CUP). Las "
        f"{sin_precio_n} publicaciones sin precio no declaran moneda y quedan "
        f"fuera de este denominador."
    )
    L.append("")
    L.append(
        f"**C2. ¿Qué porcentaje del total está en USD?** ✅ (n = {total})"
    )
    L.append("")
    L.append(
        f"> **{usd_declarada} de {total} ({pct_usd_total:.1f}%)**. El resto se "
        f"reparte entre {sin_precio_n} publicaciones sin precio "
        f"({pct(sin_precio_n, total):.1f}%) y 1 anuncio en CUP "
        f"({pct(1, total):.1f}%). La dolarización es alta incluso cuando se "
        f"cuenta a las publicaciones que no declaran precio."
    )
    L.append("")
    L.append(
        f"**C3. ¿La dolarización varía por tipo de inmueble?** ✅ "
        f"(publicaciones con precio)"
    )
    L.append("")
    for t in ["Casa", "Apartamento", "Inmueble", "Cuarto"]:
        grupo = [a for a in anuncios if a["_tipo"] == t and a["_precio"] is not None]
        usd_grupo = [a for a in grupo if a["_moneda"] == "USD"]
        if grupo:
            L.append(
                f"> - {t}: **{len(usd_grupo)} de {len(grupo)} "
                f"({pct(len(usd_grupo), len(grupo)):.1f}%)** en USD"
            )
    L.append(">")
    L.append(
        "> La dolarización es prácticamente total en todos los tipos con precio. "
        "El único anuncio en CUP es un alquiler clasificado como «Inmueble». No "
        "hay un tipo de inmueble que funcione principalmente en CUP."
    )
    L.append("")
    usd_con_zona = [a for a in usd if a["_zona"] != "No especificado"]
    L.append(
        f"**C4. ¿La dolarización varía por zona?** ✅ "
        f"({len(usd_con_zona)} publicaciones USD con zona)"
    )
    L.append("")
    L.append(
        f"> **No se puede medir variación territorial:** las "
        f"**{len(usd_con_zona)} publicaciones** con precio USD y zona "
        f"identificada están **todas en USD (100%)**. El único anuncio en CUP no "
        f"especifica zona. La conclusión no es que todas las zonas estén "
        f"dolarizadas por igual, sino que la base no permite compararlas: la "
        f"ausencia de zona en el anuncio en CUP impide saber si hay barrios con "
        f"precios en CUP."
    )
    L.append("")
    L.append(
        f"**C5. ¿Cuánto podría variar la dolarización si las publicaciones sin "
        f"precio fueran CUP o USD?** ✅ (cota inferior y superior)"
    )
    L.append("")
    L.append(
        f"> La proporción de USD en el total está acotada entre "
        f"**{usd_min:.1f}%** y **{usd_max:.1f}%**. El límite inferior supone que "
        f"las {sin_precio_n} publicaciones sin precio están en CUP; el superior, "
        f"que están en USD. La diferencia entre ambos escenarios es de "
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
        f"Son publicaciones que no permiten comparar precios sin contactar al "
        f"vendedor. La ausencia es especialmente alta en alquiler (A4)."
    )
    L.append("")
    L.append(
        f"**D2. ¿Qué porcentaje no especifica zona?** ✅ (n = {total})"
    )
    L.append("")
    L.append(
        f"> **{sin_zona_n} de {total} ({pct(sin_zona_n, total):.1f}%)**. "
        f"Sin zona no se puede verificar la ubicación ni comparar barrios. La "
        f"cifra es menor que la del informe anterior porque esta base trae un "
        f"campo de zona normalizado y se completó con el texto declarado; no "
        f"porque el mercado se haya vuelto más transparente."
    )
    L.append("")
    L.append(
        f"**D3. ¿Cuántas publicaciones carecen de precio y zona a la vez?** ✅ "
        f"(n = {total})"
    )
    L.append("")
    L.append(
        f"> **{ambos_n} de {total} ({pct(ambos_n, total):.1f}%)**. En estas "
        f"publicaciones no se puede saber ni cuánto cuesta ni dónde está. Son el "
        f"núcleo más opaco del mercado digital."
    )
    L.append("")
    L.append(
        f"**D4. ¿Qué porcentaje tiene información mínima completa "
        f"(precio + zona)?** ✅ (n = {total})"
    )
    L.append("")
    L.append(
        f"> **{completo_n} de {total} ({pct(completo_n, total):.1f}%)**. Dos "
        f"tercios de las publicaciones permiten cruzar precio y zona. Ese es el "
        f"subconjunto sobre el que se pueden hacer comparaciones territoriales "
        f"relativamente sólidas; el resto queda fuera por falta de un dato "
        f"básico."
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
        f"no declaran precio y **{sin_zona(alquileres)} de {len(alquileres)} "
        f"({pct(sin_zona(alquileres), len(alquileres)):.1f}%)** no declaran zona. "
        f"En **venta**, **{len(ventas) - len(ventas_con_precio)} de {len(ventas)} "
        f"({pct(len(ventas) - len(ventas_con_precio), len(ventas)):.1f}%)** no "
        f"declaran precio y **{sin_zona(ventas)} de {len(ventas)} "
        f"({pct(sin_zona(ventas), len(ventas)):.1f}%)** no declaran zona. El "
        f"alquiler es el segmento más opaco en ambas dimensiones, aunque el "
        f"grupo es muy pequeño."
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
        f"El lenguaje informal no es mayoritario, pero aparece en una de cada "
        f"doce publicaciones. Las {len(informal)} son de Revolico: Facebook no "
        f"aporta texto suficiente para medir esta dimensión, así que el dato es "
        f"una **cota inferior** del mercado unificado."
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
        "en pocas publicaciones. Las palabras «ganga» e «intercambio» no "
        "aparecen en la base. La informalidad se expresa más como reclamo "
        "comercial que como trueque explícito."
    )
    L.append("")
    L.append(
        f"**E3. ¿Las publicaciones informales declaran precio más que las "
        f"neutras?** 🟡 (n = {len(informal)} informales)"
    )
    L.append("")
    L.append(
        f"> **{informal_con_precio} de {len(informal)} "
        f"({pct(informal_con_precio, len(informal)):.1f}%)** de las informales "
        f"declaran precio, frente a **{neutros_con_precio} de {len(neutros)} "
        f"({pct(neutros_con_precio, len(neutros)):.1f}%)** de las neutras. La "
        f"diferencia es de "
        f"**{pct(informal_con_precio, len(informal)) - pct(neutros_con_precio, len(neutros)):.1f} puntos porcentuales**. "
        f"El subgrupo informal es pequeño (n = {len(informal)}), así que la "
        f"diferencia es indicativa: no permite concluir que el lenguaje informal "
        f"implique mayor transparencia."
    )
    L.append("")
    L.append(
        f"**E4. ¿La informalidad se concentra en alguna operación?** ✅ "
        f"(censo de {len(informal)} publicaciones informales)"
    )
    L.append("")
    for op in ["Venta", "Alquiler", "Sin clasificar"]:
        c = informal_por_op.get(op, 0)
        L.append(
            f"> - {op}: **{c} de {len(informal)} "
            f"({pct(c, len(informal)):.1f}%)**"
        )
    L.append(">")
    L.append(
        "> La informalidad aparece en **venta** y en **publicaciones sin "
        "operación declarada**; **no aparece en alquiler**. Esto refuerza la "
        "lectura de que el alquiler se gestiona por otros canales (contacto "
        "directo, redes cerradas) y no necesita el reclamo de «oportunidad» en "
        "el título."
    )
    L.append("")
    L.append(
        f"**E5. ¿Las publicaciones sin clasificar son más opacas que las "
        f"clasificadas?** ✅ (censo de operaciones)"
    )
    L.append("")
    L.append(
        f"> **No.** Las publicaciones sin operación declarada son, en esta base, "
        f"más completas que las ventas explícitas: "
        f"**{len(sin_clasificar) - sin_precio_grupo(sin_clasificar)} de "
        f"{len(sin_clasificar)} "
        f"({pct(len(sin_clasificar) - sin_precio_grupo(sin_clasificar), len(sin_clasificar)):.1f}%)** "
        f"declaran precio y **{len(sin_clasificar) - sin_zona(sin_clasificar)} "
        f"de {len(sin_clasificar)} "
        f"({pct(len(sin_clasificar) - sin_zona(sin_clasificar), len(sin_clasificar)):.1f}%)** "
        f"declaran zona. En venta, esas proporciones son "
        f"**{pct(len(ventas_con_precio), len(ventas)):.1f}%** y "
        f"**{pct(len(ventas) - sin_zona(ventas), len(ventas)):.1f}%**; en "
        f"alquiler, **{pct(len(alquileres_con_precio), len(alquileres)):.1f}%** "
        f"y **{pct(len(alquileres) - sin_zona(alquileres), len(alquileres)):.1f}%**. "
        f"El grupo realmente opaco es el alquiler, no el de las publicaciones "
        f"sin clasificar. La falta de etiqueta de operación no equivale a falta "
        f"de información."
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
    diferencia_media = stats_tipo["Casa"]["mean"] - stats_tipo["Apartamento"]["mean"]
    L.append(
        f"> El **apartamento** es la opción más accesible entre los tipos con "
        f"n ≥ 10: su media es **${fmt(stats_tipo['Apartamento']['mean'])} USD**, "
        f"frente a **${fmt(stats_tipo['Casa']['mean'])} USD** de la casa y "
        f"**${fmt(stats_tipo['Inmueble']['mean'])} USD** del inmueble sin tipo "
        f"específico. La diferencia entre apartamento y casa es de "
        f"**${fmt(diferencia_media)} USD**: el apartamento cuesta aproximadamente "
        f"**{100 * diferencia_media / stats_tipo['Casa']['mean']:.1f}% menos** "
        f"que la casa en promedio. El cuarto tiene n = {stats_tipo.get('Cuarto', {}).get('n', 0)} "
        f"y no se usa para comparar."
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
    diferencia_mediana = stats_tipo["Casa"]["median"] - stats_tipo["Apartamento"]["median"]
    L.append(
        f"> El **apartamento** también tiene la mediana más baja: "
        f"**${fmt(stats_tipo['Apartamento']['median'])} USD**, frente a "
        f"**${fmt(stats_tipo['Casa']['median'])} USD** de la casa y "
        f"**${fmt(stats_tipo['Inmueble']['median'])} USD** del inmueble. La "
        f"mediana del apartamento es un "
        f"**{100 * diferencia_mediana / stats_tipo['Casa']['median']:.1f}% menor** "
        f"que la de la casa. La conclusión se mantiene al pasar de la media a la "
        f"mediana, lo que la hace más robusta frente a valores extremos."
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
            f"**${fmt(s['median'])} USD**, P90 **${fmt(s['p90'])} USD** "
            f"(n = {s['n']})"
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
        f"más estrecho y desplazado hacia abajo. Las distribuciones se solapan, "
        f"pero el apartamento es consistentemente más accesible."
    )
    L.append("")
    L.append(
        f"**F5. ¿Qué tipo concentra más opacidad de precio y zona?** ✅ "
        f"(censo por tipo)"
    )
    L.append("")
    for t in ["Inmueble", "Casa", "Apartamento", "Cuarto"]:
        grupo = [a for a in anuncios if a["_tipo"] == t]
        if not grupo:
            continue
        sp = sin_precio_grupo(grupo)
        sz = sin_zona(grupo)
        L.append(
            f"> - {t}: **{sp} de {len(grupo)} ({pct(sp, len(grupo)):.1f}%)** sin "
            f"precio; **{sz} de {len(grupo)} ({pct(sz, len(grupo)):.1f}%)** sin zona"
        )
    L.append(">")
    L.append(
        "> El **Inmueble** (títulos que no especifican un tipo concreto) "
        "concentra la mayor opacidad entre los tipos con n ≥ 10: es el que tiene "
        "la mayor proporción sin precio y sin zona. La casa tiene más casos "
        "absolutos sin zona, pero en proporción el Inmueble la supera. El cuarto "
        "muestra una proporción alta, pero solo son 2 publicaciones: es "
        "evidencia descriptiva, no una conclusión. La opacidad de zona afecta a "
        "todos los tipos; la de precio se concentra en el Inmueble y el "
        "Apartamento."
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
        f"| Publicaciones sin precio | **{sin_precio_n}/{total} "
        f"({pct(sin_precio_n, total):.1f}%)** | "
        f"No se puede comparar sin contactar al vendedor. |"
    )
    L.append(
        f"| Publicaciones sin zona | **{sin_zona_n}/{total} "
        f"({pct(sin_zona_n, total):.1f}%)** | "
        f"No se puede verificar la ubicación ni comparar barrios. |"
    )
    L.append(
        f"| Sin precio y sin zona | **{ambos_n}/{total} "
        f"({pct(ambos_n, total):.1f}%)** | "
        f"Publicaciones completamente opacas en precio y ubicación. |"
    )
    L.append(
        f"| Información completa (precio + zona) | **{completo_n}/{total} "
        f"({pct(completo_n, total):.1f}%)** | "
        f"Dos tercios permiten un análisis mínimo. |"
    )
    L.append(
        f"| Alquileres sin precio | "
        f"**{len(alquileres) - len(alquileres_con_precio)}/{len(alquileres)} "
        f"({pct(len(alquileres) - len(alquileres_con_precio), len(alquileres)):.1f}%)** | "
        f"El mercado de alquiler es casi invisible en precios. |"
    )
    L.append(
        f"| Alquileres sin zona | **{sin_zona(alquileres)}/{len(alquileres)} "
        f"({pct(sin_zona(alquileres), len(alquileres)):.1f}%)** | "
        f"Tampoco se puede ubicar la oferta de alquiler. |"
    )
    L.append(
        f"| Publicaciones sin operación declarada | "
        f"**{len(sin_clasificar)}/{total} "
        f"({pct(len(sin_clasificar), total):.1f}%)** | "
        f"Más de la mitad no dice si se vende o se alquila. |"
    )
    L.append(
        f"| Sin característica física explícita | **{len(sin_feature)}/{total} "
        f"({pct(len(sin_feature), total):.1f}%)** | "
        f"La descripción del inmueble es mínima. |"
    )
    L.append(
        f"| Totalmente opacas (sin precio, zona ni característica) | "
        f"**{len(totalmente_opacos)}/{total} "
        f"({pct(len(totalmente_opacos), total):.1f}%)** | "
        f"No hay ningún dato útil para comparar. |"
    )
    L.append(
        f"| Sin moneda declarada | **{sin_precio_n}/{total} "
        f"({pct(sin_precio_n, total):.1f}%)** | "
        f"No se sabe si el precio, cuando exista, será en USD o CUP. |"
    )
    if duplicados:
        L.append(
            f"| Duplicado entre fuentes | **{len(duplicados) // 2} par** | "
            f"Misma propiedad publicada en Revolico y Facebook. |"
        )
    L.append("")
    L.append(
        "La lectura social es directa: la opacidad no afecta a todos por igual. "
        "Quien puede llamar, visitar y verificar accede a la información que "
        "falta; quien depende del anuncio para comparar queda en desventaja. El "
        "alquiler, además, es el segmento con mayor ausencia de precio y zona, lo "
        "que sugiere que una parte importante de ese mercado opera por canales "
        "informales o de confianza previa."
    )
    L.append("")
    if duplicados:
        ids_dup = ", ".join(f"`{a['id_unico']}`" for a in duplicados)
        L.append(
            f"> **Nota de duplicidad:** la base contiene un par de publicaciones "
            f"que describen la misma propiedad y el mismo precio en Revolico y "
            f"Facebook ({ids_dup}). Se conserva para no alterar el universo "
            f"acordado de {total}, pero el n efectivo sería {total - 1} si se "
            f"eliminara. El par no cambia las conclusiones: ambos registros son "
            f"ventas en USD y no modifican las medianas de forma apreciable."
        )
        L.append("")

    # ------------------------------------------------------------------
    # Conclusiones
    # ------------------------------------------------------------------
    L.append("## Conclusiones")
    L.append("")
    L.append(
        f"1. **La base verificada es de {total} publicaciones.** La versión "
        f"anterior usaba 134 anuncios etiquetados como Diez de Octubre; la "
        f"verificación confirmó {n_revolico} de Revolico. Con {n_facebook} de "
        f"Facebook, esta versión usa las {total} publicaciones confirmadas "
        f"({n_revolico} de Revolico + {n_facebook} de Facebook) y excluye "
        f"{conteo_uni.get('NO', 0)} de otros municipios y "
        f"{conteo_uni.get('INDETERMINADO', 0)} indeterminadas."
    )
    L.append(
        f"2. **El mercado está dolarizado.** {usd_declarada} de "
        f"{len(con_moneda)} publicaciones con moneda declarada "
        f"({pct_usd_declarada:.1f}%) están en USD; en el total, la proporción es "
        f"{pct_usd_total:.1f}% y la cota superior posible es {usd_max:.1f}%. "
        f"Quien no tiene divisas enfrenta una barrera de acceso estructural."
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
        f"{pct(top4_total, total_con_zona):.1f}% de las publicaciones con zona. "
        f"Entre las zonas con n ≥ 10, {zona_cara_10} tiene la media más alta "
        f"(${fmt(zonas_10[zona_cara_10]['mean'])} USD, "
        f"n = {zonas_10[zona_cara_10]['n']}) y {zona_mediana_10} la mediana más "
        f"alta (${fmt(zonas_10[zona_mediana_10]['median'])} USD, "
        f"n = {zonas_10[zona_mediana_10]['n']}); entre las de n ≥ 5, "
        f"{zona_cara_5} lidera la media "
        f"(${fmt(zonas_5[zona_cara_5]['mean'])} USD, "
        f"n = {zonas_5[zona_cara_5]['n']}), pero la mediana más alta sigue "
        f"siendo la de {zona_mediana_5} "
        f"(${fmt(zonas_5[zona_mediana_5]['median'])} USD, "
        f"n = {zonas_5[zona_mediana_5]['n']}). La diferencia entre media y "
        f"mediana en {zona_a} muestra que los valores extremos inflan el "
        f"promedio."
    )
    L.append(
        f"6. **La opacidad es importante en zona y moderada en precio.** "
        f"{pct(sin_zona_n, total):.1f}% no especifica zona, "
        f"{pct(sin_precio_n, total):.1f}% no declara precio y "
        f"{pct(completo_n, total):.1f}% permite cruzar ambos datos. El "
        f"{pct(ambos_n, total):.1f}% no tiene ninguno de los dos. La ausencia de "
        f"información es un mecanismo de desigualdad: quien no puede verificar "
        f"queda expuesto a la intermediación."
    )
    L.append(
        f"7. **La informalidad es visible pero no domina.** "
        f"{pct(len(informal), total):.1f}% usa lenguaje de oportunidad, permuta "
        f"o cambio. Se concentra en venta y en publicaciones sin operación "
        f"declarada; no aparece en alquiler. Las informales declaran precio algo "
        f"más que las neutras "
        f"({pct(informal_con_precio, len(informal)):.1f}% frente a "
        f"{pct(neutros_con_precio, len(neutros)):.1f}%), pero el subgrupo es "
        f"pequeño y la diferencia no es concluyente. Además, el indicador solo "
        f"cubre Revolico: es una cota inferior."
    )
    L.append(
        f"8. **El apartamento es la opción más accesible.** Su media es "
        f"${fmt(stats_tipo['Apartamento']['mean'])} USD y su mediana "
        f"${fmt(stats_tipo['Apartamento']['median'])} USD "
        f"(n = {stats_tipo['Apartamento']['n']}), frente a la casa "
        f"(${fmt(stats_tipo['Casa']['mean'])} y "
        f"${fmt(stats_tipo['Casa']['median'])} USD; "
        f"n = {stats_tipo['Casa']['n']}). La diferencia se mantiene en P10–P90. "
        f"Entre los tipos con n ≥ 10, el Inmueble sin tipo específico es el más "
        f"opaco y el más caro en media, lo que sugiere que la falta de "
        f"información sobre el tipo se asocia con operaciones de mayor valor."
    )
    L.append("")
    L.append(
        "En conjunto, el mercado digital de Diez de Octubre no es un espacio "
        "transparente de precios y ubicaciones: es un mercado segmentado por "
        "divisas, por acceso a información y por barrios. La base verificada "
        "permite afirmar esto con mayor rigor que la versión anterior, y también "
        "permite identificar qué no se puede saber: el precio del alquiler, la "
        "zona de una cuarta parte de las publicaciones y la operación de más de "
        "la mitad. Ese límite es parte del resultado."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Limitaciones
    # ------------------------------------------------------------------
    L.append("## Limitaciones")
    L.append("")
    L.append(
        f"- **Muestra no probabilística:** {total} publicaciones es una base "
        f"pequeña y no necesariamente representativa del universo de viviendas "
        f"del municipio. No hay serie temporal: el corte de Revolico es único "
        f"({fecha_corte}) y Facebook no tiene fechas homogéneas."
    )
    L.append(
        "- **Integración de fuentes heterogéneas:** Revolico y Facebook no "
        "comparten esquema. Facebook aporta descripciones y precios, pero muchas "
        "publicaciones no tienen título ni texto crudo, lo que eleva el «sin "
        "clasificar» y reduce la medición de informalidad a Revolico. Las "
        "comparaciones entre fuentes deben leerse como descriptivas."
    )
    L.append(
        "- **Duplicado entre fuentes:** se detectó un par Revolico–Facebook de la "
        f"misma propiedad y el mismo precio. Se conserva en la base de {total} "
        f"para no alterar el universo acordado; el n efectivo sería {total - 1} "
        f"si se eliminara."
    )
    L.append(
        "- **Verificación municipal:** el polígono es una simplificación de 11 "
        "vértices y no resuelve casos catastrales a pocos metros del borde. La "
        "regla de título usa la mención textual del anuncio; cuando el título es "
        "ambiguo (por ejemplo, «Ampliación del Sevillano» o «Reparto Flores»), la "
        "publicación se conserva con confianza media y la ambigüedad se "
        "documenta. Las 8 indeterminadas se excluyen, lo que puede introducir un "
        "sesgo de selección."
    )
    L.append(
        "- **Clasificación:** el tipo y la operación se toman de los campos "
        "normalizados; la zona se completa con el texto declarado. Puede haber "
        "errores de asignación, especialmente en títulos ambiguos o sin palabras "
        "clave."
    )
    L.append(
        "- **Campos ausentes:** no hay datos homogéneos de metros cuadrados, "
        "estado legal, número de baños, año de construcción, vendedor o agencia. "
        "Solo 6 publicaciones de Facebook traen `area_m2`, y ninguna de Revolico: "
        "no se puede calcular precio por m² ni distinguir particulares de "
        "intermediarios."
    )
    L.append(
        f"- **Alquiler:** solo {len(alquileres)} publicaciones, "
        f"{len(alquileres_con_precio)} con precio y ninguno en USD. No se puede "
        f"estimar un precio de alquiler ni comparar compra y alquiler."
    )
    L.append(
        f"- **Zonas:** solo {total_con_zona} de {total} publicaciones "
        f"({pct(total_con_zona, total):.1f}%) especifican zona. Los promedios "
        f"por barrio se basan en subgrupos pequeños (n = 5–25) y deben leerse "
        f"como evidencia descriptiva."
    )
    L.append(
        "- **CUP:** el único precio en CUP no se convierte a USD porque no se "
        "dispone de un tipo de cambio oficial o de mercado claramente definido "
        "para el corte. Se reporta como hallazgo, no como precio comparable."
    )
    L.append(
        "- **Precios de oferta:** los valores son precios publicados, no precios "
        "de transacción. La diferencia entre lo que se pide y lo que se paga no "
        "es observable con estos datos."
    )
    L.append(
        "- **Sesgo de publicación:** las viviendas que no se publican, o que se "
        "publican en canales cerrados, no aparecen en la base. La opacidad "
        "medida es la del mercado digital visible, no la del mercado total."
    )
    L.append("")

    # ------------------------------------------------------------------
    # Anexo: fuentes, cobertura y referencias
    # ------------------------------------------------------------------
    L.append("## Anexo: fuentes, cobertura y referencias")
    L.append("")
    L.append("### A.1 Fuentes y captura")
    L.append("")
    L.append("| Fuente | Uso en el análisis | Corte o captura | Confirmadas |")
    L.append("|---|---|---|---:|")
    L.append(
        f"| Revolico | Anuncios inmobiliarios: título, precio, enlace y fecha "
        f"de verificación | 2026-10-31 | {n_revolico} |"
    )
    L.append(
        f"| Facebook | Anuncios y descripciones: precio y texto parcial | "
        f"2026-11-04 | {n_facebook} |"
    )
    L.append(
        "| GeoJSON municipal | Polígono DPA `23.09` para la comprobación "
        "punto-en-polígono | Copia versionada | — |"
    )
    L.append(
        "| Nominatim / OpenStreetMap | Geocodificación de topónimos; caché "
        "local | `datos/geo/geocoding_lha.json` | — |"
    )
    L.append(
        "| ONEI, Anuario Estadístico de Cuba | Contexto de población, vivienda "
        "y tenencia | `fuentes/anuario_estadistico_notas.md` | — |"
    )
    L.append("")
    L.append("### A.2 Cobertura por campo")
    L.append("")
    L.append("| Campo | Cobertura | n | Lectura |")
    L.append("|---|---:|---:|---|")
    L.append(
        f"| Precio declarado en USD | {pct(usd_declarada, total):.1f}% | "
        f"{usd_declarada}/{total} | Base principal de los análisis de precio. |"
    )
    L.append(
        f"| Precio declarado en CUP | {pct(len(cup), total):.1f}% | "
        f"{len(cup)}/{total} | No se convierte a USD. |"
    )
    L.append(
        f"| Sin precio | {pct(sin_precio_n, total):.1f}% | "
        f"{sin_precio_n}/{total} | Se conserva y se reporta como opacidad. |"
    )
    L.append(
        f"| Zona identificada | {pct(total_con_zona, total):.1f}% | "
        f"{total_con_zona}/{total} | {n_zona_cruda} en ficha + "
        f"{total_con_zona - n_zona_cruda} recuperadas del texto. |"
    )
    L.append(
        f"| Operación declarada | {pct(n_operacion_declarada, total):.1f}% | "
        f"{n_operacion_declarada}/{total} | "
        f"{len(ventas)} ventas y {len(alquileres)} alquileres; "
        f"{len(sin_clasificar)} sin clasificar. |"
    )
    L.append(
        f"| Habitaciones | {pct(n_habitaciones, total):.1f}% | "
        f"{n_habitaciones}/{total} | No hay campo homogéneo; no se estima. |"
    )
    L.append(
        f"| Baños | {pct(n_banos, total):.1f}% | {n_banos}/{total} | "
        f"No hay campo homogéneo; no se estima. |"
    )
    L.append(
        f"| Superficie (m²) | {pct(n_area, total):.1f}% | {n_area}/{total} | "
        f"Solo Facebook (`detalles_propiedad.area_m2`). |"
    )
    L.append(
        f"| Teléfono | {pct(n_telefono, total):.1f}% | {n_telefono}/{total} | "
        f"Contacto declarado; no se usa para inferir intermediación. |"
    )
    L.append(
        f"| Enlace | {pct(n_enlace, total):.1f}% | {n_enlace}/{total} | "
        f"Todos de Revolico. |"
    )
    L.append("")
    L.append("### A.3 Referencias")
    L.append("")
    L.append(
        "- **ONEI.** *Anuario Estadístico de Cuba*. Oficina Nacional de "
        "Estadística e Información, República de Cuba. Notas de uso en "
        "`fuentes/anuario_estadistico_notas.md`."
    )
    L.append(
        "- **OpenStreetMap / Nominatim.** Servicio de geocodificación usado "
        "para traducir topónimos a coordenadas; resultados cacheados en "
        "`datos/geo/geocoding_lha.json`."
    )
    L.append(
        "- **GeoJSON municipal.** `datos/geo/lha.geojson`, copia versionada del "
        "polígono de La Habana; SHA-256 "
        "`b9bbcce811d9bbfcee15f5e904d97dc24cf044cabcf17a870487ad361bb7c9e6`."
    )
    L.append(
        "- **Revolico.** Portal de anuncios clasificados; captura del "
        "2026-10-31. URL base: `https://www.revolico.com`."
    )
    L.append(
        "- **Facebook.** Publicaciones de grupos y páginas de compraventa; "
        "captura del 2026-11-04. No se reproducen enlaces individuales por "
        "privacidad."
    )
    L.append("")
    L.append(
        "> **Nota sobre la evidencia:** los precios son precios de oferta, no "
        "de transacción. No hay datos homogéneos de metros cuadrados, "
        "habitaciones, baños, estado legal ni año de construcción. Las "
        "ausencias se reportan; no se imputan."
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
    print(
        f"Publicaciones: {total} ({n_revolico} Revolico + {n_facebook} Facebook) | "
        f"USD: {len(usd)} | Sin precio: {sin_precio_n}"
    )
    print(
        f"Ventas USD: n={stats_venta['n']} | media={fmt(stats_venta['mean'])} | "
        f"mediana={fmt(stats_venta['median'])} | "
        f"P10-P90={fmt(stats_venta['p10'])}-{fmt(stats_venta['p90'])}"
    )
    print("Preguntas: 30 (A1-A5, B1-B5, C1-C5, D1-D5, E1-E5, F1-F5)")


if __name__ == "__main__":
    main()
