# Verificación de pertenencia al municipio Diez de Octubre

**Fecha:** 06/11/2026
**Fuente geoespacial:** `/home/luis/proyecto-mercado-10-octubre/datos/geo/lha.geojson`, copia versionada de `/home/luis/Downloads/lha.geojson` (mismo archivo; SHA-256 `b9bbcce811d9bbfcee15f5e904d97dc24cf044cabcf17a870487ad361bb7c9e6`).
**Método:** título primero + polígono municipal + ficha como respaldo + geocodificación de topónimos.

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

1. **Título (evidencia principal):** se analiza primero el título de cada publicación. Si nombra Diez de Octubre o un reparto interno, la publicación se incluye; si nombra un municipio, reparto o localidad externa, se descarta.
2. **Ficha del anuncio:** en Revolico se extrajo `data-cy="adLocation"` de cada página. Solo se usa cuando el título no aporta una señal municipal.
3. **Resto del texto:** enlace de Revolico y grupo, autor, ubicación o zona de Facebook. Es el último respaldo cuando ni el título ni la ficha deciden.
4. **Geocodificación:** cada topónimo se convirtió en coordenadas con Nominatim y se comprobó con `punto_en_poligono` contra el polígono de Diez de Octubre.
5. **Criterio de resultado:**
   - **SÍ:** el título nombra Diez de Octubre o un reparto interno; si el título no aporta señal, la ficha (o el resto del texto) declara el municipio.
   - **NO:** el título nombra un lugar fuera del municipio; si el título no aporta señal, la ficha (o el resto del texto) declara otro municipio.
   - **CONTRADICTORIO:** el título mezcla referencias internas y externas, o la ficha contradice al resto del texto cuando el título no decide.
   - **INDETERMINADO:** ni el título, ni la ficha, ni el resto del texto aportan una ubicación verificable.

> **Regla de título:** la mención explícita del título prevalece sobre la ficha del anuncio. Un título que dice «Santos Suárez», «Lawton», «La Víbora», «Luyanó», «El Sevillano», «10 de Octubre» o «Calzada 10 de Octubre» confirma la pertenencia aunque la ficha declare Cerro o Arroyo Naranjo. Lo mismo vale en sentido contrario: «Víbora Park», «Boca Ciega», «Casino Deportivo» o «Santa Amalia» descartan la publicación aunque la ficha diga Diez de Octubre.

## 3. Resultado en Revolico (n = 134)

| Resultado | n | % | Nivel de evidencia |
|---|---:|---:|---|
| SÍ | 83 | 61.9% | alta/media |
| NO | 46 | 34.3% | alta |
| CONTRADICTORIO | 0 | 0.0% | baja |
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

Los **83** confirmados de Revolico se componen de **73** cuya ficha declara Diez de Octubre, **8** con ficha de otro municipio pero título que nombra un reparto interno (la regla de título prevalece) y **2** sin ficha recuperable que se confirman por el título: `55911834`, `58494853`.

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

### 3.3 Casos con ficha de otro municipio resueltos por el título

Estos anuncios tienen ficha en otro municipio, pero el título nombra un reparto de Diez de Octubre. La regla de título los confirma y se conservan con la contradicción documentada.

| ID | Ficha | Título | Evidencia interna del título |
|---|---|---|---|
| revolico-57906377 | Cerro, La Habana | 18,000 USD Se vende apto en el Mónaco, 53250695, todo dentro, llegar y vivir. | DENTRO:El Mónaco |
| revolico-57966431 | La Lisa, La Habana | 6,000 USD En venta casa Ampliación de Sevillano, Habana | DENTRO:El Sevillano; AMBIGUA:Ampliación del Sevillano |
| revolico-47222045 | Playa, La Habana | 15,000 USD Apartamento en Reparto Flores   ¡¡¡REBAJADO!!!  15 mil USD | AMBIGUA:Reparto Flores |
| revolico-58310416 | Arroyo Naranjo, La Habana | 36,000 USD 🏡🔥 ¡OPORTUNIDAD EN SANTOS SUÁREZ! 🔥 | DENTRO:Santos Suárez |
| revolico-55222736 | Arroyo Naranjo, La Habana | 75,000 USD ESPECTACULAR CASA INDEPENDIENTE DE 2 PLANTAS EN LA AMPLIACIÓN DEL SEVILLANO!!! | DENTRO:El Sevillano; AMBIGUA:Ampliación del Sevillano |
| revolico-57856310 | Cerro, La Habana | 45,000 USD 🏡✨ *GRAN OPORTUNIDAD DE INVERSIÓN Y VIVIENDA 10 DE OCTUBRE** ✨🏡 | DENTRO:Diez de Octubre |
| revolico-57855340 | Cerro, La Habana | 75,000 USD 🏠 *OPORTUNIDAD ÚNICA: HOGAR + NEGOCIO EN UN SOLO INMUEBLE | CALZADA 10 DE OCTUB | DENTRO:Diez de Octubre; DENTRO:Calzada 10 de Octubre |
| revolico-58296720 | Cerro, La Habana | 35,000 USD Casa en luyano a 3 cuadras de hija de Galicia | DENTRO:Luyanó; AMBIGUA:Hospital Hijas de Galicia |

### 3.4 Casos indeterminados

| ID | Título | Motivo |
|---|---|---|
| revolico-56030942 | Apartamento de dos  cuartos | El título, la ficha y el resto del texto no aportan una ubicación municipal verificable. |
| revolico-57324516 | Casa bastante grande | El título, la ficha y el resto del texto no aportan una ubicación municipal verificable. |
| revolico-58278229 | 3,000 USD Se vende casa | El título, la ficha y el resto del texto no aportan una ubicación municipal verificable. |
| revolico-58477961 | 2,600 USD Casa | El título, la ficha y el resto del texto no aportan una ubicación municipal verificable. |
| revolico-58492338 | 15,000 USD Venta de casa | El título, la ficha y el resto del texto no aportan una ubicación municipal verificable. |

