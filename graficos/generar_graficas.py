#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera las 5 gráficas esenciales para la exposición del mercado inmobiliario
de Diez de Octubre. Lee la base verificada y guarda PNG en graficos/.
"""
import json
import os
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


def zona(r):
    d = r.get("detalles_propiedad") or {}
    return d.get("zona") or "No especificado"


def moneda(r):
    p = r.get("precio")
    if isinstance(p, dict):
        return (p.get("moneda") or "").upper()
    return ""


# ---------- 1. Histograma de precios de venta en USD ----------
ventas_usd = sorted([
    monto(r) for r in datos
    if monto(r) is not None and moneda(r) == "USD" and r.get("operacion") == "Venta"
])

plt.figure(figsize=(8, 5))
plt.hist(ventas_usd, bins=15, color="#2a5298", edgecolor="white", alpha=0.85)
plt.axvline(sum(ventas_usd) / len(ventas_usd), color="#e74c3c", linestyle="--",
            label=f"Media: ${sum(ventas_usd)/len(ventas_usd):,.0f}")
plt.axvline(sorted(ventas_usd)[len(ventas_usd)//2], color="#27ae60", linestyle="-",
            label=f"Mediana: ${sorted(ventas_usd)[len(ventas_usd)//2]:,.0f}")
plt.title("Precios de venta en USD — Diez de Octubre (n = 43)")
plt.xlabel("Precio (USD)")
plt.ylabel("Cantidad de anuncios")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, "grafico_1_precios_venta_usd.png"), dpi=150)
plt.close()

# ---------- 2. Barras horizontales por zona ----------
zonas = Counter(zona(r) for r in datos if zona(r) != "No especificado")
top_zonas = zonas.most_common(8)
nombres = [z[0] for z in top_zonas][::-1]
valores = [z[1] for z in top_zonas][::-1]

plt.figure(figsize=(8, 5))
plt.barh(nombres, valores, color="#1e3c72")
plt.title("Oferta por zona — Diez de Octubre (n = 91 con zona)")
plt.xlabel("Cantidad de anuncios")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "grafico_2_oferta_por_zona.png"), dpi=150)
plt.close()

# ---------- 3. Media vs Mediana por zona (USD) ----------
precios_zona = {}
for r in datos:
    m = monto(r)
    z = zona(r)
    if m is not None and moneda(r) == "USD" and z != "No especificado":
        precios_zona.setdefault(z, []).append(m)

zonas_con_n = {z: v for z, v in precios_zona.items() if len(v) >= 5}
orden = sorted(zonas_con_n.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True)
nombres_z = [z[0] for z in orden][::-1]
medias = [sum(z[1]) / len(z[1]) for z in orden][::-1]
medianas = [sorted(z[1])[len(z[1]) // 2] for z in orden][::-1]

x = range(len(nombres_z))
plt.figure(figsize=(9, 5))
plt.bar([i - 0.2 for i in x], medias, width=0.4, label="Media", color="#e67e22")
plt.bar([i + 0.2 for i in x], medianas, width=0.4, label="Mediana", color="#2ecc71")
plt.xticks(x, nombres_z, rotation=45, ha="right")
plt.title("Media vs Mediana por zona (USD, n ≥ 5)")
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
plt.title("Moneda declarada — Diez de Octubre (n = 122)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "grafico_4_moneda.png"), dpi=150)
plt.close()

# ---------- 5. Opacidad: precio y zona ----------
con_precio_zona = sum(1 for r in datos if monto(r) is not None and zona(r) != "No especificado")
solo_precio = sum(1 for r in datos if monto(r) is not None and zona(r) == "No especificado")
solo_zona = sum(1 for r in datos if monto(r) is None and zona(r) != "No especificado")
ninguno = sum(1 for r in datos if monto(r) is None and zona(r) == "No especificado")

labels_op = ["Precio + zona", "Solo precio", "Solo zona", "Ninguno"]
valores_op = [con_precio_zona, solo_precio, solo_zona, ninguno]
colores_op = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]

plt.figure(figsize=(6, 6))
plt.pie(valores_op, labels=labels_op, colors=colores_op, autopct="%1.1f%%", startangle=90)
plt.title("Opacidad de información — Diez de Octubre (n = 122)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "grafico_5_opacidad.png"), dpi=150)
plt.close()

print("Gráficas generadas en:", OUT)
for f in sorted(os.listdir(OUT)):
    print(" -", f)
