# Diccionario de datos — Mercado inmobiliario digital en Diez de Octubre

**Proyecto:** Ciencia de Datos, Universidad de La Habana (MATCOM)  
**Tema:** opacidad, dolarización, desigualdad territorial e informalidad del mercado inmobiliario digital de Diez de Octubre  
**Universo:** 122 publicaciones confirmadas dentro del municipio (83 de Revolico + 39 de Facebook)  
**Corte:** Revolico 2026-10-31; Facebook 2026-11-04  
**Base:** `datos/limpios/unificado_confirmados_diez_octubre.json`  
**Descartes:** `datos/limpios/descartados_diez_octubre.json` y `.csv` (55 registros íntegros con motivo)

---

## 0. Convenciones generales

| Convención | Significado |
|---|---|
| Celda vacía / `null` / `""` | El dato **no existe** en la fuente o no se pudo extraer. **Nunca** se rellena con ceros, medias ni valores plausibles. |
| `"No especificado"` | El campo existe pero el anunciante no lo declara. Se conserva como ausencia, no como valor. |
| `fecha_verificacion` | Momento de captura del anuncio (Revolico no expone fecha de publicación). No es fecha de venta ni de publicación original. |
| `n` | Número de publicaciones que apoyan el resultado; siempre se indica junto al estadístico. |
| Nivel de evidencia | ✅ sólida (n ≥ 30 o censo del subgrupo), 🟡 descriptiva (n = 5–29), 🔴 no estimable (la ausencia es el hallazgo). |

---

## 1. Esquema de la base de confirmados

Cada registro de `unificado_confirmados_diez_octubre.json` tiene esta estructura:

| Campo | Tipo | n / 122 | Descripción |
|---|---|---|---|
| `id_unico` | texto | 122 | Identificador único (`revolico-<id>` o `facebook-<n>`). |
| `fuente` | texto | 122 | `revolico` o `facebook`. |
| `verificacion_municipal` | objeto | 122 | Resultado de la verificación contra el municipio (ver tabla 2). |
| `publicacion` | objeto | 122 | Metadatos de publicación (ver tabla 3). |
| `precio` | objeto | 106 | Precio declarado (ver tabla 4). |
| `operacion` | texto | 53 | `Venta`, `Alquiler` o `Sin clasificar`. |
| `detalles_propiedad` | objeto | 122 | Tipo, ubicación y zona declarada (ver tabla 5). |
| `contacto` | objeto | 29 | Teléfono y método de contacto (solo Revolico). |
| `equipamiento_incluido` | lista | 122 | Equipamiento declarado (vacío si no consta). |
| `servicios_y_caracteristicas` | lista | 122 | Servicios declarados (vacío si no consta). |
| `posibles_duplicados` | lista | 2 | IDs del par duplicado entre fuentes. |
| `extras` | objeto | 122 | Campos adicionales de la fuente original. |
| `fecha_verificacion` | texto | 100 | Fecha de captura del anuncio (corte Revolico). |

### 1.1 `verificacion_municipal`

| Subcampo | Tipo | Descripción |
|---|---|---|
| `resultado` | texto | `SÍ`, `NO`, `CONTRADICTORIO` o `INDETERMINADO`. |
| `confianza` | texto | `alta` o `media`. |
| `evidencia_principal` | texto | `título`, `ficha` o `texto`. |
| `motivo` | texto | Motivo de clasificación en lenguaje natural. |
| `ficha` | objeto | Estado de la ficha de Revolico (`dentro`, `fuera`, `sin ubicación`). |

### 1.2 `publicacion`

| Subcampo | Tipo | n / 122 | Descripción |
|---|---|---|---|
| `titulo` | texto | 83 | Título del anuncio (evidencia principal para la verificación municipal). |
| `enlace` | texto | 83 | URL del anuncio; solo Revolico. |
| `fecha` | texto | 100 | Fecha declarada o relativa (Facebook) o fecha de captura (Revolico). |
| `grupo` | texto | 39 | Grupo o canal de Facebook (vacío en Revolico). |
| `autor` | texto | 122 | Autor o plataforma del anuncio. |

### 1.3 `precio`

| Subcampo | Tipo | n / 122 | Descripción |
|---|---|---|---|
| `monto` | numérico | 106 | Monto declarado en la moneda del anuncio. |
| `moneda` | texto | 107 | `USD` o `CUP`. |
| `negociable` | booleano | 106 | Indica si el precio es negociable. |
| `nota` | texto | 106 | Nota de precio (p. ej. "Precio fijo"). |
| `monto_actual` | numérico | — | Monto tras rebaja (caso Facebook: 15,000 USD). |

