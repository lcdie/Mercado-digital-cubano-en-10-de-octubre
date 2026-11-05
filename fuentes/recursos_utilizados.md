# Recursos utilizados — Mercado inmobiliario digital en Diez de Octubre

**Proyecto:** Ciencia de Datos, Universidad de La Habana (MATCOM)  
**Tema:** opacidad, dolarización, desigualdad territorial e informalidad del mercado inmobiliario digital de Diez de Octubre  
**Universo:** 122 publicaciones confirmadas dentro del municipio (83 de Revolico + 39 de Facebook)

---

## 1. Fuentes de anuncios (datos primarios)

### 1.1 Revolico
- **Enlace web:** `https://www.revolico.com`

### 1.2 Facebook
- **Enlace web:** `https://www.facebook.com` (grupos y páginas de compraventa; no se reproducen enlaces individuales ni nombres de grupos por privacidad)

---

## 2. Recursos geoespaciales

### 2.1 GeoJSON municipal de La Habana
- **Archivo:** `datos/geo/lha.geojson`
- **Uso:** Comprobación punto-en-polígono para verificar que un anuncio pertenece al municipio Diez de Octubre (DPA `23.09`)
- **Polígono:** Simplificación de 11 vértices; no resuelve casos catastrales a pocos metros del borde
- **SHA-256:** `b9bbcce811d9bbfcee15f5e904d97dc24cf044cabcf17a870487ad361bb7c9e6`
- **Notas:** Copia versionada del polígono de La Habana.

### 2.2 Nominatim / OpenStreetMap
- **Uso:** Geocodificación de topónimos (barrios, repartos) mencionados en los anuncios para traducirlos a coordenadas y comprobar pertenencia al polígono municipal
- **Caché local:** `datos/geo/geocoding_lha.json`
- **Notas:** Se utilizó para resolver ambigüedades cuando el campo `zona` de la ficha no era suficiente. Los resultados se cachearon localmente para evitar llamadas repetidas.

---

## 3. Fuentes oficiales (contexto)

### 3.1 Oficina Nacional de Estadística e Información (ONEI) — Cuba
- **Documento:** `fuentes/anuario_estadístico_notas.md`
- **Uso:** Contexto general de población, vivienda y tenencia del municipio Diez de Octubre
- **Propósito:** Enmarcar la muestra digital de Revolico dentro del perfil oficial del municipio
- **Notas:** Todas las fuentes se citan con el fin de dar validez al análisis sin entrar en aspectos políticos.

---

## 4. Base de datos generada

### 4.1 Base unificada de confirmados
- **Archivo:** `datos/limpios/unificado_confirmados_diez_octubre.json`
- **Contenido:** 122 publicaciones confirmadas dentro de Diez de Octubre (83 de Revolico + 39 de Facebook)
- **Campos:** `id_unico`, `fuente`, `publicacion` (título, enlace, fecha, grupo, autor), `precio` (monto, moneda, negociable, nota), `operacion`, `detalles_propiedad` (tipo, ubicación, zona), `contacto`, `verificacion_municipal`, `posibles_duplicados`, `extras`, `fecha_verificacion`

### 4.2 Base de descartes
- **Archivo:** `datos/limpios/descartados_diez_octubre.json` y `.csv`
- **Contenido:** 55 registros no incluidos (47 `NO`, 8 `INDETERMINADO`, 1 fuera del universo: `facebook-27`)
- **Cada registro conserva:** `registro_original`, `registro_unificado` exacto, `motivo_descarte`, `evidencia_principal`, `confianza`

---

## 5. Notas sobre la evidencia

- Los precios son precios de oferta, no de transacción.
- No hay datos homogéneos de metros cuadrados, habitaciones, baños, estado legal, año de construcción, vendedor o agencia.
- Las ausencias (sin precio, sin zona, sin operación) se conservan y se reportan como hallazgo; no se imputan valores.
- El único precio en CUP no se convierte a USD por falta de un tipo de cambio oficial o de mercado claramente definido para el corte.
- Los subgrupos con n < 10 se presentan como evidencia descriptiva, no como conclusión firme.
