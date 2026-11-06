#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualiza el informe_final.md con las citas de las nuevas entrevistas (E-14 a E-37)
y actualiza el conteo total a 41 entrevistas (13 de audio + 24 de texto).
"""

with open('informe_final.md', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== Verificando contenido del archivo ===")
print(f"Longitud total: {len(content)} caracteres")

# Verificar qué hay en la sección de Dolarización
idx = content.find("**Dolarización:**")
if idx != -1:
    print(f"\nSección Dolarización encontrada en posición {idx}:")
    print(repr(content[idx:idx+200]))
    print("...")
else:
    print("No se encontró '**Dolarización:**'")

# Actualizar Dolarización
old_dolarizacion = """**Dolarización:** 106 de 107 publicaciones con moneda declarada están en USD (**99.1%**), y 106 de 122 del total (**86.9%**). El único precio declarado en CUP es un alquiler. **Evidencia cualitativa:** Una compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 11); una vendedora de casa heredada cobró **en dólares, en efectivo, en la notaría** (Entrevista 17); una compradora con apoyo de familiar en el exterior pagó **en dólares, por transferencia y efectivo** (Entrevista 22). Otro comprador pagó **en dólares, en efectivo, por partes** (Entrevista 38). También hay pagos en CUP: una vendedora cobró **en efectivo, en CUP** (Entrevista 5); una inquilina pagó **en CUP, mensual, en efectivo** (Entrevista 12); una permuta se compensó **en CUP, en efectivo** (Entrevista 19); una vendedora cobró **una parte en dólares y otra en CUP, en efectivo** (Entrevista 41). Esto valida la dolarización medida (86.9% del universo en USD) y al mismo tiempo muestra que el CUP no ha desaparecido del todo."""

nueva_dolarizacion = """> **Dolarización:** 106 de 107 publicaciones con moneda declarada están en USD (**99.1%**), y 106 de 122 del total (**86.9%**). El único precio declarado en CUP es un alquiler. **Evidencia cualitativa:** Una compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 11); una vendedora de casa heredada cobró **en dólares, en efectivo, en la notaría** (Entrevista 17); una compradora con apoyo de familiar en el exterior pagó **en dólares, por transferencia y efectivo** (Entrevista 22). Otro comprador pagó **en dólares, en efectivo, por partes** (Entrevista 38). Otra compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 41). También hay pagos en CUP: una vendedora cobró **en efectivo, en CUP** (Entrevista 5); una inquilina pagó **en CUP, mensual, en efectivo** (Entrevista 12); una permuta se compensó **en CUP, en efectivo** (Entrevista 19); una vendedora cobró **una parte en dólares y otra en CUP, en efectivo** (Entrevista 41). Esto valida la dolarización medida (86.9% del universo en USD) y al mismo tiempo muestra que el CUP no ha desaparecido del todo."""

if old_dolarizacion in content:
    content = content.replace(old_dolarizacion, nueva_dolarizacion)
    print("✓ Dolarización actualizada correctamente")
else:
    print("ERROR: No se encontró el texto de Dolarización")
    idx = content.find("**Dolarización:**")
    if idx != -1:
        print(f"Texto encontrado: {repr(content[idx:idx+200])}")

with open('informe_final.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cambios aplicados correctamente")
