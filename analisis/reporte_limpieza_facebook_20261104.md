# Reporte de limpieza e unificación de Facebook

**Fecha:** 04/11/2026  
**Fuente Facebook:** `datos/brutos/facebook_crudos_20261104.json`  
**Base Revolico:** `datos/brutos/revolico_crudos_limpio_final.json`  
**Salida unificada:** `datos/limpios/datos_unificados_facebook_revolico.json`

## 1. Archivo de entrada

La captura nueva contiene **43 publicaciones** de Facebook, con IDs `1–43` únicos. Respecto a la captura anterior de 37 publicaciones:

- Se conservan las 37 anteriores.
- 36 son idénticas campo por campo.
- 1 fue corregida: en el id 6, `distribucion_general` pasó de nivel superior a `detalles_propiedad`.
- Se añaden 6 publicaciones nuevas: ids 38–43.
- No se elimina ninguna publicación anterior.

## 2. Criterios de limpieza

Se aplicaron los mismos criterios que a Revolico:

1. **Municipio:** se rechaza la publicación si su grupo, título, autor o ubicación menciona un municipio, reparto o localidad fuera de Diez de Octubre. Se reutiliza la lista de patrones de `scripts/limpieza_final_municipio.py`.
2. **Precio mínimo:** se rechaza un precio declarado inferior a 1,000 USD o 24,000 CUP. Las publicaciones sin precio se conservan porque la ausencia es un hallazgo.
3. **Normalización:** tipo, zona, operación, distribución, detalles de estructura y contacto se llevan a formas homogéneas.

## 3. Resultado del filtro

| Etapa | Registros |
|---|---:|
| Publicaciones capturadas | 43 |
| Conservadas | **42** |
| Rechazadas | **1** |
| Base unificada final (Revolico + Facebook) | **176** |

**Rechazo:**

| ID | Motivo | Patrón detectado | Ubicación |
|---:|---|---|---|
| 27 | Municipio distinto a Diez de Octubre | `santa amalia` | Santa Amalia, a 3 cuadras de la Calzada de 10 de Octubre |

No hubo rechazos por precio: el mínimo declarado es 2,000 USD.

## 4. Composición de la base limpia de Facebook

| Indicador | Valor |
|---|---:|
| Publicaciones | 42 |
| Con monto de precio | 33 |
| Sin precio | 9 |
| Con moneda USD declarada | 34 |
| Con moneda CUP | 0 |
| Precios menores de 1,000 USD | 0 |

**Precio en USD (n = 33):** mínimo $2,000; P10 $4,700; mediana $22,000; media $32,984.85; P90 $69,000; máximo $150,000.

**Tipos normalizados:**

| Tipo | n | % |
|---|---:|---:|
| Casa | 27 | 64.3% |
| Apartamento | 11 | 26.2% |
| Inmueble | 3 | 7.1% |
| Cuarto | 1 | 2.4% |

**Zonas:**

| Zona | n |
|---|---:|
| No especificado | 12 |
| Lawton | 8 |
| Santos Suárez | 6 |
| El Sevillano | 4 |
| Santa Catalina | 4 |
| Luyano | 3 |
| La Víbora | 2 |
| El Mónaco | 1 |
| Vista Alegre | 1 |
| Calzada 10 de Octubre | 1 |

**Operación inferida:**

| Operación | n |
|---|---:|
| Sin clasificar | 23 |
| Venta | 19 |
| Alquiler | 0 |

**Evidencia municipal:**

| Evidencia | n |
|---|---:|
| Explícita («10 de Octubre») | 23 |
| Por reparto conocido | 15 |
| Ambigua | 2 |
| Sin ubicación | 2 |

Las dos ubicaciones ambiguas son los ids 1 («Plaza Roja») y 16 («San Leopoldo»). Las dos sin ubicación son los ids 8 y 17.

## 5. Campos ausentes y calidad

| Campo | Situación |
|---|---|
| Fecha | 17 de 42 la declaran; 25 no. Los formatos mezclan «Hace 4 días», «Oct 18» y «Jul 1», sin año. |
| Contacto directo | 5 de 42 no tienen teléfono, WhatsApp ni enlace: ids 25, 26, 30, 36 y 38. |
| Ubicación | 2 de 42 no la declaran: ids 8 y 17. |
| Precio | 9 de 42 no lo declaran. El id 26 declara USD pero no monto. |
| Tipo original | El id 36 no declara tipo; se clasifica como «Inmueble». |

**Teléfonos compartidos:** hay 4 grupos de publicaciones del mismo vendedor: ids 3-4-5, 9-10, 16-17 y 20-21. No son anuncios duplicados: son propiedades distintas del mismo contacto.

**Duplicado exacto entre fuentes:** `facebook-35` y `revolico-58326838` comparten el mismo título («VENTA DE CASA – REPARTO RESIDENCIAL ASUNCIÓN, 10 DE OCTUBRE») y el mismo precio (70,000 USD). Se conservan ambos, pero quedan marcados en `posibles_duplicados` para que puedan filtrarse.

## 6. Normalización aplicada

- `detalles_propiedad.tipo`: categoría homogénea; el valor original se conserva en `tipo_original`.
- `detalles_propiedad.zona`: zona homogénea o «No especificado».
- `detalles_propiedad.distribucion`: siempre lista de texto; si el original era diccionario, se conserva en `distribucion_detallada`.
- `detalles_propiedad.detalles_estructura`: siempre lista.
- `operacion`: Venta, Alquiler o Sin clasificar, inferida del grupo o título.
- `servicios_y_caracteristicas` y `equipamiento_incluido`: siempre listas.
- `contacto.telefonos` y `contacto.whatsapp`: siempre listas cuando existen.
- Campos nuevos: `id_unico`, `fuente`, `municipio`, `municipio_evidencia`, `estado`, `posibles_duplicados` y `extras`.

## 7. Unificación

La base unificada contiene **176 registros**:

| Fuente | n |
|---|---:|
| Revolico | 134 |
| Facebook | 42 |
| **Total** | **176** |

Verificaciones:

- 176 identificadores únicos (`revolico-*` y `facebook-*`).
- Esquema superior uniforme en los 176 registros.
- `distribucion` es lista en los 176 registros.
- Los 134 registros de Revolico provienen de la base estricta ya validada.
- No se modificaron las cifras del informe A-F ni del informe revisado: ambos siguen usando solo los 134 anuncios de Revolico.

## 8. Archivos generados

| Archivo | Contenido |
|---|---|
| `datos/brutos/facebook_crudos_20261104.json` | Captura original (43) |
| `datos/limpios/facebook_publicaciones_limpias.json` | Facebook limpio y normalizado (42) |
| `datos/limpios/facebook_eliminados_por_filtro.json` | Rechazo y motivo (1) |
| `datos/limpios/datos_unificados_facebook_revolico.json` | Base unificada limpia (176) |

## 9. Conclusión

La captura nueva es una ampliación compatible: conserva las 37 publicaciones anteriores, corrige una estructura y añade 6. Tras aplicar el mismo filtro municipal y de precio que a Revolico, quedan **42 publicaciones limpias de Facebook**. La base unificada resultante tiene **176 registros**, con campos normalizados y trazabilidad de fuente. Facebook sigue fuera de las cifras del informe A-F; su incorporación es para exploración y futuras ampliaciones.

---

Proyecto de Ciencia de Datos — Universidad de La Habana  
Facultad de Matemática y Computación (MATCOM)  
Profesor: **Yudivian Almeida Cruz**
