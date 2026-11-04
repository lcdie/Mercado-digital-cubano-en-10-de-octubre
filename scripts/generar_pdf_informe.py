#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte un informe de Markdown a PDF con portada académica.

Uso:
    python3 scripts/generar_pdf_informe.py
    python3 scripts/generar_pdf_informe.py \
        --input analisis/informe_30_preguntas_originales_reemplazadas.md \
        --output analisis/informe_30_preguntas_originales_reemplazadas.pdf \
        --subtitle "Versión revisada — 20 preguntas originales y 10 reemplazos"

Requiere las dependencias de requirements-docs.txt:
    pip install -r requirements-docs.txt
"""

import argparse
import re
from pathlib import Path

try:
    import markdown
    from weasyprint import HTML
except ImportError as exc:  # pragma: no cover - mensaje de ayuda
    raise SystemExit(
        "Faltan dependencias para generar el PDF. Instala con:\n"
        "  pip install -r requirements-docs.txt\n"
        f"Detalle: {exc}"
    )

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = BASE_DIR / "analisis" / "informe_final.md"
DEFAULT_OUTPUT = BASE_DIR / "analisis" / "informe_final.pdf"
DEFAULT_SUBTITLE = "Informe final — 30 preguntas de investigación"


def extraer_metadatos(texto):
    """Extrae fecha, fuente y universo de las líneas iniciales del informe."""
    fecha = re.search(r"\*\*Fecha de generación:\*\*\s*(.+)", texto)
    fuente = re.search(r"\*\*Fuente:\*\*\s*(.+)", texto)
    universo = re.search(r"\*\*Universo estricto:\*\*\s*(.+)", texto)
    usd = re.search(r"\*\*Anuncios con precio en USD:\*\*\s*(.+)", texto)
    return {
        "fecha": fecha.group(1).strip() if fecha else "",
        "fuente": fuente.group(1).strip() if fuente else "",
        "universo": universo.group(1).strip() if universo else "",
        "usd": usd.group(1).strip() if usd else "",
    }


def preparar_cuerpo(texto):
    """Quita el título y los metadatos que ya aparecen en la portada."""
    cuerpo = re.sub(r"^# .+\n", "", texto, count=1)
    for patron in (
        r"^\*\*Fecha de generación:\*\*.*\n?",
        r"^\*\*Corte de los datos:\*\*.*\n?",
        r"^\*\*Fuente:\*\*.*\n?",
        r"^\*\*Universo estricto:\*\*.*\n?",
        r"^\*\*Anuncios con precio en USD:\*\*.*\n?",
    ):
        cuerpo = re.sub(patron, "", cuerpo, count=1, flags=re.MULTILINE)
    return cuerpo.strip()


CSS = """
@page {
    size: A4;
    margin: 22mm 20mm 20mm 20mm;
    @top-right {
        content: "Mercado Inmobiliario Digital — Diez de Octubre";
        font-family: "DejaVu Sans", sans-serif;
        font-size: 7.5pt;
        color: #7a7a7a;
    }
    @bottom-center {
        content: counter(page) " / " counter(pages);
        font-family: "DejaVu Sans", sans-serif;
        font-size: 8.5pt;
        color: #555;
    }
}

@page cover {
    margin: 0;
    @top-right { content: none; }
    @bottom-center { content: none; }
}

html {
    font-family: "DejaVu Serif", Georgia, serif;
    font-size: 10.4pt;
    line-height: 1.45;
    color: #1b1b1b;
}

.cover {
    page: cover;
    height: 297mm;
    box-sizing: border-box;
    padding: 34mm 28mm 28mm;
    position: relative;
}