### 1.4 `detalles_propiedad`

| Subcampo | Tipo | n / 122 | Descripción |
|---|---|---|---|
| `tipo` | texto | 122 | `Casa`, `Apartamento`, `Inmueble`, `Cuarto`, `Local`, `Terreno`. |
| `tipo_original` | texto | 122 | Valor original antes de normalizar. |
| `ubicacion` | texto | 122 | Ubicación declarada por el anunciante. |
| `zona` | texto | 84 | Zona declarada en la ficha; si está vacía, se recupera del texto. |
| `distribucion` | lista | 122 | Distribución declarada (vacía si no consta). |

Cobertura analítica de zona: 91/122 (84 en ficha + 7 recuperadas del título o texto; ninguna asignada sin mención textual).

---

## 2. Esquema de los descartes

Cada registro de `descartados_diez_octubre.json` conserva:

| Campo | Tipo | Descripción |
|---|---|---|
| `id_unico` | texto | Identificador del anuncio descartado. |
| `resultado` | texto | `NO` (47) o `INDETERMINADO` (8). |
| `confianza` | texto | `alta` o `media`. |
| `evidencia_principal` | texto | `título`, `ficha` o `texto`. |
| `motivo_descarte` | texto | Motivo del descarte en lenguaje natural. |
| `en_universo_unificado` | booleano | `true` si el anuncio estaba en las 176 unificadas. |
| `registro_original` | objeto | Registro tal como entró al pipeline de verificación. |
| `registro_unificado` | objeto | Registro exacto en la base unificada (exacto, sin alteraciones). |

- 54 descartados del universo conservan `registro_unificado` exacto.
- `facebook-27` estaba fuera de la base unificada (publicación previa rechazada), por eso `registro_unificado` es `null`.
- Ningún registro se elimina ni se modifica: se conserva íntegro con su motivo.

---

## 3. Cobertura por campo

| Campo | Cobertura | n | Lectura |
|---|---:|---:|---|
| Precio USD | 86.9% | 106/122 | Base principal de los análisis de precio. |
| Precio CUP | 0.8% | 1/122 | No se convierte a USD. |
| Sin precio | 12.3% | 15/122 | Se conserva y se reporta como opacidad. |
| Zona identificada | 74.6% | 91/122 | 84 en ficha + 7 recuperadas del texto. |
| Operación declarada | 43.4% | 53/122 | 50 ventas y 3 alquileres; 69 sin clasificar. |
| Habitaciones | 0.0% | 0/122 | No hay campo homogéneo; no se estima. |
| Baños | 0.0% | 0/122 | No hay campo homogéneo; no se estima. |
| Superficie (m²) | 4.9% | 6/122 | Solo Facebook (`detalles_propiedad.area_m2`). |
| Teléfono | 23.8% | 29/122 | Contacto declarado; no se usa para inferir intermediación. |
| Enlace | 68.0% | 83/122 | Todos de Revolico. |

---

## 4. Estadísticos clave del informe

| Indicador | Valor | n |
|---|---|---:|
| Media de ventas USD | $26,023.26 | 43 |
| Mediana de ventas USD | $20,000.00 | 43 |
| P10 – P90 ventas USD | $6,200.00 – $60,000.00 | 43 |
| Zona media más alta (n ≥ 10) | La Víbora, $49,590.91 | 11 |
| Zona mediana más alta (n ≥ 10) | El Sevillano, $36,000.00 | 10 |
| Zona media más alta (n ≥ 5) | El Mónaco, $57,666.67 | 6 |
| Zona mediana más alta (n ≥ 5) | El Sevillano, $36,000.00 | 10 |
| Cruce precio y zona | 82 | 67.2% |
| Sin precio ni zona | 6 | 4.9% |
| Par duplicado entre fuentes | 1 | `facebook-35` / `revolico-58326838` |
| n efectivo tras eliminar el duplicado | 121 | — |

---

## 5. Notas de calidad

- No se imputan precios, zonas, operaciones, habitaciones, baños ni superficies ausentes.
- Las zonas recuperadas del texto solo se asignan cuando el anuncio menciona explícitamente el barrio o reparto.
- Los precios son de oferta, no de transacción.
- El único precio en CUP no se convierte a USD por falta de un tipo de cambio defendible para el corte.
- Los subgrupos con n < 10 se presentan como evidencia descriptiva, no como conclusión firme.
