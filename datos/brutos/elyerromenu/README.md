# Datos de elyerromenu

Esta carpeta contiene los datos crudos extraídos de https://elyerromenu.com mediante
el script `scripts/scraper_elyerromenu.py`.

## Estructura

- `elyerromenu-<id>.json`: un archivo por anuncio extraído.
- Cada archivo tiene la misma estructura que los registros de Facebook/Revolico de tu proyecto.

## Advertencias

- Los datos están SIN verificar municipalmente.
- Antes de incluirlos en el informe, pásalos por tu pipeline de verificación municipal
  (regla de título primero + polígono de Diez de Octubre).
- Revisa `https://elyerromenu.com/robots.txt` y los términos de servicio antes de ejecutar el scraper.
- No recolectes datos personales (teléfonos, nombres) sin consentimiento.

## Requisitos

```bash
pip install requests beautifulsoup4
```

## Ejecución

```bash
python3 scripts/scraper_elyerromenu.py
```
