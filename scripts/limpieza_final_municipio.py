#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpieza FINAL de datos del mercado inmobiliario de Diez de Octubre.

Criterios de FILTRADO ESTRICTO:
1. PRECIO MÍNIMO 1000 USD: Se eliminan anuncios con precio < 1000 USD (o equivalente).
   - Anuncios sin precio declarado se mantienen solo si no tienen moneda especificada
     (para revisión manual), pero los que tienen precio < 1000 USD se eliminan.
2. MUNICIPIO: Solo se mantienen anuncios de Diez de Octubre y sus repartos.
   Se ELIMINAN anuncios que mencionen en título o enlace:
   Centro Habana, Playa, Vedado, Habana del Este, Guanabacoa, San Miguel, Alamar,
   el Cerro, La Lisa, Cotorro, Regla, Nuevo Vedado, La Víbora (si es como zona aparte),
   etc.
3. Solo municipios de Diez de Octubre y sus repartos (Santos Suárez, La Víbora, Lawton,
   Luyano, El Sevillano, El Mónaco, Santa Catalina, Vista Alegre, Reparto Asunción,
   Reparto Lawton, Reparto Sevillano, Calzada 10 de Octubre, etc.)

Lee:  datos/brutos/revolico_crudos_limpio.json
Escribe: datos/brutos/revolico_crudos_limpio_final.json
Escribe: datos/limpios/anuncios_eliminados_por_filtro_final.json
"""

import json
import re
from datetime import datetime
from collections import Counter

INPUT_FILE = "datos/brutos/revolico_crudos_limpio.json"
OUTPUT_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
REJECTED_FILE = "datos/limpios/anuncios_eliminados_por_filtro_final.json"

# Municipios y zonas de La Habana QUE NO SON Diez de Octubre - EXCLUIR completamente
MUNICIPIOS_EXCLUIDOS = [
    # Municipios completos de La Habana
    "centro habana", "centro habana", "playa", "vedado", "nuevo vedado",
    "habana del este", "guanabacoa", "san miguel", "alamar", "el cerro",
    "cerro", "la lisa", "cotorro", "regla", "marianao", "arroyo naranjo",
    "boyeros", "guanabo", "guanabacoa", "san miguel del padrón",
    # Barrios específicos de otros municipios
    "santa amalia", "siboney", "miramar", "buena vista", "atares",
    "cayo santa maría", "varadero", "jibacoa", "cayo guano", "cayo levisa",
    # Otras zonas no de 10 de Octubre
    "cotorro", "regla", "casablanca", "guanabo",
]

# Zonas VÁLIDAS de Diez de Octubre (para validar que sí pertenece)
ZONAS_DIEZ_DE_OCTUBRE = [
    "diez de octubre", "10 de octubre", "santos suárez", "santos suarez",
    "la víbora", "la vibora", "lawton", "luyano", "luyanó", "el sevillano",
    "sevillano", "mónaco", "monaco", "asunción", "asuncion",
    "santa catalina", "vista alegre", "reparto asunción", "reparto lawton",
    "reparto sevillano", "vía blanca", "via blanca",
    "calzada 10 de octubre", "calzada diez de octubre",
    "diez de octubre y", "10 de octubre y",
    "reparto diezmero", "diezmero",
]

# Patrones de excluir en título/enlaces
PATRONES_EXCLUIR = [
    r"centro habana", r"playa\b", r"vedado", r"nuevo vedado",
    r"habana del este", r"guanabacoa", r"san miguel", r"alamar",
    r"el cerro", r"cerro\b", r"la lisa", r"cotorro", r"regla\b",
    r"santa amalia", r"siboney", r"miramar", "buena vista",
    "cayo santa mar", "cayo jibacoa", "cayo guano", "cayo levisa",
]


def contiene_municipio_excluido(titulo, enlace):
    """Detecta si el anuncio menciona municipios que NO son Diez de Octubre."""
    texto = (titulo + " " + (enlace or "")).lower()
    for patron in PATRONES_EXCLUIR:
        if re.search(patron, texto, re.IGNORECASE):
            return True
    return False


def es_de_diez_de_octubre(titulo, enlace, municipio):
    """Determina si el anuncio pertenece a Diez de Octubre."""
    texto = (titulo + " " + (enlace or " ") + " " + (municipio or "")).lower()

    # Primero verificar si contiene zonas de Diez de Octubre
    for zona in ZONAS_DIEZ_DE_OCTUBRE:
        if zona in texto:
            return True

    # Si no menciona zona de Diez de Octubre, pero el municipio dice Diez de Octubre
    if "diez de octubre" in municipio.lower() or "10 de octubre" in municipio.lower():
        return True

    return False


def es_precio_valido(precio, moneda):
    """Verifica si el precio cumple el mínimo de 1000 USD."""
    if precio is None:
        # Sin precio declarado - se mantiene para revisión manual, pero marcado
        return True, "sin_precio"

    if moneda == "USD":
        if precio < 1000:
            return False, "precio_muy_bajo_usd"
        return True, "valido"

    if moneda == "CUP":
        # Para CUP, usar tasa aproximada 1 USD = 24 CUP (mercado informal)
        # 1000 USD = 24,000 CUP aproximadamente
        if precio < 24000:
            return False, "precio_muy_bajo_cup"
        return True, "valido"

    # Moneda desconocida o vacía
    return True, "moneda_desconocida"


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        anuncios = json.load(f)

    print(f"Total anuncios iniciales: {len(anuncios)}")

    anuncios_limpios = []
    anuncios_eliminados = []

    for a in anuncios:
        titulo = a.get("titulo", "") or ""
        enlace = a.get("enlace", "") or ""
        precio = a.get("precio")
        moneda = (a.get("moneda") or "").upper()
        municipio = a.get("municipio", "") or ""

        motivo_eliminacion = None

        # 1. Verificar si es de Diez de Octubre (municipio y zonas)
        if not es_de_diez_de_octubre(titulo, enlace, municipio):
            motivo_eliminacion = "MUNICIPIO_NO_ES_10_DE_OCTUBRE"

        # 2. Verificar si contiene municipios excluidos en título/enlace
        elif contiene_municipio_excluido(titulo, enlace):
            motivo_eliminacion = "MUNICIPIO_EXCLUIDO_EN_TITULO_ENLACE"

        # 3. Verificar precio mínimo
        elif precio is not None:
            valido, motivo = es_precio_valido(precio, moneda)
            if not valido:
                motivo_eliminacion = motivo

        # 4. Si tiene moneda vacía pero tiene precio numérico muy bajo, también sospechoso
        elif precio is not None and moneda == "":
            if precio < 1000:
                motivo_eliminacion = "PRECIO_SIN_MONEDA_PERO_BAJO"

        if motivo_eliminacion:
            anuncios_eliminados.append({
                "titulo": titulo,
                "precio": precio,
                "moneda": moneda,
                "municipio": municipio,
                "enlace": enlace,
                "motivo": motivo_eliminacion
            })
        else:
            anuncios_limpios.append(a)

    print(f"\n=== RESULTADOS DE LIMPIEZA ===")
    print(f"Total inicial: {len(anuncios)}")
    print(f"Anuncios eliminados: {len(anuncios_eliminados)}")
    print(f"Anuncios limpios finales: {len(anuncios_limpios)}")
    print()

    # Contar motivos de eliminación
    motivos_counter = Counter(e["motivo"] for e in anuncios_eliminados)
    print("Motivos de eliminación:")
    for motivo, count in motivos_counter.most_common():
        print(f"  {motivo}: {count}")
    print()

    # Estadísticas de los limpios
    con_precio = [a for a in anuncios_limpios if a.get("precio") is not None]
    sin_precio = [a for a in anuncios_limpios if not a.get("precio")]
    usd = [a for a in anuncios_limpios if a.get("moneda") == "USD"]
    cup = [a for a in anuncios_limpios if a.get("moneda") == "CUP"]

    print(f"  Con precio: {len(con_precio)}")
    print(f"  Sin precio: {len(sin_precio)}")
    print(f"  USD: {len(usd)}")
    print(f"  CUP: {len(cup)}")

    if usd:
        precios_usd = [a["precio"] for a in usd]
        print(f"  Precio USD - Min: {min(precios_usd):,}, Max: {max(precios_usd):,}")
        print(f"  Promedio USD: {sum(precios_usd)/len(precios_usd):,.2f}")

    if cup:
        precios_cup = [a["precio"] for a in cup]
        print(f"  Precio CUP - Min: {min(precios_cup):,}, Max: {max(precios_cup):,}")

    # Guardar archivo limpio
    import os
    os.makedirs("datos/brutos", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(anuncios_limpios, f, ensure_ascii=False, indent=2)

    # Guardar eliminados
    os.makedirs("datos/limpios", exist_ok=True)
    with open(REJECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(anuncios_eliminados, f, ensure_ascii=False, indent=2)

    print(f"\nArchivo limpio guardado: {OUTPUT_FILE}")
    print(f"Archivo de eliminados guardado: {REJECTED_FILE}")


if __name__ == "__main__":
    main()
