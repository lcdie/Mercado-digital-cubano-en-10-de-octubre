#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cifras de control del informe final (solo lectura).

Comprueba que las cifras que sostienen el informe coincidan con los datos
generados. No modifica archivos. Sale con código 0 si todo cuadra y con
código 1 si alguna cifra no coincide.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

from analisis_final_30_preguntas import (  # noqa: E402
    INPUT_DESCARTADOS,
    cargar_anuncios_confirmados,
    pct,
    stats,
)


def cargar_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def tiene_dato(valor):
    return valor not in (None, "", "No especificado", "Sin especificar", [], {})


def main() -> int:
    anuncios, verificacion = cargar_anuncios_confirmados()
    total = len(anuncios)
    fuentes = Counter(a.get("fuente") for a in anuncios)
    conteo = Counter(r.get("resultado") for r in verificacion)

    precios = [a["_precio"] for a in anuncios if a["_precio"] is not None]
    usd = [
        a["_precio"] for a in anuncios
        if a["_precio"] is not None and a["_moneda"] == "USD"
    ]
    cup = [
        a["_precio"] for a in anuncios
        if a["_precio"] is not None and a["_moneda"] == "CUP"
    ]
    ventas_usd = [
        a["_precio"] for a in anuncios
        if a["_op"] == "Venta" and a["_precio"] is not None and a["_moneda"] == "USD"
    ]
    s = stats(ventas_usd)

    zonas = Counter(a["_zona"] for a in anuncios if a["_zona"] != "No especificado")
    con_zona = sum(zonas.values())
    sin_zona = total - con_zona
    top4 = sum(c for _, c in zonas.most_common(4))

    completo = sum(
        1 for a in anuncios
        if a["_precio"] is not None and a["_zona"] != "No especificado"
    )
    ambos = sum(
        1 for a in anuncios
        if a["_precio"] is None and a["_zona"] == "No especificado"
    )

    descartados = cargar_json(INPUT_DESCARTADOS)["registros"]
    universo = {
        r["id_unico"]: r
        for r in cargar_json(RAIZ / "datos" / "limpios" / "datos_unificados_facebook_revolico.json")
    }
    descartados_universo = [d for d in descartados if d.get("en_universo_unificado")]
    integridad = all(
        d.get("registro_unificado") == universo.get(d["id_unico"])
        for d in descartados_universo
    )

    pares = {
        frozenset([a["id_unico"]] + (a.get("posibles_duplicados") or []))
        for a in anuncios
        if a.get("posibles_duplicados")
    }
    n_pares = len(pares)
    n_efectivo = total - n_pares

    zona_cruda = sum(
        1 for a in anuncios
        if tiene_dato((a.get("detalles_propiedad") or {}).get("zona"))
    )
    operacion_declarada = sum(1 for a in anuncios if a["_op"] != "Sin clasificar")
    habitaciones = sum(
        1 for a in anuncios
        if tiene_dato((a.get("detalles_propiedad") or {}).get("habitaciones"))
    )
    banos = sum(
        1 for a in anuncios
        if tiene_dato((a.get("detalles_propiedad") or {}).get("banos"))
    )
    superficie = sum(
        1 for a in anuncios
        if tiene_dato((a.get("detalles_propiedad") or {}).get("area_m2"))
    )
    telefono = sum(
        1 for a in anuncios
        if tiene_dato((a.get("contacto") or {}).get("telefono"))
    )
    enlace = sum(
        1 for a in anuncios
        if tiene_dato((a.get("publicacion") or {}).get("enlace"))
    )

    checks = [
        ("publicaciones confirmadas", total, 122),
        ("Revolico confirmadas", fuentes.get("revolico", 0), 83),
        ("Facebook confirmadas", fuentes.get("facebook", 0), 39),
        ("resultado NO", conteo.get("NO", 0), 46),
        ("resultado INDETERMINADO", conteo.get("INDETERMINADO", 0), 8),
        ("resultado CONTRADICTORIO", conteo.get("CONTRADICTORIO", 0), 0),
        ("descartados conservados", len(descartados), 55),
        (
            "descartados fuera del universo",
            sum(1 for d in descartados if not d.get("en_universo_unificado")),
            1,
        ),
        ("descartados del universo", len(descartados_universo), 54),
        ("integridad del registro unificado", integridad, True),
        ("precios USD", len(usd), 106),
        ("precios CUP", len(cup), 1),
        ("sin precio", total - len(precios), 15),
        ("ventas USD n", s["n"], 43),
        ("ventas USD media", round(s["mean"], 2), 26023.26),
        ("ventas USD mediana", round(s["median"], 2), 20000.00),
        ("ventas USD P10", round(s["p10"], 2), 6200.00),
        ("ventas USD P90", round(s["p90"], 2), 60000.00),
        ("zona identificada", con_zona, 91),
        ("sin zona", sin_zona, 31),
        ("top-4 zonas", top4, 69),
        ("precio y zona", completo, 82),
        ("sin precio ni zona", ambos, 6),
        ("zona cruda en ficha", zona_cruda, 84),
        ("pares duplicados", n_pares, 1),
        ("n efectivo", n_efectivo, 121),
        ("operación declarada", operacion_declarada, 53),
        ("habitaciones", habitaciones, 0),
        ("baños", banos, 0),
        ("superficie", superficie, 6),
        ("teléfono", telefono, 29),
        ("enlace", enlace, 83),
        ("USD sobre moneda declarada", round(pct(len(usd), len(usd) + len(cup)), 1), 99.1),
        ("USD sobre total", round(pct(len(usd), total), 1), 86.9),
        ("zona sobre total", round(pct(con_zona, total), 1), 74.6),
        ("precio y zona sobre total", round(pct(completo, total), 1), 67.2),
    ]

    fallos = 0
    print("CIFRAS DE CONTROL DEL INFORME FINAL")
    print(f"Base: {total} publicaciones confirmadas")
    print("-" * 72)
    for etiqueta, real, esperado in checks:
        if isinstance(esperado, bool):
            ok = real == esperado
        elif isinstance(esperado, float):
            ok = abs(real - esperado) < 0.01
        else:
            ok = real == esperado
        estado = "OK  " if ok else "FALLA"
        print(f"{estado}  {etiqueta:<38} {real!s:>12}   esperado: {esperado}")
        if not ok:
            fallos += 1

    print("-" * 72)
    if fallos:
        print(f"RESULTADO: {fallos} cifra(s) no coinciden. Revisa el informe antes de entregarlo.")
        return 1
    print(f"RESULTADO: {len(checks)} cifras verificadas; todas coinciden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
