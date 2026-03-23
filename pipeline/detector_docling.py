"""
detector_docling.py
-----------
GOAL: Smart extraction pipeline for PDFs.
Router: Quantrium Tech approach (Text Area vs Image Area via PyMuPDF).
Track A (Digital): Native extraction via PyMuPDF4LLM.
Track B (Scanned): Layout-aware OCR via Docling + EasyOCR.

RUN:
    python pipeline/detector_docling.py --pdf input/dummy.pdf --debug
"""
import os
import argparse
import fitz  # PyMuPDF
import pdfplumber
from pathlib import Path

import pymupdf4llm
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling.datamodel.base_models import InputFormat

OUTPUT_FOLDER = "output"


def is_text_based_pdf(pdf_path, debug=False):
    """
    Quantrium Tech Approach:
    Classifies a PDF by calculating the geometric area of text blocks vs image blocks.
    """
    doc = fitz.open(pdf_path)
    page = doc[0]
    image_area = 0.0
    text_area = 0.0

    for b in page.get_text("blocks"):
        block_type = b[6]
        r = fitz.Rect(b[:4])

        if block_type == 1:
            image_area += abs(r)
        elif block_type == 0:
            text_area += abs(r)

    doc.close()

    if debug:
        print(f"[DEBUG] Geometry Check -> Text Area: {text_area:.2f} | Image Area: {image_area:.2f}")

    return text_area > image_area

def is_extraction_poor(text):
    """
    Simple, stable condition to decide if we need to escalate to the next Tier.
    Avoids complex math, checks for obvious failures.
    """
    if not text:
        return True

    # Check 1: Is it suspiciously short? (e.g., PyMuPDF only saw a header)
    if len(text.strip()) < 50:
        return True

    # Check 2: Did the font encoding fail? (Common PyMuPDF error)
    if "(cid:" in text:
        return True

    return False


def extract_with_pdfplumber(pdf_path, debug=False):
    """Tier 2: Alternative digital extraction using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        if debug: print(f"[DEBUG] pdfplumber failed: {e}")
        return ""


def extract_with_docling(pdf_path, lang_list, use_ocr=True):
    """Tier 3 & Track B: Shared Docling engine."""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_table_structure = True
    pipeline_options.do_ocr = use_ocr

    if use_ocr:
        pipeline_options.ocr_options = EasyOcrOptions(
            force_full_page_ocr=True,
            lang=lang_list
        )

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )

    result = converter.convert(pdf_path)
    return result.document.export_to_markdown()

def detector(pdf_path, lang_list, debug=False):
    """
    Routes the PDF to the appropriate extraction engine based on page geometry.
    """
    if debug:
        print("[DEBUG] Analyzing PDF geometry to route extraction...")

    is_digital = is_text_based_pdf(pdf_path, debug=debug)

    if is_digital:
        # ==========================================
        # TRACK A: DIGITAL PIPELINE (3-Tier Flow)
        # ==========================================
        if debug: print("[DEBUG] Digital PDF detected. Starting Track A...")

        # TIER 1: Fast native extraction
        if debug: print("[DEBUG] -> Running Tier 1 (PyMuPDF4LLM)")
        text = pymupdf4llm.to_markdown(pdf_path)

        # Evaluate Tier 1
        if is_extraction_poor(text):
            if debug: print("[DEBUG] Tier 1 extraction poor/corrupted. Escalating...")

            # TIER 2: pdfplumber fallback
            if debug: print("[DEBUG] -> Running Tier 2 (pdfplumber)")
            text = extract_with_pdfplumber(pdf_path, debug)

            # Evaluate Tier 2
            if is_extraction_poor(text):
                if debug: print("[DEBUG] Tier 2 extraction poor/corrupted. Escalating...")

                # TIER 3: Docling Digital layout extraction
                if debug: print("[DEBUG] -> Running Tier 3 (Docling Digital, OCR=False)")
                text = extract_with_docling(pdf_path, lang_list, use_ocr=False)

        # This return must be here to catch successful Tier 1, 2, or 3 extractions
        return text

    else:
        # ==========================================
        # TRACK B: SCANNED PIPELINE
        # ==========================================
        if debug:
            print(f"[DEBUG] Scanned image detected. Routing to Docling + EasyOCR with languages: {lang_list}...")

        # BUG 2 FIXED: Use the clean helper function instead of repeating 15 lines of code
        return extract_with_docling(pdf_path, lang_list, use_ocr=True)

def run():
    parser = argparse.ArgumentParser(description="Extract text from a PDF and save to output folder.")
    parser.add_argument('--pdf', required=True, help='Path to the PDF file to process')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--lang', default='es+en', help='Language codes separated by a plus (e.g., es+en)')

    args = parser.parse_args()
    lang_list = args.lang.split('+')

    pdf_path = args.pdf

    if args.debug:
        print(f"[DEBUG] Reading : {pdf_path}")

    raw_text = detector(pdf_path, lang_list=lang_list, debug=args.debug)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_file = Path(OUTPUT_FOLDER) / f"{Path(pdf_path).stem}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(raw_text)

    print(f"Characters extracted : {len(raw_text)}")
    print(f"Saved to             : {output_file}")


if __name__ == "__main__":
    run()