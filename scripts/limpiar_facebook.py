#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpieza de las publicaciones de Facebook capturadas para el proyecto.

Criterios (los mismos que se aplican a Revolico)
------------------------------------------------
1. MUNICIPIO: se elimina toda publicación cuyo grupo, título, autor o
   ubicación mencione un municipio, reparto o localidad que no pertenezca a
   Diez de Octubre. Se reutiliza la lista de patrones de
   ``limpieza_final_municipio.py`` para que ambas fuentes sean coherentes.
2. PRECIO MÍNIMO: se eliminan los precios declarados inferiores a 1,000 USD
   (o 24,000 CUP). Las publicaciones sin precio se conservan: la ausencia de
   precio es un hallazgo del estudio.

Además, se normalizan los campos que en Facebook aparecen con formas
heterogéneas:
- tipo de inmueble -> Casa / Apartamento / Cuarto / Local / Terreno / Inmueble
- zona -> nombres homogéneos usados en el informe de Revolico
- operación -> Venta / Alquiler / Sin clasificar
- distribución y detalles de estructura -> siempre listas de texto
- fuente, id único y evidencia municipal

Entrada:
    datos/brutos/facebook_crudos_20261104.json       (43 publicaciones)
Salidas:
    datos/limpios/facebook_publicaciones_limpias.json (publicaciones válidas)
    datos/limpios/facebook_eliminados_por_filtro.json (rechazadas y motivo)
