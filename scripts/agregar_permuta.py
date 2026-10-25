#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agrega el campo 'permuta' a ambos archivos JSON de datos brutos.

Lógica:
- Palabras positivas (indican permuta): permuta, permuto, permutación, intercambio, cambio
- Palabras negativas (niegan permuta): no permuto, no permuta, no acepto permuta(s),
  sin permuta, no intercambio, no cambio, no acepto intercambio, etc.
- Regla: si hay negativa -> false; si hay positiva y no hay negativa -> true;
  si no hay nada -> false.
"""

import json
import re
import os

ARCHIVOS = [
    "datos/brutos/revolico_crudos.json",
    "datos/brutos/elcaiman_crudos.json",
]

PALABRAS_POSITIVAS = [
    r"\bpermuta\b",
    r"\bpermuto\b",
    r"\bpermutaci[oó]n\b",
    r"\bintercambio\b",
    r"\bcambio\b",
]

PALABRAS_NEGATIVAS = [
    r"\bno\s+permuto\b",
    r"\bno\s+permuta\b",
    r"\bno\s+acepto\s+permuta\b",
    r"\bno\s+acepto\s+permutas\b",
    r"\bsin\s+permuta\b",
    r"\bno\s+intercambio\b",
    r"\bno\s+cambio\b",
    r"\bno\s+acepto\s+intercambio\b",
]

patron_positivo = re.compile("|".join(PALABRAS_POSITIVAS), re.IGNORECASE)
patron_negativo = re.compile("|".join(PALABRAS_NEGATIVAS), re.IGNORECASE)


def detectar_permuta(titulo):
    if not titulo:
        return False
    if patron_negativo.search(titulo):
        return False
    return bool(patron_positivo.search(titulo))


def main():
    for path in ARCHIVOS:
        if not os.path.exists(path):
            print(f"No existe: {path}")
            continue

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        for anuncio in data:
            titulo = anuncio.get("titulo", "")
            anuncio["permuta"] = detectar_permuta(titulo)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        con_permuta = sum(1 for a in data if a["permuta"])
        print(f"{path}: {len(data)} anuncios, {con_permuta} con permuta=true")


if __name__ == "__main__":
    main()
