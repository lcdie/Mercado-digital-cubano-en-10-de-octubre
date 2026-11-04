# Verificación de pertenencia al municipio Diez de Octubre

**Fecha:** 04/11/2026  
**Fuente geoespacial:** `/home/luis/proyecto-mercado-10-octubre/datos/geo/lha.geojson`, copia versionada de `/home/luis/Downloads/lha.geojson` (mismo archivo; SHA-256 `b9bbcce811d9bbfcee15f5e904d97dc24cf044cabcf17a870487ad361bb7c9e6`).
**Método:** polígono municipal + ubicación de la ficha + geocodificación de topónimos.

## 1. Análisis del GeoJSON

- Municipios incluidos: **15**.
- Municipio objetivo: **Diez de Octubre** (DPA `23.09`).
- Vértices del polígono: **11**.
- Bounding box: lon -82.3824 a -82.3361; lat 23.0780 a 23.1143.
- Área aproximada: **12.98 km²**.
- Municipios con frontera terrestre: Cerro, San Miguel del Padrón, Arroyo Naranjo, Boyeros.
- Borde compartido medido en el GeoJSON: Arroyo Naranjo (6.19 km), Cerro (4.45 km), San Miguel del Padrón (2.54 km), La Habana Vieja (1.61 km).
- **Matiz:** el GeoJSON no distingue tierra de agua. El tramo compartido con La Habana Vieja corresponde al borde norte por la bahía, y Regla solo coincide en un vértice; por eso no se cuentan como vecinos terrestres. Boyeros tampoco registra longitud de borde: la simplificación de 11 vértices reduce su frontera a un vértice.

> El polígono tiene solo 11 vértices, por lo que sirve para descartar o confirmar ubicaciones con margen, no para resolver casos catastrales a pocos metros del límite. En esos casos se usa además el municipio declarado por OpenStreetMap y la ficha del anuncio.

## 2. Cómo se diferenció el municipio

1. **Ficha del anuncio:** en Revolico se extrajo `data-cy="adLocation"` de cada página. Es la ubicación que declara el propio anuncio.
2. **Texto:** se buscaron menciones a Diez de Octubre, a sus repartos (Lawton, Luyanó, La Víbora, Santos Suárez, El Sevillano, Santa Catalina, Vista Alegre, El Mónaco, La Asunción, Reparto Flores, Plaza Roja) y a otros municipios o repartos.
3. **Geocodificación:** cada topónimo se convirtió en coordenadas con Nominatim y se comprobó con `punto_en_poligono` contra el polígono de Diez de Octubre.
4. **Criterio de resultado:**
   - **SÍ:** la ficha declara Diez de Octubre, o el texto lo declara y no hay contradicción.
   - **NO:** la ficha declara otro municipio, o el topónimo geocodificado queda fuera, sin señal interna que lo contradiga.
   - **CONTRADICTORIO:** la ficha y el texto apuntan a municipios distintos; requiere revisión manual.
   - **INDETERMINADO:** no hay ficha municipal ni topónimo verificable.

## 3. Resultado en Revolico (n = 134)

| Resultado | n | % | Nivel de evidencia |
|---|---:|---:|---|
| SÍ | 75 | 56.0% | alta/media |
| NO | 46 | 34.3% | alta |
| CONTRADICTORIO | 8 | 6.0% | baja |
| INDETERMINADO | 5 | 3.7% | baja |
| **Total** | **134** | **100.0%** | |

### 3.1 Ubicación declarada por la ficha

| Municipio en la ficha | n |
|---|---:|
| Diez de Octubre | 73 |
| Cerro | 12 |
| Centro Habana | 9 |
| (sin ubicación) | 7 |
| Playa | 6 |
| La Lisa | 5 |
| Arroyo Naranjo | 5 |
| Habana del Este | 4 |
| Plaza | 4 |
| Habana Vieja | 3 |
| Marianao | 3 |
| Guanabacoa | 2 |
| Boyeros | 1 |

**Hallazgo principal:** de los 134 anuncios de la base llamada «estricta», solo **73** declaran Diez de Octubre en su propia ficha; **54** declaran otro municipio y **7** no tienen ubicación recuperable.

Los **75** confirmados de Revolico se componen de **73** cuya ficha declara Diez de Octubre más **2** sin ubicación recuperable pero con el municipio explícito en el título: `55911834`, `58494853`.

### 3.2 Anuncios con ficha de otro municipio

| Municipio | n |
|---|---:|
| Cerro | 12 |
| Centro Habana | 9 |
| Playa | 6 |
| La Lisa | 5 |
| Arroyo Naranjo | 5 |
| Habana del Este | 4 |
| Plaza | 4 |
| Habana Vieja | 3 |
| Marianao | 3 |
| Guanabacoa | 2 |
| Boyeros | 1 |

### 3.3 Casos contradictorios

