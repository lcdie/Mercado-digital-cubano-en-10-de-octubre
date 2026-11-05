# Documentación de datos

Este documento explica la procedencia, contenido y estado de los datos del proyecto, así como la relación entre los archivos de `datos/`.

## Estructura de carpetas

```
datos/
├── brutos/                 # Capturas originales (no versionadas del todo)
│   ├── facebook_crudos_20261104.json      # Captura de Facebook (43 publicaciones)
│   ├── revolico_crudos.json               # Captura base de Revolico
│   ├── revolico_crudos_actualizados.json
│   ├── revolico_crudos_con_fechas.json
│   ├── revolico_crudos_limpio.json
│   ├── revolico_crudos_limpio_final.json
│   ├── revolico_progreso_actualizacion.json
│   └── revolico_ubicaciones_pagina.json
├── geo/                    # Recursos geoespaciales
│   ├── lha.geojson         # Polígono municipal de La Habana (DPA 23.09, 11 vértices)
│   └── geocoding_lha.json  # Caché de geocodificación Nominatim
└── limpios/                # Bases limpias, confirmados y descartados
    ├── anuncios_activos.txt
    ├── anuncios_eliminados_por_filtro_final.json
    ├── anuncios_eliminados_por_sospecha.json
    ├── anuncios_inactivos.txt
    ├── anuncios_limpios_listado.txt
    ├── datos_sospechosos_o_mal_filtrados.json
    ├── datos_unificados_facebook_revolico.json     # Base unificada (176 registros)
    ├── descartados_diez_octubre.json               # 55 descartes íntegros con motivo
    ├── descartados_diez_octubre.csv                # Versión tabular de los descartes
    ├── facebook_confirmados_diez_octubre.json      # 39 confirmados de Facebook
    ├── facebook_eliminados_por_filtro.json
    ├── facebook_publicaciones_limpias.json
    ├── nuevos_anuncios.txt
    ├── reporte_actualizacion_anuncios.txt
    ├── reporte_analisis_precios_rango_p10_p90.txt
    ├── reporte_limpieza_fechas.txt
    ├── reporte_tecnico_datos_limpios.txt
    ├── revolico_confirmados_diez_octubre.json      # 83 confirmados de Revolico
    ├── unificado_confirmados_diez_octubre.json     # Base final: 122 confirmados
    ├── verificacion_municipal.csv
    ├── verificacion_municipal_facebook.json
    ├── verificacion_municipal_revolico.json
    └── verificacion_municipal_unificado.json
```

## Procedencia de los datos

| Fuente | Tipo | Cantidad confirmada | Corte / Captura | Uso |
|---|---|---|---|---|
| Revolico | Anuncios clasificados | 83 | 2026-10-31 | Título, precio, enlace, fecha de verificación, zona |
| Facebook | Grupos y páginas de compraventa | 39 | 2026-11-04 | Precio y descripción parcial |
| ONEI | Anuario Estadístico de Cuba | Contexto | — | Población, vivienda y tenencia del municipio |
| OpenStreetMap / Nominatim | Geocodificación de topónimos | — | — | Coordenadas para comprobación punto-en-polígono |
| GeoJSON municipal | Polígono DPA 23.09 | — | — | Comprobación de pertenencia al municipio |

## Estado de los datos

- **Base canónica:** `datos/limpios/unificado_confirmados_diez_octubre.json` (122 publicaciones confirmadas dentro de Diez de Octubre).
- **Base histórica:** `datos/brutos/revolico_crudos_limpio_final.json` (134 anuncios de Revolico etiquetados como Diez de Octubre, no verificada). Se conserva solo como referencia histórica; no es comparable con el informe final.
- **Descartes:** `datos/limpios/descartados_diez_octubre.json` y `.csv` (55 registros no incluidos: 46 `NO`, 8 `INDETERMINADO`, 1 fuera del universo). Se conservan íntegros con motivo, `registro_original` y `registro_unificado` exacto. No se elimina información.

## Relación entre archivos

1. `datos/brutos/` → limpieza y normalización → `datos/limpios/datos_unificados_facebook_revolico.json` (176 registros)
2. `datos/limpios/datos_unificados_facebook_revolico.json` → verificación municipal → `unificado_confirmados_diez_octubre.json` (122) + `descartados_diez_octubre.json` (55)
3. `datos/limpios/unificado_confirmados_diez_octubre.json` → informe A-F → `analisis/informe_final.md` y `.pdf`
4. `datos/limpios/unificado_confirmados_diez_octubre.json` → gráficos → `graficos/grafico_1_*.png` a `grafico_5_*.png`

## Qué datos alimentan cada análisis

| Análisis | Fuente de datos |
|---|---|
| Informe final A-F (30 preguntas) | `datos/limpios/unificado_confirmados_diez_octubre.json` |
| Gráficos de exposición | `datos/limpios/unificado_confirmados_diez_octubre.json` |
| Cifras de control | `datos/limpios/unificado_confirmados_diez_octubre.json` + `datos/limpios/descartados_diez_octubre.json` |
| Pruebas de contrato | Ambos archivos anteriores |

## Qué datos pueden regenerarse

- `datos/limpios/unificado_confirmados_diez_octubre.json`: regenerar con `scripts/verificar_municipio_publicaciones.py`
- `datos/limpios/descartados_diez_octubre.json`: regenerar con `scripts/verificar_municipio_publicaciones.py`
- `analisis/informe_final.md`: regenerar con `scripts/analisis_final_30_preguntas.py`
- `graficos/grafico_*.png`: regenerar con `graficos/generar_graficas.py`

## Tratamiento ético de datos personales

- **No se publican teléfonos ni nombres** de vendedores de Facebook. Los campos de contacto se conservan vacíos o enmascarados cuando proceda.
- **Las capturas de pantalla de Facebook** (si se incluyen en la exposición) deben tener datos personales difuminados o recortados.
- **Las entrevistas de audio** (carpeta `evidencias/entrevistas_audio/`) deben usar códigos anónimos (ej. `E-01`, `E-02`) y no incluir nombres, direcciones o teléfonos identificables.
- **No se publican metadatos sensibles** (GPS, fechas de contacto precisas) en ningún archivo del repositorio.

## Convenciones de datos ausentes

- Celdas vacías, `null`, `""` o `"No especificado"` significan que el dato **no existe** en la fuente o no se pudo extraer.
- **Nunca se imputan** valores ausentes con ceros, medias ni valores plausibles.
- Las ausencias se reportan como hallazgo de opacidad, no como defecto.
