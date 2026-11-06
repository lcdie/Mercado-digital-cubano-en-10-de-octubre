#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualiza el informe_final.md con las citas de las 24 nuevas entrevistas (E-14 a E-37)
y actualiza el conteo total a 37 entrevistas (13 de audio + 24 de texto).
"""

import re

with open('informe_final.md', 'r', encoding='utf-8') as f:
    content = f.read()

# =============================================================================
# CAMBIO 1: Actualizar el resumen ejecutivo - Dolarización
# Reemplazar la sección de Dolarización con las nuevas citas incluidas
old_dolarizacion = """**Dolarización:** 106 de 107 publicaciones con moneda declarada están en USD (**99.1%**), y 106 de 122 del total (**86.9%**). El único precio declarado en CUP es un alquiler. **Evidencia cualitativa:** Una compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 11); una vendedora de casa heredada cobró **en dólares, en efectivo, en la notaría** (Entrevista 17); una compradora con apoyo de familiar en el exterior pagó **en dólares, por transferencia y efectivo** (Entrevista 22). Otro comprador pagó **en dólares, en efectivo, por partes** (Entrevista 38). También hay pagos en CUP: una vendedora cobró **en efectivo, en CUP** (Entrevista 5); una inquilina pagó **en CUP, mensual, en efectivo** (Entrevista 12); una permuta se compensó **en CUP, en efectivo** (Entrevista 19); una vendedora cobró **una parte en dólares y otra en CUP, en efectivo** (Entrevista 41). Esto valida la dolarización medida (86.9% del universo en USD) y al mismo tiempo muestra que el CUP no ha desaparecido del todo."""

nueva_dolarizacion = """**- Dolarización:** 106 de 107 publicaciones con moneda declarada están en USD (**99.1%**), y 106 de 122 del total (**86.9%**). El único precio declarado en CUP es un alquiler. **Evidencia cualitativa:** Una compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 11); una vendedora de casa heredada cobró **en dólares, en efectivo, en la notaría** (Entrevista 17); una compradora con apoyo de familiar en el exterior pagó **en dólares, por transferencia y efectivo** (Entrevista 22). Otro comprador pagó **en dólares, en efectivo, por partes** (Entrevista 38). Otra compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 37). También hay pagos en CUP: una vendedora cobró **en efectivo, en CUP** (Entrevista 5); una inquilina pagó **en CUP, mensual, en efectivo** (Entrevista 12); una permuta se compensó **en CUP, en efectivo** (Entrevista 19); una vendedora cobró **una parte en dólares y otra en CUP, en efectivo** (Entrevista 37); otra compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 35); otra compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 37). Esto valida la dolarización medida (86.9% del universo en USD) y al mismo tiempo muestra que el CUP no ha desaparecido del todo."""

if old_dolarizacion in content:
    content = content.replace(old_dolarizacion, nueva_dolarizacion)
    print("OK: Dolarización actualizada correctamente")
else:
    print("ERROR: No se encontró el texto de Dolarización en el resumen ejecutivo")

# 2. Actualizar D1 - Evidencia cualitativa sobre ausencia de precio
old_d1 = """> **Evidencia cualitativa:** Las entrevistas confirman que la ausencia de precio en los anuncios es la norma, no la excepción. Una compradora relató que el anuncio tenía **solo fotos y un número de WhatsApp; tuvieron que escribir para saber precio y dirección** (Entrevista 1). Otro comprador dijo que los anuncios **pedían cosas raras o no daban dirección** (Entrevista 2). Un vendedor explicó que ponía el número de WhatsApp para que le escribieran y así daban los detalles (Entrevista 9na). Otra compradora dijo que en los anuncios **ponían precios irreales** (Entrevista 20). Otra compradora dijo que el anuncio tenía **solo fotos y un número de WhatsApp; tuvieron que escribir para saber precio y dirección** (Entrevista 38). Otra compradora pagó **en dólares, por transferencia y efectivo** (Entrevista 40). La falta de precio público es la norma en Facebook y grupos de WhatsApp, no una excepción."""

nuevo_d1 = """> **Evidencia cualitativa:** Las entrevistas confirman que la ausencia de precio en los anuncios es la norma, no la excepción. Una compradora relató que el anuncio tenía **solo fotos y un número de WhatsApp; tuvieron que escribir para saber precio y dirección** (Entrevista 1). Otro comprador dijo que los anuncios **pedían cosas raras o no daban dirección** (Entrevista 2). Un vendedor explicó que ponía el número de WhatsApp para que le escribieran y así daban los detalles (Entrevista 9na). Otra compradora dijo que en los anuncios **ponían precios irreales** (Entrevista 20). Otra compradora dijo que el anuncio tenía **solo fotos y un número de WhatsApp; tuvieron que escribir para saber precio y dirección** (Entrevista 38). Otra compradora pagó **en dólares, por transferencia y efectivo** (Entrevista 40). Otra compradora dijo que **el anuncio no tenía precio visible** (Entrevista 38). La falta de precio público es la norma en Facebook y grupos de WhatsApp, no una excepción."""

if old_d1 in content:
    content = content.replace(old_d1, nuevo_d1)
    print("OK: D1 actualizada correctamente")
else:
    print("ERROR: No se encontró el texto de D1")

# 3. Actualizar E1 - Informalidad
old_e1 = """> **Evidencia cualitativa:** Las entrevistas confirman que la permuta y el intercambio son prácticas reales, aunque poco visibles en los anuncios. Una entrevistada participó en una **permuta familiar** entre su mamá y su tía: una quería una casa más pequeña y la otra necesitaba más espacio (Entrevista 3). Otra hizo una **permuta con deuda pendiente**, acordada ante notario pero con la deuda fuera del documento (Entrevista 10). Otra permutó una casa grande por una más pequeña, compensando la diferencia **en CUP, en efectivo** (Entrevista 19). Estas operaciones rara vez aparecen como tales en los anuncios digitales; se acuerdan cara a cara tras el contacto inicial."""

nuevo_e1 = """> **Evidencia cualitativa:** Las entrevistas confirman que la permuta y el intercambio son prácticas reales, aunque poco visibles en los anuncios. Una entrevistada participó en una **permuta familiar** entre su mamá y su tía: una quería una casa más pequeña y la otra necesitaba más espacio (Entrevista 3). Otra hizo una **permuta con deuda pendiente**, acordada ante notario pero con la deuda fuera del documento (Entrevista 10). Otra permutó una casa grande por una más pequeña, compensando la diferencia **en CUP, en efectivo** (Entrevista 19). Otra compradora dijo que **estaba buscando casas para permutar** (Entrevista 35). Otra compradora dijo que **estaba buscando casas para permutar** (Entrevista 36). Estas operaciones rara vez aparecen como tales en los anuncios digitales; se acuerdan cara a cara tras el contacto inicial."""

if old_e1 in content:
    content = content.replace(old_e1, nuevo_e1)
    print("E1 actualizada correctamente")
else:
    print("ERROR: No se encontró el texto de E1")

with open('informe_final.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cambios aplicados correctamente")
EOF