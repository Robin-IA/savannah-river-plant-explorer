"""Make the downloadable PDF of the whole story.

Run after build/build.py, which writes story-print.html:

    python build/make_pdf.py

Needs Playwright with Chromium (see requirements-pdf.txt):

    pip install -r requirements-pdf.txt
    python -m playwright install chromium
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "story-print.html"
OUT = ROOT / "atomic-history-savannah-river-plant.pdf"

FOOTER = ('<div style="font: 8px Helvetica, Arial, sans-serif; color: #57595c; width: 100%; '
          'text-align: center;">Atomic History: The Savannah River Plant · '
          '<span class="pageNumber"></span> of <span class="totalPages"></span></div>')


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(SOURCE.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(path=str(OUT), format="Letter", print_background=True,
                 display_header_footer=True, header_template="<div></div>", footer_template=FOOTER,
                 margin={"top": "0.7in", "bottom": "0.8in", "left": "0.7in", "right": "0.7in"},
                 outline=True, tagged=True)
        browser.close()
    print("wrote", OUT.name, round(OUT.stat().st_size / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
