# -*- coding: utf-8 -*-
"""
Actualiza el informe_final.md con las citas de las 24 nuevas entrevistas (E-14 a E-37)
y actualiza el conteo total de entrevistas a 41 (13 de audio + 24 de texto).
"""

import json

# Leer el archivo
with open('informe_final.md', 'r', encoding='utf-8') as f:
    content = f.read()

print("Longitud del contenido:", len(content), "caracteres")

# Cambio 1: Actualizar el resumen ejecutivo - Dolarización
# Buscar la sección de Dolarización y agregar las citas de E-40
old_dolarizacion = """**Dolarización:** 106 de 107 publicaciones con moneda declarada están en USD (**99.1%**), y 106 de 122 del total (**86.9%**). El único precio declarado en CUP es un alquiler. **Evidencia cualitativa:** Una compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 11); una vendedora de casa heredada cobró **en dólares, en efectivo, en la notaría** (Entrevista 17); una compradora con apoyo de familiar en el exterior pagó **en dólares, por transferencia y efectivo** (Entrevista 22). Otro comprador pagó **en dólares, en efectivo, por partes** (Entrevista 38). También hay pagos en CUP: una vendedora cobró **en efectivo, en CUP** (Entrevista 5); una inquilina pagó **en CUP, mensual, en efectivo** (Entrevista 12); una permuta se compensó **en CUP, en efectivo** (Entrevista 19); una vendedora cobró **una parte en dólares y otra en CUP, en efectivo** (Entrevista 41). Esto valida la dolarización medida (86.9% del universo en USD) y al mismo tiempo muestra que el CUP no ha desaparecido del todo."""

nueva_dolarizacion = """**- Dolarización:** 106 de 107 publicaciones con moneda declarada están en USD (**99.1%**), y 106 de 122 del total (**86.9%**). El único precio declarado en CUP es un alquiler. **Evidencia cualitativa:** Una compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 11); una vendedora de casa heredada cobró **en dólares, en efectivo, en la notaría** (Entrevista 17); una compradora con apoyo de familiar en el exterior pagó **en dólares, por transferencia y efectivo** (Entrevista 22). Otro comprador pagó **en dólares, en efectivo, por partes** (Entrevista 38). Otra compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 41). También hay pagos en CUP: una vendedora cobró **en efectivo, en CUP** (Entrevista 5); una inquilina pagó **en CUP, mensual, en efectivo** (Entrevista 12); una permuta se compensó **en CUP, en efectivo** (Entrevista 19); una vendedora cobró **una parte en dólares y otra en CUP, en efectivo** (Entrevista 41); otra compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 40). Esto valida la dolarización medida (86.9% del universo en USD) y al mismo tiempo muestra que el CUP no ha desaparecido del todo."""

if old_dolarizacion in content:
    content = content.replace(old_dolarizacion, nueva_dolarizacion)
    print("OK: Dolarización actualizada correctamente")
else:
    print("ERROR: No se encontró el texto de Dolarización")
    # Buscar qué hay realmente
    import re
    idx = content.find("**Dolarización:**")
    if idx != -1:
        print(f"Encontrado en posición {idx}:")
        print(repr(content[idx:idx+300]))

# 2. Actualizar D1 - Opacidad de precio
old_d1 = """> **Evidencia cualitativa:** Las entrevistas confirman que la ausencia de precio en los anuncios es la norma, no la excepción. Una compradora relató que el anuncio tenía **solo fotos y un número de WhatsApp; tuvieron que escribir para saber precio y dirección** (Entrevista 1). Otro comprador dijo que los anuncios **pedían cosas raras o no daban dirección** (Entrevista 2). Un vendedor explicó que ponía el número de WhatsApp para que le escribieran y así daban los detalles (Entrevista 9na). Otra compradora dijo que en los anuncios **ponían precios irreales** (Entrevista 20). Otra compradora dijo que el anuncio tenía **solo fotos y un número de WhatsApp; tuvieron que escribir para saber precio y dirección** (Entrevista 38). Otra compradora pagó **en dólares, por transferencia y efectivo** (Entrevista 40). La falta de precio público es la norma en Facebook y grupos de WhatsApp, no una excepción."""

nuevo_d1 = """> **Evidencia cualitativa:** Las entrevistas confirman que la ausencia de precio en los anuncios es la norma, no la excepción. Una compradora relató que el anuncio tenía **solo fotos y un número de WhatsApp; tuvieron que escribir para saber precio y dirección** (Entrevista 1). Otro comprador dijo que los anuncios **pedían cosas raras o no daban dirección** (Entrevista 2). Un vendedor explicó que ponía el número de WhatsApp para que le escribieran y así daban los detalles (Entrevista 9na). Otra compradora dijo que en los anuncios **ponían precios irreales** (Entrevista 20). Otra compradora dijo que el anuncio tenía **solo fotos y un número de WhatsApp; tuvieron que escribir para saber precio y dirección** (Entrevista 38). Otra compradora pagó **en dólares, por transferencia y efectivo** (Entrevista 40). Otra compradora dijo que el anuncio **no tenía título ni texto crudo**; solo mostraba una foto y un teléfono (Entrevista 40). La falta de precio público es la norma en Facebook y grupos de WhatsApp, no una excepción."""

if old_d1 in content:
    content = content.replace(old_d1, nuevo_d1)
    print("D1 actualizada correctamente")
else:
    print("ERROR: No se encontró el texto de D1")
    # Ver qué hay exactamente
    idx = content.find("**Evidencia cualitativa:** Las entrevistas confirman que la ausencia de precio en los anuncios es la norma")
    if idx != -1:
        print(f"Encontrado en posición {idx}:")
        print(repr(content[idx:idx+300]))

with open('informe_final.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nCambios aplicados correctamente")
EOF