"""

import copy
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analisis_final_30_preguntas import clasificar_operacion, clasificar_zona
from limpieza_final_municipio import PATRONES_EXCLUIR, validar_precio

INPUT_FILE = "datos/brutos/facebook_crudos_20261104.json"
OUTPUT_FILE = "datos/limpios/facebook_publicaciones_limpias.json"
REJECTED_FILE = "datos/limpios/facebook_eliminados_por_filtro.json"


def texto_municipio(registro):
    """Texto donde se busca evidencia de otro municipio o localidad."""
    publicacion = registro.get("publicacion") or {}
    detalles = registro.get("detalles_propiedad") or {}
    partes = [
        publicacion.get("grupo"),
        publicacion.get("titulo"),
        publicacion.get("autor"),
        detalles.get("ubicacion"),
    ]
    return " ".join(str(p) for p in partes if p).lower()


def patron_excluido(registro):
    """Devuelve el patrón que delata otro municipio, o None."""
    texto = texto_municipio(registro)
    for patron in PATRONES_EXCLUIR:
        if re.search(patron, texto, re.IGNORECASE):
            return patron
    return None


def clasificar_zona_facebook(ubicacion):
    """Zona homogénea, incluyendo variantes que no usa el clasificador base."""
    zona = clasificar_zona(ubicacion or "", "")
    if zona != "No especificado":
        return zona
    texto = (ubicacion or "").lower()
    if "santo suárez" in texto or "santo suarez" in texto:
        return "Santos Suárez"
    return "No especificado"


def clasificar_tipo_facebook(tipo_original):
    """Mapea las etiquetas libres de Facebook a las categorías del informe."""
    t = (tipo_original or "").strip().lower()
    if not t:
        return "Inmueble"
    # "Casa ... + Apartamento ..." debe seguir siendo Casa: manda el inicio.
    if t.startswith("casa") or "casa" in t or "biplanta" in t:
        return "Casa"
    if "apartamento" in t or t.startswith("apto"):
        return "Apartamento"
    if "cuarto" in t or "habitaci" in t:
        return "Cuarto"
    if "local" in t:
        return "Local"
    if "terreno" in t or "solar" in t:
        return "Terreno"
    return "Inmueble"


def aplanar_lista(valor):
    """Convierte listas, diccionarios anidados o texto en una lista de texto."""
    if valor is None:
        return []
    if isinstance(valor, str):
        return [valor]
    if isinstance(valor, (int, float)):
        return [str(valor)]
    if isinstance(valor, list):
        salida = []
        for item in valor:
            salida.extend(aplanar_lista(item))
        return salida
    if isinstance(valor, dict):
        salida = []
        for clave, item in valor.items():
            if isinstance(item, dict):
                salida.extend(aplanar_lista(item))
            elif isinstance(item, list):
                salida.extend(aplanar_lista(item))
            elif item:
                salida.append(f"{clave}: {item}")
        return salida
    return [str(valor)]


def evidencia_municipio(ubicacion, zona):
    """Clasifica la fuerza de la evidencia municipal de una publicación."""
    if not ubicacion:
        return "sin ubicación"
    texto = ubicacion.lower()
    if (
        "10 de octubre" in texto
        or "diez de octubre" in texto
        or "10/10" in texto
    ):
        return "explícita"
    if zona != "No especificado":
        return "por reparto"
    return "ambigua"


def normalizar_contacto(contacto):
    contacto = copy.deepcopy(contacto) if isinstance(contacto, dict) else {}
    if isinstance(contacto.get("telefonos"), str):
        contacto["telefonos"] = [contacto["telefonos"]]
    if isinstance(contacto.get("whatsapp"), str):
        contacto["whatsapp"] = [contacto["whatsapp"]]
    return contacto


def limpiar_registro(registro):
    """Devuelve una copia normalizada sin alterar los datos originales."""
    limpio = copy.deepcopy(registro)
    detalles = limpio.get("detalles_propiedad") or {}
    precio = limpio.get("precio") or {}

    tipo_original = detalles.get("tipo")
    ubicacion = detalles.get("ubicacion")
    zona = clasificar_zona_facebook(ubicacion)

    distribucion_original = detalles.get("distribucion")
    detalles["distribucion"] = aplanar_lista(distribucion_original)
    if isinstance(distribucion_original, dict):
        detalles["distribucion_detallada"] = copy.deepcopy(distribucion_original)
    detalles["detalles_estructura"] = aplanar_lista(
        detalles.get("detalles_estructura")
    )
    detalles["tipo_original"] = tipo_original or "No especificado"
    detalles["tipo"] = clasificar_tipo_facebook(tipo_original)
    detalles["zona"] = zona

    precio["monto"] = precio.get("monto") if isinstance(
        precio.get("monto"), (int, float)
    ) else None
    moneda = precio.get("moneda")
    precio["moneda"] = moneda.upper() if isinstance(moneda, str) else None
    limpio["precio"] = precio

    limpio["servicios_y_caracteristicas"] = aplanar_lista(
        limpio.get("servicios_y_caracteristicas")
    )
    limpio["equipamiento_incluido"] = aplanar_lista(
        limpio.get("equipamiento_incluido")
    )
    limpio["contacto"] = normalizar_contacto(limpio.get("contacto"))

    publicacion = limpio.get("publicacion") or {}
    texto_operacion = " ".join(
        str(p) for p in [publicacion.get("grupo"), publicacion.get("titulo")] if p
    )
    limpio["operacion"] = clasificar_operacion(texto_operacion)
    limpio["municipio"] = "Diez de Octubre"
    limpio["municipio_evidencia"] = evidencia_municipio(ubicacion, zona)
    limpio["id_unico"] = f"facebook-{limpio.get('id_publicacion')}"
    limpio["fuente"] = "facebook"
    limpio["estado"] = "capturado"
    limpio["publicacion"] = publicacion
    limpio["detalles_propiedad"] = detalles
    return limpio


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        publicaciones = json.load(f)

    print(f"Publicaciones de Facebook en la fuente: {len(publicaciones)}")

    conservadas = []
    eliminadas = []

    for registro in publicaciones:
        patron = patron_excluido(registro)
        if patron:
            eliminadas.append({
                **copy.deepcopy(registro),
                "motivo_eliminacion": "MUNICIPIO_DISTINTO_A_DIEZ_DE_OCTUBRE",
                "patron_detectado": patron,
            })
            continue

        precio = (registro.get("precio") or {}).get("monto")
        moneda = (registro.get("precio") or {}).get("moneda")
        valido, motivo = validar_precio(precio, moneda)
        if not valido:
            eliminadas.append({
                **copy.deepcopy(registro),
                "motivo_eliminacion": motivo,
                "patron_detectado": None,
            })
            continue

        conservadas.append(limpiar_registro(registro))

    motivos = Counter(e["motivo_eliminacion"] for e in eliminadas)
    con_precio = [a for a in conservadas if (a.get("precio") or {}).get("monto") is not None]
    sin_precio = [a for a in conservadas if (a.get("precio") or {}).get("monto") is None]
    usd = [a for a in conservadas if (a.get("precio") or {}).get("moneda") == "USD"]
    cup = [a for a in conservadas if (a.get("precio") or {}).get("moneda") == "CUP"]
    tipos = Counter((a.get("detalles_propiedad") or {}).get("tipo") for a in conservadas)
    zonas = Counter((a.get("detalles_propiedad") or {}).get("zona") for a in conservadas)
    operaciones = Counter(a.get("operacion") for a in conservadas)
    evidencias = Counter(a.get("municipio_evidencia") for a in conservadas)

    print("\n=== RESULTADO DE LA LIMPIEZA DE FACEBOOK ===")
    print(f"Total fuente:          {len(publicaciones)}")
    print(f"Publicaciones eliminadas: {len(eliminadas)}")
    print(f"Publicaciones conservadas: {len(conservadas)}")
    print("\nMotivos de eliminación:")
    for motivo, count in motivos.most_common():
        print(f"  {motivo}: {count}")
    print("\nComposición de la base limpia:")
    print(f"  Con precio: {len(con_precio)}")
    print(f"  Sin precio: {len(sin_precio)}")
    print(f"  USD:        {len(usd)}")
    print(f"  CUP:        {len(cup)}")
    print("\nTipos:")
    for tipo, count in tipos.most_common():
        print(f"  {tipo}: {count}")
    print("\nZonas:")
    for zona, count in zonas.most_common():
        print(f"  {zona}: {count}")
    print("\nOperaciones:")
    for operacion, count in operaciones.most_common():
        print(f"  {operacion}: {count}")
    print("\nEvidencia municipal:")
    for evidencia, count in evidencias.most_common():
        print(f"  {evidencia}: {count}")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(REJECTED_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(conservadas, f, ensure_ascii=False, indent=2)
    with open(REJECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(eliminadas, f, ensure_ascii=False, indent=2)

    print(f"\nBase limpia guardada en:   {OUTPUT_FILE}")
    print(f"Eliminadas guardadas en:   {REJECTED_FILE}")


if __name__ == "__main__":
    main()