### 3.5 Casos contradictorios residuales

Ninguno. Los 8 casos que la regla anterior marcaba como contradictorios tenían un título con un reparto interno y quedaron confirmados por la regla de título (ver sección 3.3).

## 4. Resultado en Facebook (n = 42 + 1 rechazada)

| Resultado | n (base limpia) | % | Nivel de evidencia |
|---|---:|---:|---|
| SÍ | 39 | 92.9% | alta/media |
| NO | 0 | 0.0% | alta |
| CONTRADICTORIO | 0 | 0.0% | baja |
| INDETERMINADO | 3 | 7.1% | baja |
| **Total** | **42** | **100.0%** | |

La publicación rechazada previamente (id 27) queda clasificada como **NO**: su título nombra **Santa Amalia**, que OpenStreetMap ubica en Arroyo Naranjo, a 0.77 km del polígono de Diez de Octubre. La alusión a la Calzada de 10 de Octubre, en el resto del texto, es una referencia de cercanía («a solo 3 cuadras»), no la ubicación de la propiedad. La regla de título descarta la publicación y confirma el rechazo anterior.

### 4.1 Casos indeterminados de Facebook

| ID | Ubicación | Motivo |
|---|---|---|
| facebook-8 | (sin ubicación) | El título, la ficha y el resto del texto no aportan una ubicación municipal verificable. |
| facebook-16 | San Leopoldo (zona céntrica) | El título, la ficha y el resto del texto no aportan una ubicación municipal verificable. |
| facebook-17 | (sin ubicación) | El título, la ficha y el resto del texto no aportan una ubicación municipal verificable. |

## 5. Resultado unificado (n = 176)

| Resultado | n | % |
|---|---:|---:|
| SÍ | 122 | 69.3% |
| NO | 46 | 26.1% |
| CONTRADICTORIO | 0 | 0.0% |
| INDETERMINADO | 8 | 4.5% |
| **Total** | **176** | **100.0%** |

## 6. Impacto en el informe A-F

El informe A-F ya fue recalculado con la base verificada de **122 publicaciones confirmadas** (83 de Revolico + 39 de Facebook). Las 46 de otro municipio, las 0 contradictorias y las 8 indeterminadas quedan fuera del universo. La base canónica de 134 y la versión revisada del cuestionario original se conservan como referencia histórica, pero no son comparables con el informe A-F actual.

La base depurada de confirmados está en **122 registros** (83 de Revolico + 39 de Facebook), en `datos/limpios/unificado_confirmados_diez_octubre.json`, con los campos completos de la base unificada y la verificación municipal incorporada. El generador `scripts/analisis_final_30_preguntas.py` carga esa base y produce `analisis/informe_final.md`.

Ningún registro se elimina de las bases originales. Los **55** registros no incluidos (más la publicación rechazada previamente) se conservan íntegros en `datos/limpios/descartados_diez_octubre.json`, con su resultado, confianza, evidencia principal, motivo de descarte, registro original y registro unificado exacto. También hay una versión tabular en `datos/limpios/descartados_diez_octubre.csv`.

## 7. Archivos generados

| Archivo | Contenido |
|---|---|
| `datos/limpios/verificacion_municipal_revolico.json` | Verificación de los 134 anuncios de Revolico |
| `datos/limpios/verificacion_municipal_facebook.json` | Verificación de las 42 publicaciones limpias + la rechazada |
| `datos/limpios/verificacion_municipal_unificado.json` | Verificación de los 176 registros unificados |
| `datos/limpios/verificacion_municipal.csv` | Resumen tabular para revisión |
| `datos/limpios/revolico_confirmados_diez_octubre.json` | 83 anuncios de Revolico confirmados |
| `datos/limpios/facebook_confirmados_diez_octubre.json` | 39 publicaciones de Facebook confirmadas |
| `datos/limpios/unificado_confirmados_diez_octubre.json` | 122 registros confirmados |
| `datos/limpios/descartados_diez_octubre.json` | 55 registros descartados con motivo, registro original y registro unificado |
| `datos/limpios/descartados_diez_octubre.csv` | Versión tabular de los descartados |

## 8. Limitaciones

- El polígono de Diez de Octubre tiene 11 vértices: es una simplificación administrativa, no un límite catastral.
- La regla de título prioriza la mención textual sobre la ficha. Si el título usa un topónimo ambiguo, la publicación se conserva con confianza media y la ambigüedad queda documentada.
- **Ampliación del Sevillano** y **Reparto Flores** se incluyen por mención interna en el título. El topónimo completo no se pudo geocodificar; la señal verificable es «Sevillano» (Diez de Octubre) y «Flores» (Santos Suárez, Diez de Octubre). Por eso su confianza es media, no alta.
- La ubicación de la ficha de Revolico la declara el anunciante y puede contener errores. La regla de título puede confirmar un anuncio aunque la ficha esté mal declarada.
- Los topónimos se geocodifican a un punto representativo del reparto, no a la dirección exacta de la propiedad.
- La verificación cubre los 134 anuncios conservados y las 43 publicaciones de Facebook; no se re-verificaron los 136 anuncios rechazados por el filtro anterior.
- Los casos indeterminados se reportan como tales; no se imputa municipio. Los descartados se conservan íntegros en `datos/limpios/descartados_diez_octubre.json`.

---

Proyecto de Ciencia de Datos — Universidad de La Habana  
Facultad de Matemática y Computación (MATCOM)  
Profesor: **Yudivian Almeida Cruz**