.cover-top { text-align: center; }
.cover-top .uni {
    font-family: "DejaVu Sans", sans-serif;
    font-size: 15pt;
    font-weight: bold;
    color: #123c69;
    margin: 0;
}
.cover-top .fac {
    font-family: "DejaVu Sans", sans-serif;
    font-size: 11.5pt;
    color: #333;
    margin: 4mm 0 0;
}
.cover-top .asig {
    font-family: "DejaVu Sans", sans-serif;
    font-size: 10pt;
    color: #666;
    margin: 2mm 0 0;
    letter-spacing: .04em;
    text-transform: uppercase;
}
.cover-rule {
    width: 45mm;
    border: 0;
    border-top: 2.5px solid #123c69;
    margin: 8mm auto 0;
}
.cover-title {
    margin-top: 52mm;
    text-align: center;
}
.cover-title h1 {
    font-family: "DejaVu Sans", sans-serif;
    font-size: 25pt;
    line-height: 1.18;
    color: #0d2b45;
    margin: 0;
}
.cover-title .subtitle {
    font-family: "DejaVu Sans", sans-serif;
    font-size: 12.5pt;
    color: #2e6da4;
    margin: 7mm 0 0;
}
.cover-title .place {
    font-size: 10pt;
    color: #666;
    margin: 4mm 0 0;
}
.cover-meta {
    position: absolute;
    bottom: 30mm;
    left: 28mm;
    right: 28mm;
    border-top: 1px solid #123c69;
    padding-top: 5mm;
    font-size: 10pt;
}
.cover-meta p { margin: 1.6mm 0; text-align: left; }
.cover-meta strong { color: #123c69; }

main h2 {
    font-family: "DejaVu Sans", sans-serif;
    font-size: 15pt;
    color: #123c69;
    border-bottom: 2px solid #123c69;
    padding-bottom: 2mm;
    margin: 8mm 0 3mm;
    page-break-after: avoid;
}
main h3 {
    font-family: "DejaVu Sans", sans-serif;
    font-size: 12pt;
    color: #1f5f8b;
    margin: 6mm 0 2mm;
    page-break-after: avoid;
}
p {
    text-align: justify;
    margin: 1.6mm 0;
}
strong { color: #0d2b45; }
blockquote {
    margin: 2.2mm 0 3mm;
    padding: 2.2mm 3.5mm;
    background: #f4f7fb;
    border-left: 3.5px solid #2e6da4;
    page-break-inside: avoid;
}
blockquote p { margin: 1mm 0; }
table {
    width: 100%;
    border-collapse: collapse;
    margin: 3mm 0 5mm;
    font-size: 8.7pt;
    page-break-inside: avoid;
}
th {
    background: #123c69;
    color: #ffffff;
    font-family: "DejaVu Sans", sans-serif;
    font-size: 8.5pt;
    padding: 2.2mm;
    text-align: left;
}
td {
    border: 1px solid #cfd8e3;
    padding: 1.8mm 2.2mm;
    vertical-align: top;
}
tr:nth-child(even) td { background: #f7f9fc; }
ul, ol { margin: 1.5mm 0 3mm 6mm; padding: 0; }
li { margin: .8mm 0; text-align: justify; }
code {
    font-family: "DejaVu Sans Mono", monospace;
    font-size: 8.4pt;
    background: #eef2f6;
    padding: .3mm 1mm;
}
hr {
    border: 0;
    border-top: 1px solid #c9d3de;
    margin: 6mm 0 3mm;
}
"""


def construir_html(cuerpo_html, meta, subtitle=DEFAULT_SUBTITLE):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Informe Final — Mercado Inmobiliario Digital en Diez de Octubre</title>
<style>{CSS}</style>
</head>
<body>
<section class="cover">
    <div class="cover-top">
        <p class="uni">Universidad de La Habana</p>
        <p class="fac">Facultad de Matemática y Computación (MATCOM)</p>
        <p class="asig">Ciencia de Datos</p>
        <hr class="cover-rule">
    </div>
    <div class="cover-title">
        <h1>Mercado Inmobiliario Digital en Diez de Octubre</h1>
        <p class="subtitle">{subtitle}</p>
        <p class="place">La Habana, Cuba</p>
    </div>
    <div class="cover-meta">
        <p><strong>Profesor:</strong> Yudivian Almeida Cruz</p>
        <p><strong>Fuente:</strong> {meta['fuente']}</p>
        <p><strong>Universo estricto:</strong> {meta['universo']}</p>
        <p><strong>Anuncios con precio en USD:</strong> {meta['usd']}</p>
        <p><strong>Fecha de generación:</strong> {meta['fecha']}</p>
    </div>
</section>
<main>
{cuerpo_html}
</main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Convierte un informe Markdown en PDF con portada académica."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Ruta del informe Markdown de entrada.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Ruta del PDF de salida.",
    )
    parser.add_argument(
        "--subtitle",
        default=DEFAULT_SUBTITLE,
        help="Subtítulo que aparece en la portada.",
    )
    args = parser.parse_args()

    input_file = Path(args.input)
    output_file = Path(args.output)

    if not input_file.exists():
        raise SystemExit(
            f"No se encontró {input_file}. Ejecuta primero el generador del informe."
        )

    texto = input_file.read_text(encoding="utf-8")
    meta = extraer_metadatos(texto)
    cuerpo_md = preparar_cuerpo(texto)
    cuerpo_html = markdown.markdown(
        cuerpo_md,
        extensions=["tables", "sane_lists", "fenced_code"],
    )
    html = construir_html(cuerpo_html, meta, args.subtitle)

    documento = HTML(string=html, base_url=str(BASE_DIR)).render()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    documento.write_pdf(str(output_file))

    print(f"PDF guardado en: {output_file}")
    print(f"Páginas: {len(documento.pages)}")


if __name__ == "__main__":
    main()
