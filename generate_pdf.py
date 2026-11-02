"""
Generate high-fidelity PDF from Raspberry Pi DOCUMENTATION.md using headless Microsoft Edge.
Clean, executive design without raw code dumps, focused on architecture, operations, and feature roadmaps.
"""

import os
import sys
import subprocess
from pathlib import Path
import markdown

BASE_DIR = Path(r"d:\e\Kites Robotics\Assis projects\Raspberry")
MD_PATH = BASE_DIR / "DOCUMENTATION.md"
HTML_PATH = BASE_DIR / "documentation_rendered.html"
PDF_PATH = BASE_DIR / "Encycle_Bank_Documentation.pdf"
EW_PDF_PATH = Path(r"d:\e\Kites Robotics\Assis projects\ewaste-kiosk\Encycle_Bank_Documentation.pdf")

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE_PATH):
    EDGE_PATH = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

def build_pdf():
    print(f"[PDF Generator] Reading {MD_PATH} ...")
    content = MD_PATH.read_text(encoding="utf-8")

    extensions = [
        "markdown.extensions.tables",
        "markdown.extensions.fenced_code",
        "markdown.extensions.toc",
        "markdown.extensions.nl2br",
        "markdown.extensions.sane_lists",
    ]
    
    html_body = markdown.markdown(content, extensions=extensions)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Encycle Bank — Raspberry Pi Kiosk Documentation</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {{
      content: "Encycle Bank — Kites Robotics";
      font-family: 'Inter', sans-serif;
      font-size: 8pt;
      color: #94a3b8;
    }}
    @bottom-right {{
      content: counter(page);
      font-family: 'Inter', sans-serif;
      font-size: 8pt;
      color: #64748b;
    }}
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.65;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }}

  /* Headings */
  h1, h2, h3, h4 {{
    font-family: 'Outfit', 'Inter', sans-serif;
    color: #0f172a;
    font-weight: 700;
    line-height: 1.25;
    margin-top: 1.6em;
    margin-bottom: 0.5em;
  }}

  h1 {{
    font-size: 22pt;
    font-weight: 800;
    color: #065f46;
    border-bottom: 2.5px solid #10b981;
    padding-bottom: 6px;
    margin-top: 0;
    page-break-before: always;
  }}

  h1:first-of-type {{
    page-break-before: avoid;
  }}

  h2 {{
    font-size: 15pt;
    color: #047857;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 24px;
    page-break-after: avoid;
  }}

  h3 {{
    font-size: 12pt;
    color: #0f172a;
    margin-top: 18px;
    page-break-after: avoid;
  }}

  h4 {{
    font-size: 10.5pt;
    color: #334155;
    margin-top: 12px;
    page-break-after: avoid;
  }}

  p, li {{
    color: #334155;
    margin-bottom: 0.6em;
  }}

  ul, ol {{
    padding-left: 20px;
    margin-top: 0.4em;
    margin-bottom: 0.8em;
  }}

  li {{
    margin-bottom: 4px;
  }}

  strong {{
    color: #0f172a;
    font-weight: 600;
  }}

  /* Cover Page */
  .cover-page {{
    height: 100vh;
    min-height: 250mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    padding: 30mm 10mm 20mm 10mm;
    page-break-after: always;
  }}

  .cover-badge {{
    background: #ecfdf5;
    color: #059669;
    border: 1px solid #10b981;
    font-weight: 700;
    font-size: 9.5pt;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 9999px;
    margin-bottom: 20px;
  }}

  .cover-title {{
    font-family: 'Outfit', sans-serif;
    font-size: 32pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.15;
    margin: 0 0 12px 0;
  }}

  .cover-title span {{
    color: #059669;
  }}

  .cover-subtitle {{
    font-size: 13.5pt;
    color: #475569;
    max-width: 620px;
    line-height: 1.5;
    margin-bottom: 30px;
  }}

  .cover-meta {{
    margin-top: auto;
    border-top: 2px solid #e2e8f0;
    padding-top: 18px;
    width: 100%;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    font-size: 9.5pt;
    color: #64748b;
  }}

  .cover-meta strong {{
    display: block;
    color: #0f172a;
    font-size: 10pt;
    margin-bottom: 2px;
  }}

  /* ASCII & Architectural Schematics */
  pre {{
    background: #0f172a;
    color: #38bdf8;
    border-radius: 8px;
    padding: 12px 14px;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8pt;
    line-height: 1.4;
    overflow-x: auto;
    margin: 12px 0;
    border: 1px solid #1e293b;
    page-break-inside: avoid;
  }}

  code {{
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #047857;
    padding: 1.5px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    border: none;
    font-size: inherit;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }}

  th, td {{
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    text-align: left;
    vertical-align: top;
  }}

  th {{
    background-color: #065f46;
    color: #ffffff;
    font-weight: 600;
    font-size: 8.5pt;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }}

  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}

  /* Callouts & Quotes */
  blockquote {{
    border-left: 4px solid #10b981;
    background: #f0fdf4;
    padding: 8px 14px;
    margin: 14px 0;
    border-radius: 0 6px 6px 0;
    color: #166534;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}

  blockquote p {{
    margin: 0;
    color: inherit;
  }}

  /* Dividers */
  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 20px 0;
  }}
</style>
</head>
<body>

<!-- Front Cover -->
<div class="cover-page">
  <div class="cover-badge">Kites Robotics Technical Documentation</div>
  <h1 class="cover-title">Encycle <span>Bank</span></h1>
  <div class="cover-subtitle">
    Autonomous Smart E-Waste Collection & Recycling Touchscreen Kiosk System.<br>
    Dedicated Raspberry Pi Architecture, Hardware Schematics, Operations & Feature Extensions.
  </div>

  <div class="cover-meta">
    <div>
      <strong>Organization:</strong> Kites Robotics — Sustainable Waste Tech
    </div>
    <div>
      <strong>Document Version:</strong> 3.0.0 (Raspberry Pi Edition)
    </div>
    <div>
      <strong>Compute Architecture:</strong> Raspberry Pi 4 / 5 Single Board Computer
    </div>
    <div>
      <strong>Date:</strong> October 2026
    </div>
  </div>
</div>

<div class="content-body">
{html_body}
</div>

</body>
</html>
"""

    print(f"[PDF Generator] Writing rendered HTML to {HTML_PATH} ...")
    HTML_PATH.write_text(full_html, encoding="utf-8")

    print(f"[PDF Generator] Invoking headless Edge from {EDGE_PATH} ...")
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_PATH}",
        "--no-pdf-header-footer",
        str(HTML_PATH)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[PDF Generator] Edge error: {result.stderr}")
        return False

    if os.path.exists(PDF_PATH):
        size_kb = os.path.getsize(PDF_PATH) / 1024.0
        print(f"[PDF Generator] SUCCESS! Generated clean PDF at: {PDF_PATH} ({size_kb:.1f} KB)")
        
        try:
            import shutil
            shutil.copyfile(PDF_PATH, EW_PDF_PATH)
            print(f"[PDF Generator] Copied clean PDF to: {EW_PDF_PATH}")
        except Exception as e:
            print(f"[PDF Generator] Copy error: {e}")
        return True
    else:
        print("[PDF Generator] PDF file not found after conversion!")
        return False

if __name__ == "__main__":
    success = build_pdf()
    sys.exit(0 if success else 1)
