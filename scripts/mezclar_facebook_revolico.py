#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unifica las bases limpias de Facebook y Revolico en un solo JSON.

Entradas:
    datos/limpios/facebook_publicaciones_limpias.json  (42 publicaciones)
    datos/brutos/revolico_crudos_limpio_final.json     (134 anuncios)
Salida:
    datos/limpios/datos_unificados_facebook_revolico.json

Ambas fuentes se llevan a la misma estructura. Cada registro conserva su fuente
(``facebook`` o ``revolico``), un identificador único, los campos normalizados
de tipo, zona y operación, y una lista de posibles duplicados entre fuentes.
"""

import json
import os
import re
import unicodedata
from collections import Counter, defaultdict

FACEBOOK_FILE = "datos/limpios/facebook_publicaciones_limpias.json"
REVOLICO_FILE = "datos/brutos/revolico_crudos_limpio_final.json"
OUTPUT_FILE = "datos/limpios/datos_unificados_facebook_revolico.json"

CAMPOS_COMUNES = [
    "id_publicacion",
    "id_unico",
    "fuente",
    "publicacion",
    "detalles_propiedad",
    "servicios_y_caracteristicas",
    "equipamiento_incluido",
    "precio",
    "contacto",
    "operacion",
    "municipio",
    "municipio_evidencia",
    "estado",
    "motivo_estado",
    "fecha_verificacion",
    "permuta",
    "posibles_duplicados",
]


def cargar_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def id_revolico(anuncio, indice):
    """ID estable: campo id_anuncio o el número final del enlace."""
    if anuncio.get("id_anuncio"):
        return anuncio["id_anuncio"]
    enlace = anuncio.get("enlace", "") or ""
    coincidencia = re.search(r"-(\d{5,})(?:\?|$)", enlace)
    if coincidencia:
        return int(coincidencia.group(1))
    return f"sin-id-{indice}"


def convertir_revolico(anuncio, indice):
    """Convierte un anuncio limpio de Revolico al esquema unificado."""
    titulo = anuncio.get("titulo", "") or ""
    enlace = anuncio.get("enlace", "") or ""
    municipio = anuncio.get("municipio", "") or "10 de Octubre"
    identificador = id_revolico(anuncio, indice)
    precio = anuncio.get("precio")
    moneda = (anuncio.get("moneda") or "").upper() or None
    fecha = anuncio.get("fecha_agregado") or anuncio.get("fecha_verificacion") or ""

    # Importación local para no cargar el generador del informe al importar
    # este módulo desde otros scripts.
    from analisis_final_30_preguntas import (
        clasificar_operacion,
        clasificar_tipo,
        clasificar_zona,
    )

    tipo = clasificar_tipo(titulo)
    zona = clasificar_zona(titulo, enlace)
    operacion = clasificar_operacion(titulo)

    return {
        "id_publicacion": identificador,
        "id_unico": f"revolico-{identificador}",
        "fuente": "revolico",
        "publicacion": {
            "grupo": "Revolico",
            "autor": "Revolico",
            "fecha": fecha,
            "titulo": titulo,
            "enlace": enlace,
        },
        "detalles_propiedad": {
            "tipo": tipo,
            "tipo_original": None,
            "ubicacion": f"{municipio}. {titulo}".strip(),
            "zona": zona,
            "distribucion": [],
        },
        "servicios_y_caracteristicas": [],
        "equipamiento_incluido": [],
        "precio": {
            "monto": precio,
            "moneda": moneda,
            "negociable": False,
            "nota": "Permuta: SÍ" if anuncio.get("permuta") else "Precio fijo",
        },
        "contacto": {
            "telefono": "",
            "metodo": "Vía Revolico",
            "enlace_revolico": enlace,
        },
        "operacion": operacion,
        "municipio": "Diez de Octubre",
        "municipio_evidencia": "filtro estricto",
        "estado": anuncio.get("estado", ""),
        "motivo_estado": anuncio.get("motivo_estado", ""),
        "fecha_verificacion": anuncio.get("fecha_verificacion", ""),
        "permuta": bool(anuncio.get("permuta")),
        "posibles_duplicados": [],
    }


def normalizar_titulo(texto):
    """Minúsculas, sin acentos, sin emojis ni signos repetidos."""
    texto = (texto or "").lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9áéíóúñü ]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def canonizar(registro):
    """Deja un conjunto común de campos y guarda el resto en ``extras``."""
    canonico = {campo: registro.get(campo) for campo in CAMPOS_COMUNES}
    canonico["servicios_y_caracteristicas"] = (
        registro.get("servicios_y_caracteristicas") or []
    )
    canonico["equipamiento_incluido"] = registro.get("equipamiento_incluido") or []
    canonico["detalles_propiedad"] = registro.get("detalles_propiedad") or {}
    canonico["publicacion"] = registro.get("publicacion") or {}
    canonico["precio"] = registro.get("precio") or {}
    canonico["contacto"] = registro.get("contacto") or {}
    canonico["posibles_duplicados"] = registro.get("posibles_duplicados") or []
    canonico["permuta"] = bool(registro.get("permuta"))
    canonico["motivo_estado"] = registro.get("motivo_estado") or ""
    canonico["fecha_verificacion"] = registro.get("fecha_verificacion") or ""
    canonico["extras"] = {
        clave: valor
        for clave, valor in registro.items()
        if clave not in CAMPOS_COMUNES
    }
    return canonico


def marcar_duplicados(registros):
    """Marca coincidencias exactas de título normalizado + precio + tipo."""
    grupos = defaultdict(list)
    for registro in registros:
        publicacion = registro.get("publicacion") or {}
        detalles = registro.get("detalles_propiedad") or {}
        precio = registro.get("precio") or {}
        titulo = normalizar_titulo(publicacion.get("titulo"))
        monto = precio.get("monto")
        if not titulo or monto is None:
            continue
        clave = (titulo, monto, detalles.get("tipo"))
        grupos[clave].append(registro)

    for grupo in grupos.values():
        if len(grupo) < 2:
            continue
        fuentes = {r.get("fuente") for r in grupo}
        if len(fuentes) < 2:
            continue
        for registro in grupo:
            registro["posibles_duplicados"] = [
                otro.get("id_unico")
                for otro in grupo
                if otro.get("id_unico") != registro.get("id_unico")
            ]


def main():
    facebook = cargar_json(FACEBOOK_FILE)
    revolico = cargar_json(REVOLICO_FILE)

    unificados = list(facebook)
    unificados.extend(
        convertir_revolico(anuncio, i)
        for i, anuncio in enumerate(revolico, start=1)
    )
    marcar_duplicados(unificados)
    unificados = [canonizar(r) for r in unificados]

    ids = [r.get("id_unico") for r in unificados]
    duplicados = [i for i, n in Counter(ids).items() if n > 1]
    con_duplicados = [r for r in unificados if r.get("posibles_duplicados")]

    print(f"Facebook limpio: {len(facebook)}")
    print(f"Revolico limpio: {len(revolico)}")
    print(f"Total unificado: {len(unificados)}")
    print(f"IDs únicos:      {len(set(ids))}")
    if duplicados:
        print(f"IDs duplicados:  {duplicados[:10]}")

    print("\nRegistros por fuente:")
    for fuente, count in Counter(r.get("fuente") for r in unificados).most_common():
        print(f"  {fuente}: {count}")

    print("\nRegistros por operación:")
    for operacion, count in Counter(
        r.get("operacion") for r in unificados
    ).most_common():
        print(f"  {operacion}: {count}")

    print(f"\nCoincidencias exactas entre fuentes: {len(con_duplicados)}")
    for registro in con_duplicados:
        print(
            f"  {registro['id_unico']} -> "
            f"{', '.join(registro['posibles_duplicados'])}"
        )

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(unificados, f, ensure_ascii=False, indent=2)

    print(f"\nBase unificada guardada en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
