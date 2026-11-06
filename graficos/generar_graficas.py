#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las 5 gráficas esenciales para la exposición del mercado inmobiliario
de Diez de Octubre. Lee la base verificada y guarda PNG en graficos/.

Usa la misma lógica de zona normalizada que el informe (zona de ficha +
recuperada del texto), y mediana real (statistics.median) en lugar de
sorted[n//2]. Los n de los títulos se calculan dinámicamente.
"""
import json
import os
import statistics
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(RAIZ, "datos", "limpios", "unificado_confirmados_diez_octubre.json")
OUT = os.path.join(RAIZ, "graficos")
os.makedirs(OUT, exist_ok=True)

with open(BASE, encoding="utf-8") as f:
    datos = json.load(f)


def monto(r):
    p = r.get("precio")
    if isinstance(p, dict):
        return p.get("monto") or p.get("monto_actual")
    return p


def moneda(r):
    p = r.get("precio")
    if isinstance(p, dict):
        return (p.get("moneda") or "").upper()
    return ""


def operacion(r):
    return r.get("operacion") or "Sin clasificar"


def texto_anuncio(r):
    """Todo el texto declarado, en minúsculas, para buscar señales de zona."""
    detalles = r.get("detalles_propiedad") or {}
    publicacion = r.get("publicacion") or {}
    partes = [
        publicacion.get("titulo", ""),
        publicacion.get("enlace", ""),
        publicacion.get("grupo", ""),
        detalles.get("ubicacion", ""),
        detalles.get("zona", ""),
    ]
    for clave in ("distribucion", "detalles_estructura"):
        partes += detalles.get(clave) or []
    partes += r.get("servicios_y_caracteristicas") or []
    partes += r.get("equipamiento_incluido") or []
    return " ".join(str(p) for p in partes if p).lower()


ZONAS = [
    ("Santos Suárez", ["santos suárez", "santos suarez"]),
    ("Lawton", ["lawton"]),
    ("La Víbora", ["la víbora", "la vibora"]),
    ("El Sevillano", ["el sevillano"]),
    ("Luyano", ["luyano"]),
    ("El Mónaco", ["el mónaco", "el monaco"]),
    ("Santa Catalina", ["santa catalina"]),
    ("Calzada 10 de Octubre", ["calzada 10 de octubre"]),
    ("Vía Blanca", ["vía blanca", "via blanca"]),
    ("Vista Alegre", ["vista alegre"]),
    ("Cotorro", ["cotorro"]),
    ("Almendares", ["almendares"]),
]


def zona_normalizada(r):
    """Zona de ficha, recuperada del texto si falta."""
    detalles = r.get("detalles_propiedad") or {}
    zona = (detalles.get("zona") or "").strip()
    if zona and zona.lower() not in ("no especificado", "sin especificar"):
        return zona
    texto = texto_anuncio(r)
    for nombre, variantes in ZONAS:
        if any(v in texto for v in variantes):
            return nombre
    return "No especificado"


def mediana(valores):
    if not valores:
        return 0.0
    return statistics.median(valores)


# ---------- 1. Histograma de precios de venta en USD ----------
ventas_usd = sorted([
    monto(r) for r in datos
    if monto(r) is not None and moneda(r) == "USD" and operacion(r) == "Venta"
])
n_ventas = len(ventas_usd)
media_ventas = sum(ventas_usd) / n_ventas if n_ventas else 0

plt.figure(figsize=(8, 5))
plt.hist(ventas_usd, bins=15, color="#2a5298", edgecolor="white", alpha=0.85)
plt.axvline(media_ventas, color="#e74c3c", linestyle="--",
            label=f"Media: ${media_ventas:,.0f}")
plt.axvline(mediana(ventas_usd), color="#27ae60", linestyle="-",
            label=f"Mediana: ${mediana(ventas_usd):,.0f}")
plt.title(f"Precios de venta en USD — Diez de Octubre (n = {n_ventas})")
plt.xlabel("Precio (USD)")
plt.ylabel("Cantidad de anuncios")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, "grafico_1_precios_venta_usd.png"), dpi=150)
plt.close()

# ---------- 2. Barras horizontales por zona ----------
zonas = Counter(zona_normalizada(r) for r in datos if zona_normalizada(r) != "No especificado")
total_con_zona = sum(zonas.values())
top_zonas = zonas.most_common(8)
nombres = [z[0] for z in top_zonas][::-1]
valores = [z[1] for z in top_zonas][::-1]

plt.figure(figsize=(8, 5))
plt.barh(nombres, valores, color="#1e3c72")
plt.title(f"Oferta por zona — Diez de Octubre (n = {total_con_zona} con zona)")
plt.xlabel("Cantidad de anuncios")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "grafico_2_oferta_por_zona.png"), dpi=150)
plt.close()

# ---------- 3. Media vs Mediana por zona (USD) ----------
precios_zona = {}
for r in datos:
    m = monto(r)
    z = zona_normalizada(r)
    if m is not None and moneda(r) == "USD" and z != "No especificado":
        precios_zona.setdefault(z, []).append(m)

# Solo ventas con precio USD para consistencia con el informe
precios_zona_venta = {}
for r in datos:
    m = monto(r)
    z = zona_normalizada(r)
    if m is not None and moneda(r) == "USD" and operacion(r) == "Venta" and z != "No especificado":
        precios_zona_venta.setdefault(z, []).append(m)

zonas_con_n = {z: v for z, v in precios_zona_venta.items() if len(v) >= 5}
orden = sorted(zonas_con_n.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True)
nombres_z = [z[0] for z in orden][::-1]
medias = [sum(z[1]) / len(z[1]) for z in orden][::-1]
medianas_z = [mediana(z[1]) for z in orden][::-1]

x = range(len(nombres_z))
plt.figure(figsize=(9, 5))
plt.bar([i - 0.2 for i in x], medias, width=0.4, label="Media", color="#e67e22")
plt.bar([i + 0.2 for i in x], medianas_z, width=0.4, label="Mediana", color="#2ecc71")
plt.xticks(x, nombres_z, rotation=45, ha="right")
plt.title("Media vs Mediana por zona (USD, ventas, n ≥ 5)")
plt.ylabel("USD")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, "grafico_3_media_mediana_zona.png"), dpi=150)
plt.close()

# ---------- 4. Moneda declarada ----------
monedas = Counter(moneda(r) for r in datos if moneda(r))
sin_precio = sum(1 for r in datos if monto(r) is None)
labels = []
valores = []
colores = []
if monedas.get("USD"):
    labels.append("USD")
    valores.append(monedas["USD"])
    colores.append("#27ae60")
if monedas.get("CUP"):
    labels.append("CUP")
    valores.append(monedas["CUP"])
    colores.append("#f39c12")
if sin_precio:
    labels.append("Sin precio")
    valores.append(sin_precio)
    colores.append("#95a5a6")

plt.figure(figsize=(6, 6))
plt.pie(valores, labels=labels, colors=colores, autopct="%1.1f%%", startangle=90)
plt.title(f"Moneda declarada — Diez de Octubre (n = {len(datos)})")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "grafico_4_moneda.png"), dpi=150)
plt.close()

# ---------- 5. Opacidad: precio y zona ----------
def zona_ok(r):
    return zona_normalizada(r) != "No especificado"

con_precio_zona = sum(1 for r in datos if monto(r) is not None and zona_ok(r))
solo_precio = sum(1 for r in datos if monto(r) is not None and not zona_ok(r))
solo_zona = sum(1 for r in datos if monto(r) is None and zona_ok(r))
ninguno = sum(1 for r in datos if monto(r) is None and not zona_ok(r))

labels_op = ["Precio + zona", "Solo precio", "Solo zona", "Ninguno"]
valores_op = [con_precio_zona, solo_precio, solo_zona, ninguno]
colores_op = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]

plt.figure(figsize=(6, 6))
plt.pie(valores_op, labels=labels_op, colors=colores_op, autopct="%1.1f%%", startangle=90)
plt.title(f"Opacidad de información — Diez de Octubre (n = {len(datos)})")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "grafico_5_opacidad.png"), dpi=150)
plt.close()

print("Gráficas generadas en:", OUT)
for f in sorted(os.listdir(OUT)):
    print(" -", f)
print(f"\nResumen: n_ventas_usd={n_ventas}, total_con_zona={total_con_zona}, "
      f"con_precio_zona={con_precio_zona}, ninguno={ninguno}")