| ID | Ficha | Evidencia textual | Título |
|---|---|---|---|
| revolico-57906377 | Cerro, La Habana | DENTRO:El Mónaco | 18,000 USD Se vende apto en el Mónaco, 53250695, todo dentro, llegar y vivir. |
| revolico-57966431 | La Lisa, La Habana | DENTRO:El Sevillano; AMBIGUA:Ampliación del Sevillano | 6,000 USD En venta casa Ampliación de Sevillano, Habana |
| revolico-47222045 | Playa, La Habana | AMBIGUA:Reparto Flores | 15,000 USD Apartamento en Reparto Flores   ¡¡¡REBAJADO!!!  15 mil USD |
| revolico-58310416 | Arroyo Naranjo, La Habana | DENTRO:Santos Suárez | 36,000 USD 🏡🔥 ¡OPORTUNIDAD EN SANTOS SUÁREZ! 🔥 |
| revolico-55222736 | Arroyo Naranjo, La Habana | DENTRO:El Sevillano; AMBIGUA:Ampliación del Sevillano | 75,000 USD ESPECTACULAR CASA INDEPENDIENTE DE 2 PLANTAS EN LA AMPLIACIÓN DEL SEVILLANO!!! |
| revolico-57856310 | Cerro, La Habana | DENTRO:Diez de Octubre | 45,000 USD 🏡✨ *GRAN OPORTUNIDAD DE INVERSIÓN Y VIVIENDA 10 DE OCTUBRE** ✨🏡 |
| revolico-57855340 | Cerro, La Habana | DENTRO:Diez de Octubre; DENTRO:Calzada 10 de Octubre | 75,000 USD 🏠 *OPORTUNIDAD ÚNICA: HOGAR + NEGOCIO EN UN SOLO INMUEBLE | CALZADA 10 DE OCTUB |
| revolico-58296720 | Cerro, La Habana | DENTRO:Luyanó; AMBIGUA:Hospital Hijas de Galicia | 35,000 USD Casa en luyano a 3 cuadras de hija de Galicia |

### 3.4 Casos indeterminados

| ID | Título | Motivo |
|---|---|---|
| revolico-56030942 | Apartamento de dos  cuartos | No hay ficha municipal ni topónimo verificable en el texto. |
| revolico-57324516 | Casa bastante grande | No hay ficha municipal ni topónimo verificable en el texto. |
| revolico-58278229 | 3,000 USD Se vende casa | No hay ficha municipal ni topónimo verificable en el texto. |
| revolico-58477961 | 2,600 USD Casa | No hay ficha municipal ni topónimo verificable en el texto. |
| revolico-58492338 | 15,000 USD Venta de casa | No hay ficha municipal ni topónimo verificable en el texto. |

## 4. Resultado en Facebook (n = 42 + 1 rechazada)

| Resultado | n (base limpia) | % | Nivel de evidencia |
|---|---:|---:|---|
| SÍ | 39 | 92.9% | alta/media |
| NO | 0 | 0.0% | alta |
| CONTRADICTORIO | 0 | 0.0% | baja |
| INDETERMINADO | 3 | 7.1% | baja |
| **Total** | **42** | **100.0%** | |

La publicación rechazada previamente (id 27) queda clasificada como **NO**: menciona Santa Amalia, que OpenStreetMap ubica en Arroyo Naranjo, a 0.77 km del polígono de Diez de Octubre. La alusión a la Calzada de 10 de Octubre es una referencia de cercanía («a solo 3 cuadras»), no la ubicación de la propiedad, por lo que no se contó como señal interna. El rechazo anterior fue correcto.

### 4.1 Casos indeterminados de Facebook

| ID | Ubicación | Motivo |
|---|---|---|
| facebook-8 | (sin ubicación) | No hay ficha municipal ni topónimo verificable en el texto. |
| facebook-16 | San Leopoldo (zona céntrica) | No hay ficha municipal ni topónimo verificable en el texto. |
| facebook-17 | (sin ubicación) | No hay ficha municipal ni topónimo verificable en el texto. |

## 5. Resultado unificado (n = 176)

| Resultado | n | % |
|---|---:|---:|
| SÍ | 114 | 64.8% |
| NO | 46 | 26.1% |
| CONTRADICTORIO | 8 | 4.5% |
| INDETERMINADO | 8 | 4.5% |
| **Total** | **176** | **100.0%** |

## 6. Impacto en el informe A-F

El informe A-F ya fue recalculado con la base verificada de **114 publicaciones confirmadas** (75 de Revolico + 39 de Facebook). Las 46 de otro municipio, las 8 contradictorias y las 8 indeterminadas quedan fuera del universo. La base canónica de 134 y la versión revisada del cuestionario original se conservan como referencia histórica, pero no son comparables con el informe A-F actual.

La base depurada de confirmados está en **114 registros** (75 de Revolico + 39 de Facebook), en `datos/limpios/unificado_confirmados_diez_octubre.json`, con los campos completos de la base unificada y la verificación municipal incorporada. El generador `scripts/analisis_final_30_preguntas.py` carga esa base y produce `analisis/informe_final.md`.

## 7. Archivos generados

| Archivo | Contenido |
|---|---|
| `datos/limpios/verificacion_municipal_revolico.json` | Verificación de los 134 anuncios de Revolico |
| `datos/limpios/verificacion_municipal_facebook.json` | Verificación de las 42 publicaciones limpias + la rechazada |
| `datos/limpios/verificacion_municipal_unificado.json` | Verificación de los 176 registros unificados |
| `datos/limpios/verificacion_municipal.csv` | Resumen tabular para revisión |
| `datos/limpios/revolico_confirmados_diez_octubre.json` | 75 anuncios de Revolico confirmados |
| `datos/limpios/facebook_confirmados_diez_octubre.json` | 39 publicaciones de Facebook confirmadas |
| `datos/limpios/unificado_confirmados_diez_octubre.json` | 114 registros confirmados |

## 8. Limitaciones

- El polígono de Diez de Octubre tiene 11 vértices: es una simplificación administrativa, no un límite catastral.
- La ubicación de la ficha de Revolico la declara el anunciante y puede contener errores.
- Los topónimos se geocodifican a un punto representativo del reparto, no a la dirección exacta de la propiedad.
- La verificación cubre los 134 anuncios conservados y las 43 publicaciones de Facebook; no se re-verificaron los 136 anuncios rechazados por el filtro anterior.
- Los casos contradictorios e indeterminados se reportan como tales; no se imputa municipio.

---

Proyecto de Ciencia de Datos — Universidad de La Habana  
Facultad de Matemática y Computación (MATCOM)  
Profesor: **Yudivian Almeida Cruz**
