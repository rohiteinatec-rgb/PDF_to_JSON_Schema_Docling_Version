"""
detector.py
-----------
GOAL: Read one invoice PDF → save raw text to /output

RUN:
    python pipeline/detector.py --pdf input/digital_invoice_test.pdf
    python pipeline/detector.py --pdf input/dummy.pdf
"""

import fitz              # PyMuPDF
import os
import argparse
from pathlib import Path


OUTPUT_FOLDER = "output"


def detector(pdf_path):
    """
    Open the PDF and extract whatever text PyMuPDF finds on page 1.

    Digital PDF → returns full invoice text
    Scanned PDF → returns little or nothing (page is just an image)
    """

    doc  = fitz.open(pdf_path)
    text = doc[0].get_text()   # page 1 only — invoice is always 1 page
    doc.close()

    return text


def run():
    parser = argparse.ArgumentParser(description="Extract text from a PDF and save to output folder.")
    parser.add_argument('--pdf', required=True, help='Path to the PDF file to process')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    pdf_path = args.pdf

    if args.debug:
        print(f"[DEBUG] Reading : {pdf_path}")

    raw_text = detector(pdf_path)

    # Save to /output using the same filename as the PDF
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_file = Path(OUTPUT_FOLDER) / f"{Path(pdf_path).stem}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(raw_text)

    print(f"Characters extracted : {len(raw_text)}")
    print(f"Saved to             : {output_file}")


if __name__ == "__main__":
    run()