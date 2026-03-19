import os
import glob
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

figure_dir = "figures"
svg_files = glob.glob(os.path.join(figure_dir, "*.svg"))

print(f"Found {len(svg_files)} SVG files to convert.")

for svg_file in svg_files:
    pdf_file = svg_file.replace(".svg", ".pdf")
    try:
        drawing = svg2rlg(svg_file)
        renderPDF.drawToFile(drawing, pdf_file)
        print(f"✅ Converted {svg_file} to {pdf_file}")
    except Exception as e:
        print(f"❌ Failed to convert {svg_file}: {e}")
