# Bitácora de cambios — Mercado inmobiliario digital en Diez de Octubre

**Proyecto:** Ciencia de Datos, Universidad de La Habana (MATCOM)  
**Tema:** opacidad, dolarización, desigualdad territorial e informalidad del mercado inmobiliario digital de Diez de Octubre  
**Repositorio:** `Mercado-digital-cubano-en-10-de-octubre`

---

## Convenciones

- `n` siempre se reporta junto al resultado.
- 134 = base histórica etiquetada (no verificada); 122 = base verificada (informe canónico).
- Los descartes se conservan íntegros; no se elimina información.

---

## Historial de cambios

### 2026-11-05 — Cierre para entrega (informe + repositorio defendible)

- Se implementa la regla **título primero**: el título decide; ficha, enlace, grupo, ubicación y zona solo se usan cuando el título no aporta señal.
- Título con lugar externo ⇒ `NO`; título con Diez de Octubre o reparto interno ⇒ `SÍ`.
- Se regenera el universo: **122 confirmados** (83 Revolico + 39 Facebook), 46 `NO`, 0 `CONTRADICTORIO`, 8 `INDETERMINADO`.
- Se generan `datos/limpios/descartados_diez_octubre.json` y `.csv` con **55 registros** (47 `NO`, 8 `INDETERMINADO` y `facebook-27` fuera del universo); los 54 del universo conservan `registro_unificado` exacto.
- Se corrige el script `verificar_municipio_publicaciones.py`: `lineterminator="\n"` en CSV, geocodificación con caché, trazabilidad del SHA-256 del GeoJSON.
- Se regenera `analisis/informe_final.md` y `analisis/informe_final.pdf` (14 páginas).
- Se corrige la contradicción territorial del resumen y las conclusiones: La Víbora tiene la **media más alta** (n = 11); El Sevillano la **mediana más alta** (n = 10); El Mónaco lidera la media entre n ≥ 5 (n = 6), no la mediana.
- Se añade al informe el **Anexo: fuentes, cobertura y referencias** con tabla de fuentes, cobertura por campo y referencias (ONEI, Nominatim/OpenStreetMap, GeoJSON municipal, Revolico, Facebook).
- Se añade `scripts/cifras_control.py`: 36 cifras de control que validan el informe (sale con código 0 si todo cuadra).
- Se añade `tests/test_verificacion.py` con 8 pruebas de contrato: universo 122, fuentes 83/39, descartes 55, integridad de registros, no solapamiento, títulos externos, estadísticos de ventas y duplicado conocido.
- Se añade `data_dictionary.md` y `bitacora_cambios.md`.
- Se fijan dependencias en `requirements.txt` (pendiente de versiones exactas si se reproduce el entorno).
- Se verifica `git diff --check` sin errores y se crea commit local.

### 2026-11-04 — Priorización del título y conservación de descartes

- Commit `7fc9c7e feat: priorizar el título y conservar íntegros los descartados municipales`.
- Se actualizan `README.md`, `verificacion_municipal_geojson_20261104.md`, las bases de confirmados y la base de descartados.
- Se eliminan espacios finales en la fecha del reporte y se corrigen los CSV con `lineterminator="\n"`.
- Se verifica la integridad: 176 en el universo, 122 confirmados, 55 descartados, sin solapamiento y sin alteración de registros.

### 2026-11-03 y anteriores — Pipeline de obtención y verificación

- `src/scrape_revolico.py`: descarga de anuncios de Revolico (filtrado por municipio en la URL; campo `municipio` no fiable).
- `scripts/limpieza_final_municipio.py`, `limpiar_facebook.py`, `mezclar_facebook_revolico.py`: bases limpias y unificación de 176 publicaciones.
- `scripts/verificar_municipio_publicaciones.py`: verificación municipal con polígono DPA 23.09 y geocodificación Nominatim.
- `scripts/analisis_final_30_preguntas.py`: informe A-F con 30 preguntas.
- `scripts/generar_pdf_informe.py`: conversión Markdown → PDF (14 páginas).
- `fuentes/anuario_estadistico_notas.md`: nota de fuente oficial ONEI.

---

## Pendientes operativos (no bloquean la entrega del informe)

- **Push a origin:** credenciales de GitHub no configuradas y `gh` no instalado. El token expuesto anteriormente no se reutiliza.
- **Versiones fijadas:** `requirements.txt` usa `>=`; para reproducibilidad exacta conviene pasar a `==` con las versiones instaladas.
- **AGENTS.md:** faltan invariantes del pipeline para reproducción automatizada.
- **Script `run_all.sh`:** faltan los cuatro pasos del pipeline en un único ejecutable.
