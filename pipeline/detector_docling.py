"""
detector_docling.py
-----------
GOAL: Read one invoice PDF → save raw text to /output
Fast Track: Native Digital PDFs (PyMuPDF)
Backup Track: Scanned PDFs (Docling + Tesseract OCR)

RUN:
    python pipeline/detector_docling.py --pdf input/dummy.pdf --debug
"""
import os
import argparse
from pathlib import Path

import pymupdf4llm  # Added for the fast-track extraction
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractCliOcrOptions
from docling.datamodel.base_models import InputFormat


OUTPUT_FOLDER = "output"


def detector(pdf_path, debug=False):
    """
    Open the PDF and extract text.
    Attempts PyMuPDF first. If text is missing, falls back to Tesseract OCR.
    """
    # --- Step 1: The Fast Track (PyMuPDF) ---
    if debug:
        print("[DEBUG] Attempting digital extraction with PyMuPDF...")

    fast_text = pymupdf4llm.to_markdown(pdf_path)

    # Heuristic Gatekeeper: If text is found, return immediately and skip OCR
    if len(fast_text.strip()) >= 50:
        if debug:
            print("[DEBUG] Digital PDF text found. Bypassing OCR.")
        return fast_text

    # --- Step 2: The Backup Track (Docling + Tesseract) ---
    if debug:
        print("[DEBUG] Scanned image detected. Routing to Docling + Tesseract...")

    # Configure PDF pipeline
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True

    pipeline_options.ocr_options = TesseractCliOcrOptions(
        force_full_page_ocr=True, # Forces OCR because the gatekeeper confirmed it's an image
        lang=["spa", "eng"],
        tesseract_cmd=r"C:\Users\rohit\tesseract.exe"
    )

    # Initialize converter with the mapped pipeline
    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    result = converter.convert(pdf_path)
    text   = result.document.export_to_markdown()

    return text


def run():
    parser = argparse.ArgumentParser(description="Extract text from a PDF and save to output folder.")
    parser.add_argument('--pdf', required=True, help='Path to the PDF file to process')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    pdf_path = args.pdf

    if args.debug:
        print(f"[DEBUG] Reading : {pdf_path}")

    # Pass the debug flag down so the detector function can log its routing decisions
    raw_text = detector(pdf_path, debug=args.debug)

    # Save to /output using the same filename as the PDF
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_file = Path(OUTPUT_FOLDER) / f"{Path(pdf_path).stem}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(raw_text)

    print(f"Characters extracted : {len(raw_text)}")
    print(f"Saved to             : {output_file}")


if __name__ == "__main__":
    run()