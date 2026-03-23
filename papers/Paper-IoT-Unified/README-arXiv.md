# arXiv Submission Package: Unified IoT Paper

This directory contains the complete LaTeX source ready for arXiv submission.

## Files Included

- `main.tex`: The master LaTeX document with standard arXiv/neurips preamble.
- `paper_body.tex`: The compiled LaTeX body (converted via Pandoc from the Markdown sections).
- `references.bib`: The BibTeX file containing all 24 academic citations.
- `figures/`: Contains the 5 high-fidelity technical diagrams.

## Critical Step Before Submission

arXiv does **not** natively compile `.svg` images. The `main.tex` file has already been configured to look for `.pdf` versions of your figures. 

Before uploading the `.zip` to arXiv, you must convert the 5 `.svg` files in the `figures/` directory to `.pdf`.

### How to Convert (macOS)
If you have Inkscape installed:
```bash
inkscape --export-type="pdf" figures/*.svg
```

Or using a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install svglib reportlab
python3 convert_figures.py
```

## Assembly & Submission
Once the figures are in `.pdf` format, simply compress the files into a single `.zip` archive:

```bash
zip -r arxiv_submission.zip main.tex paper_body.tex references.bib figures/*.pdf
```
Upload this `arxiv_submission.zip` directly to the arXiv submission portal. Moderation will see standard LaTeX formatting, formal math equations, and substantive empirical tables.
