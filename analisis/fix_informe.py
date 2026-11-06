with open('informe_final.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Cambio 1: Actualizar el encabezado de las entrevistas
old_header = "Además de las 122 publicaciones verificadas, el proyecto incluye **13 entrevistas a residentes de Diez de Octubre** (E-01 a E-13), grabadas en audio y conservadas en `evidencias/entrevistas_audio/`. Estas entrevistas no constituyen una muestra representativa del municipio: son relatos individuales de personas que han comprado, vendido, alquilado o permutado vivienda. Se presentan como evidencia cualitativa que ilumina los hallazgos cuantitativos, no como estadística poblacional."

nuevo_header = """Además de las 122 publicaciones verificadas, el proyecto incluye **37 entrevistas a residentes de Diez de Octubre** (E-01 a E-37), grabadas en audio y texto y conservadas en `evidencias/entrevistas_audio/`. Estas entrevistas no constituyen una muestra representativa del municipio: son relatos individuales de personas que han comprado, vendido, alquilado o permutado vivienda. Se presentan como evidencia cualitativa que ilumina los hallazgos cuantitativos, no como estadística poblacional."""

if old_header in content:
    content = content.replace(old_header, nuevo_header)
    print("OK: Encabezado de entrevistas actualizado a 37 entrevistas (E-01 a E-37)")
else:
    print("ERROR: No se encontró el encabezado de entrevistas")
    idx = content.find("Además de las 122 publicaciones verificadas")
    if idx != -1:
        print(f"Encontrado en posición {idx}:")
        print(repr(content[idx:idx+200]))

# Cambio 2: Actualizar el resumen ejecutivo - Dolarización
old_dolarizacion = """> **Dolarización:** 106 de 107 publicaciones con moneda declarada están en USD (**99.1%**), y 106 de 122 del total (**86.9%**). El único precio declarado en CUP es un alquiler. **Evidencia cualitativa:** Una compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 11); una vendedora de casa heredada cobró **en dólares, en efectivo, en la notaría** (Entrevista 17); una compradora con apoyo de familiar en el exterior pagó **en dólares, por transferencia y efectivo** (Entrevista 22). Otro comprador pagó **en dólares, en efectivo, por partes** (Entrevista 38). También hay pagos en CUP: una vendedora cobró **en efectivo, en CUP** (Entrevista 5); una inquilina pagó **en CUP, mensual, en efectivo** (Entrevista 12); una permuta se compensó **en CUP, en efectivo** (Entrevista 19); una vendedora cobró **una parte en dólares y otra en CUP, en efectivo** (Entrevista 41). Esto valida la dolarización medida (86.9% del universo en USD) y al mismo tiempo muestra que el CUP no ha desaparecido del todo."""

nueva_dolarizacion = """> **Dolarización:** 106 de 107 publicaciones con moneda declarada están en USD (**99.1%**), y 106 de 122 del total (**86.9%**). El único precio declarado en CUP es un alquiler. **Evidencia cualitativa:** Una compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 11); una vendedora de casa heredada cobró **en dólares, en efectivo, en la notaría** (Entrevista 17); una compradora con apoyo de familiar en el exterior pagó **en dólares, por transferencia y efectivo** (Entrevista 22). Otro comprador pagó **en dólares, en efectivo, por partes** (Entrevista 38). Otra compradora pagó **en dólares, en efectivo, todo de una vez** (Entrevista 37). También hay pagos en CUP: una vendedora cobró **en efectivo, en CUP** (Entrevista 5); una inquilina pagó **en CUP, mensual, en efectivo** (Entrevista 12); una permuta se compensó **en CUP, en efectivo** (Entrevista 19); una vendedora cobró **una parte en dólares y otra en CUP, en efectivo** (Entrevista 37). Esto valida la dolarización medida (86.9% del universo en USD) y al mismo tiempo muestra que el CUP no ha desaparecido del todo."""

if old_dolarizacion in content:
    content = content.replace(old_dolarizacion, nueva_dolarizacion)
    print("OK: Dolarización actualizada correctamente")
else:
    print("ERROR: No se encontró el texto de Dolarización")
    idx = content.find("**Dolarización:**")
    if idx != -1:
        print(f"Encontrado en posición {idx}:")
        print(repr(content[idx:idx+200]))

with open('informe_final.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cambios aplicados correctamente")
EOF