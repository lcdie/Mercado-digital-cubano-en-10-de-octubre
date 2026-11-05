# Estado del proyecto

Este documento resume las fases completadas, los análisis terminados, las tareas pendientes y los problemas conocidos. Se actualiza con cada avance relevante.

## Fases completadas

| Fase | Descripción | Estado |
|---|---|---|
| Obtención de datos | Scraping de Revolico (83 confirmadas) y captura de Facebook (39 confirmadas) | ✅ Completada |
| Limpieza y unificación | 176 registros unificados (134 Revolico + 42 Facebook) | ✅ Completada |
| Verificación municipal | Regla de título primero + polígono DPA 23.09 + geocodificación | ✅ Completada (122 confirmados, 55 descartes) |
| Informe final A-F | 30 preguntas en 6 bloques con n y nivel de evidencia | ✅ Completado (Markdown + PDF) |
| Control de cifras | 36 cifras validadas contra los datos | ✅ Completado (`cifras_control.py`) |
| Pruebas de contrato | 8 pruebas que protegen el universo verificado | ✅ Completado (`tests/test_verificacion.py`) |
| Integración continua | GitHub Actions ejecuta pruebas y cifras en cada push | ✅ Configurado (`.github/workflows/ci.yml`) |
| Gráficos de exposición | 5 PNG para la presentación oral | ✅ Generados (`graficos/`) |
| Documentación de datos | `data_dictionary.md`, `datos/README.md` | ✅ Completado |
| Bitácora de cambios | Historia 134 → 122 y decisiones manuales | ✅ Completado (`bitacora_cambios.md`) |
| Anexo de recursos | Enlaces web de fuentes primarias | ✅ Completado (`fuentes/recursos_utilizados.md`) |

## Análisis terminados

- **Bloque A — Precios de referencia:** A1–A5 respondidas en `analisis/informe_final.md`.
- **Bloque B — Desigualdades territoriales:** B1–B5 respondidas.
- **Bloque C — Dolarización:** C1–C5 respondidas.
- **Bloque D — Opacidad de la información:** D1–D5 respondidas.
- **Bloque E — Prácticas informales:** E1–E5 respondidas.
- **Bloque F — Tipos de inmueble y accesibilidad:** F1–F5 respondidas.

## Tareas pendientes

| Tarea | Prioridad | Notas |
|---|---|---|
| Push a GitHub (`git push origin main`) | Alta | Pendiente por credenciales y token revocado. No reutilizar el token expuesto. |
| Metadatos de GitHub (descripción, topics, enlace al informe) | Media | Se configura en la interfaz web de GitHub, no en el repositorio local. |
| Carpeta `evidencias/` con audios y fotos de Facebook | Media | Pendiente de material del usuario. Los README ya están creados. |
| Fijar versiones en `requirements-docs.txt` | Baja | Ya fijadas (`Markdown==3.11.2`, `weasyprint==70.0`). |

## Problemas conocidos

- El push a `origin/main` no se ha completado porque el repositorio remoto tiene commits que no están en la rama local (`c6e6c1f` vs `a82283a`). Será necesario hacer `git pull --rebase origin main` antes de push.
- El token de GitHub previamente compartido en el chat fue revocado por seguridad. Se necesita uno nuevo para hacer push.
- `datos/brutos/*.json` está en `.gitignore` con excepción `!datos/brutos/.gitkeep`; algunos archivos brutos se versionaron con `git add -f`.

## Próximas mejoras

- Resolver credenciales y hacer push a GitHub.
- Añadir metadatos de GitHub (descripción, topics, enlace al informe, imagen representativa).
- Si se dispone de audios y fotos de Facebook, incluirlos en `evidencias/` siguiendo las normas de anonimato.

## Invariantes del proyecto (no modificar sin revisar el informe)

- El título manda en la verificación municipal.
- No se elimina información: los 55 descartes se conservan íntegros.
- El universo es 122 confirmados (83 Revolico + 39 Facebook). 134 es referencia histórica, no comparable.
- No se imputan valores ausentes.
- No se añaden fuentes ajenas (Cubisima, HogarEnCuba, entrevistas, tasas de cambio).
- No se cambia el universo a última hora.
