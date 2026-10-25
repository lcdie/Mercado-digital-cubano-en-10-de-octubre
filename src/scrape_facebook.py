#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para obtener datos de Facebook Graph API (mercado inmobiliario).

IMPORTANTE: Este script requiere un Access Token válido de Facebook Graph API.
Pasos previos (debes hacerlos tú):
  1. Ve a https://developers.facebook.com/
  2. Inicia sesión con tu cuenta de Facebook
  3. Crea una app nueva
  4. Solicita permisos: user_posts, groups_access_member_info, public_profile
  5. Genera un Access Token desde el Graph API Explorer

Limitaciones conocidas:
  - No se pueden leer grupos de terceros a menos que seas administrador
  - Los tokens de corta duración expiran en 1 hora
  - Facebook restringe fuertemente el scraping de grupos públicos

Resultados: datos/brutos/facebook_crudos.json  (titulo, precio, moneda, municipio, enlace, fuente, permuta)
"""

import json
import os
import re
import time
import sys
from urllib.parse import urljoin

import requests

# Configuración de la API de Facebook
FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v19.0"

# Carpeta y archivo de salida
OUTPUT_DIR = "datos/brutos"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "facebook_crudos.json")

# Palabras clave para búsqueda en Facebook (mercado inmobiliario 10 de Octubre)
BUSQUEDAS_SUGERIDAS = [
    "casas en venta 10 de octubre La Habana",
    "apartamento venta Diez de Octubre",
    "vivienda Diez de Octubre La Habana",
    "casas alquiler Diez de Octubre",
    "permuta casa 10 de octubre",
]

# Palabras para detectar permuta
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


def detectar_permuta(texto):
    """
    Detecta si un anuncio menciona permuta.
    Regla: si hay negativa -> false; si hay positiva y no hay negativa -> true;
    si no hay nada -> false.
    """
    if not texto:
        return False
    if patron_negativo.search(texto):
        return False
    return bool(patron_positivo.search(texto))


def parse_precio(texto):
    """
    Convierte un texto de precio tipo "$4,000 USD" o "50,000 CUP" en
    (numero, moneda). Devuelve (None, "") si no se puede parsear.
    """
    if not texto:
        return None, ""

    texto = texto.strip()

    # Detectar moneda
    moneda = ""
    m_moneda = re.search(r"\b([A-Z]{3})\b", texto)
    if m_moneda:
        moneda = m_moneda.group(1).upper()
    elif "$" in texto:
        moneda = "USD"
    elif "€" in texto:
        moneda = "EUR"

    # Extraer número
    m_num = re.search(r"[\d][\d.,]*", texto)
    if not m_num:
        return None, moneda

    num_str = m_num.group(0).replace(",", "").replace(".", "")

    try:
        valor = int(num_str)
    except ValueError:
        try:
            valor = float(num_str)
        except ValueError:
            valor = None

    return valor, moneda


def validar_token(access_token):
    """
    Valida que el access token sea correcto consultando /me.
    Devuelve True si el token es válido, False en caso contrario.
    """
    url = f"{FACEBOOK_GRAPH_URL}/me"
    params = {"access_token": access_token, "fields": "id,name"}
    try:
        respuesta = requests.get(url, params=params, timeout=30)
        respuesta.raise_for_status()
        data = respuesta.json()
        print(f"Token válido. Usuario: {data.get('name', 'N/A')} (ID: {data.get('id', 'N/A')})")
        return True
    except requests.RequestException as e:
        print(f"Token inválido o error de conexión: {e}")
        return False


def buscar_publicaciones(access_token, consulta, limite=50):
    """
    Busca publicaciones en Facebook usando la Graph API.
    Nota: El endpoint /search requiere permisos especiales y puede no funcionar
    para contenido de grupos de terceros.
    """
    url = f"{FACEBOOK_GRAPH_URL}/search"
    params = {
        "access_token": access_token,
        "q": consulta,
        "type": "post",
        "limit": limite,
        "fields": "id,message,created_time,permalink_url,from",
    }

    publicaciones = []
    try:
        respuesta = requests.get(url, params=params, timeout=30)
        respuesta.raise_for_status()
        data = respuesta.json()

        for post in data.get("data", []):
            mensaje = post.get("message", "")
            if not mensaje:
                continue

            # Extraer título (primera línea o hasta 100 caracteres)
            lineas = mensaje.strip().split("\n")
            titulo = lineas[0][:100] if lineas else mensaje[:100]

            # Extraer precio
            precio_texto = ""
            for linea in lineas:
                if "USD" in linea or "CUP" in linea or "$" in linea:
                    precio_texto = linea.strip()
                    break

            precio_numero, moneda = parse_precio(precio_texto)
            permuta = detectar_permuta(mensaje)

            publicaciones.append({
                "titulo": titulo,
                "precio": precio_numero,
                "moneda": moneda,
                "municipio": "Diez de Octubre",
                "enlace": post.get("permalink_url", ""),
                "fuente": "facebook",
                "permuta": permuta,
                "publicado_en": post.get("created_time", ""),
                "mensaje_completo": mensaje[:500],  # Truncado para no guardar textos enormes
            })

    except requests.RequestException as e:
        print(f"Error buscando '{consulta}': {e}")

    return publicaciones


def obtener_grupos(access_token):
    """
    Intenta obtener los grupos del usuario autenticado.
    Solo devuelve grupos donde el usuario es miembro y la app tiene permiso.
    """
    url = f"{FACEBOOK_GRAPH_URL}/me/groups"
    params = {
        "access_token": access_token,
        "fields": "id,name,privacy",
        "limit": 50,
    }

    grupos = []
    try:
        respuesta = requests.get(url, params=params, timeout=30)
        respuesta.raise_for_status()
        data = respuesta.json()
        grupos = data.get("data", [])
    except requests.RequestException as e:
        print(f"Error obteniendo grupos: {e}")

    return grupos


def obtener_publicaciones_grupo(access_token, grupo_id, limite=50):
    """
    Obtiene publicaciones de un grupo específico (requiere ser admin o tener permisos).
    """
    url = f"{FACEBOOK_GRAPH_URL}/{grupo_id}/feed"
    params = {
        "access_token": access_token,
        "limit": limite,
        "fields": "id,message,created_time,permalink_url,from",
    }

    publicaciones = []
    try:
        respuesta = requests.get(url, params=params, timeout=30)
        respuesta.raise_for_status()
        data = respuesta.json()

        for post in data.get("data", []):
            mensaje = post.get("message", "")
            if not mensaje:
                continue

            lineas = mensaje.strip().split("\n")
            titulo = lineas[0][:100] if lineas else mensaje[:100]

            precio_texto = ""
            for linea in lineas:
                if "USD" in linea or "CUP" in linea or "$" in linea:
                    precio_texto = linea.strip()
                    break

            precio_numero, moneda = parse_precio(precio_texto)
            permuta = detectar_permuta(mensaje)

            publicaciones.append({
                "titulo": titulo,
                "precio": precio_numero,
                "moneda": moneda,
                "municipio": "Diez de Octubre",
                "enlace": post.get("permalink_url", ""),
                "fuente": "facebook",
                "permuta": permuta,
                "publicado_en": post.get("created_time", ""),
                "mensaje_completo": mensaje[:500],
            })

    except requests.RequestException as e:
        print(f"Error obteniendo publicaciones del grupo {grupo_id}: {e}")

    return publicaciones


def guardar_json(anuncios, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(anuncios, f, ensure_ascii=False, indent=2)


def main():
    print("=== Script de Facebook Graph API para mercado inmobiliario ===\n")

    # Solicitar access token
    access_token = input("Ingresa tu Access Token de Facebook Graph API: ").strip()
    if not access_token:
        print("No se proporcionó un token. Saliendo.")
        sys.exit(1)

    # Validar token
    print("\nValidando token...")
    if not validar_token(access_token):
        print("El token no es válido. Obtén uno nuevo desde el Graph API Explorer.")
        sys.exit(1)

    print("\n¿Qué deseas hacer?")
    print("1. Buscar publicaciones por palabra clave (público general)")
    print("2. Obtener publicaciones de tus grupos (requiere ser miembro/admin)")
    print("3. Ambos")

    opcion = input("\nSelecciona una opción (1-3): ").strip()

    todos_anuncios = []

    if opcion in ("1", "3"):
        print("\n--- Búsqueda por palabras clave ---")
        for consulta in BUSQUEDAS_SUGERIDAS:
            print(f"Buscando: {consulta}")
            resultados = buscar_publicaciones(access_token, consulta, limite=30)
            print(f"  Encontrados: {len(resultados)} publicaciones")
            todos_anuncios.extend(resultados)
            time.sleep(1)  # Pausa para no saturar la API

    if opcion in ("2", "3"):
        print("\n--- Obtener grupos del usuario ---")
        grupos = obtener_grupos(access_token)
        print(f"Grupos encontrados: {len(grupos)}")
        for g in grupos:
            print(f"  - {g.get('name', 'Sin nombre')} (ID: {g.get('id', 'N/A')})")

        if grupos:
            print("\nObteniendo publicaciones de cada grupo...")
            for g in grupos:
                grupo_id = g.get("id")
                grupo_nombre = g.get("name", "Sin nombre")
                print(f"  Grupo: {grupo_nombre}")
                resultados = obtener_publicaciones_grupo(access_token, grupo_id, limite=30)
                print(f"    Publicaciones: {len(resultados)}")
                todos_anuncios.extend(resultados)
                time.sleep(1)

    # Eliminar duplicados por enlace
    enlaces_vistos = set()
    anuncios_unicos = []
    for a in todos_anuncios:
        enlace = a.get("enlace", "")
        if enlace and enlace not in enlaces_vistos:
            enlaces_vistos.add(enlace)
            anuncios_unicos.append(a)

    print(f"\n=== Resultado final: {len(anuncios_unicos)} anuncios únicos ===")

    if anuncios_unicos:
        guardar_json(anuncios_unicos, OUTPUT_FILE)
        print(f"Guardado en: {OUTPUT_FILE}")

        # Resumen rápido
        con_precio = sum(1 for a in anuncios_unicos if a["precio"] is not None)
        con_permuta = sum(1 for a in anuncios_unicos if a["permuta"])
        usd = sum(1 for a in anuncios_unicos if a["moneda"] == "USD")
        cup = sum(1 for a in anuncios_unicos if a["moneda"] == "CUP")
        print(f"  Con precio: {con_precio}")
        print(f"  Con permuta: {con_permuta}")
        print(f"  Moneda USD: {usd}")
        print(f"  Moneda CUP: {cup}")
    else:
        print("No se obtuvieron anuncios.")


if __name__ == "__main__":
    main()
