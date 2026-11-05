# Catálogo de visualizaciones

Este directorio contiene las 5 gráficas de exposición generadas a partir de `datos/limpios/unificado_confirmados_diez_octubre.json` (122 publicaciones confirmadas dentro de Diez de Octubre).

Cada gráfica responde a una pregunta de investigación específica del informe A-F y puede usarse en la presentación oral.

## Índice de figuras

| Figura | Archivo | Pregunta de investigación | Descripción | Código generador |
|---|---|---|---|---|
| 1 | `grafico_1_precios_venta_usd.png` | A2 — Mediana y rango P10–P90 del precio de compra | Histograma de 43 ventas en USD con línea de media ($26.023) y mediana ($20.000). Rango P10–P90: $6.200–$60.000. | `graficos/generar_graficas.py` |
| 2 | `grafico_2_oferta_por_zona.png` | B1 — Zonas con mayor oferta | Barras horizontales con las 8 zonas que más anuncios concentran. Santos Suárez, Lawton, La Víbora y El Sevillano agrupan el 75.8% de las publicaciones con zona. | `graficos/generar_graficas.py` |
| 3 | `grafico_3_media_mediana_zona.png` | B3 — Zona con la mediana más alta | Comparación media vs mediana por zona (n ≥ 5). El Sevillano tiene la mediana más alta ($36.000, n=10); La Víbora tiene la media más alta ($49.591, n=11) por valores extremos. | `graficos/generar_graficas.py` |
| 4 | `grafico_4_moneda.png` | C1 — Proporción de anuncios en USD | Gráfico circular: 106 de 107 anuncios con moneda declarada están en USD (99.1%); 1 en CUP; 15 sin precio (12.3% del total). | `graficos/generar_graficas.py` |
| 5 | `grafico_5_opacidad.png` | D3 — Anuncios sin precio ni zona | Gráfico circular: 67.2% tiene precio y zona; 4.9% no tiene ninguno de los dos; 25.4% sin zona; 12.3% sin precio. | `graficos/generar_graficas.py` |

## Cómo regenerar todas las figuras

```bash
python3 graficos/generar_graficas.py
```

Requiere: `matplotlib` (ya incluido en `requirements.txt`).

## Notas de uso

- Los precios son precios de oferta, no de transacción.
- Las zonas se asignaron usando la regla de título primero y geocodificación de topónimos; no se infiere una zona que el anuncio no mencione.
- Las subgrupos con n < 10 se presentan como evidencia descriptiva, no como conclusión firme.
