📄 Hybrid PDF Extraction Pipeline
A high-performance, locally hosted Python pipeline for extracting structured text and tables from invoices. This architecture utilizes a two-tier routing system to process native digital PDFs in milliseconds while dynamically falling back to heavily optimized Tesseract OCR for scanned images.

🚀 Core Architecture
This pipeline is designed around a Heuristic Gatekeeper to minimize CPU/RAM overhead and prevent unnecessary deep-learning model allocation.

Tier 1: The Fast Track (pymupdf4llm)

Reads native C-structures and binary streams of digital PDFs.

Bypasses visual rendering and OCR entirely.

Execution time: < 0.2 seconds.

Tier 2: The Backup Track (Docling + Tesseract)

Triggered only if Tier 1 yields < 50 characters (confirming a flat image).

Uses a locally hosted Tesseract binary.

Specifically configured with spa (Spanish) language weights to perfectly capture Euro (€) symbols, European decimal commas (1.850,00), and accented characters (ñ, á).

🛠️ Prerequisites & Setup
1. Python Dependencies
   Install the required libraries via pip:

Bash
pip install pymupdf4llm docling
2. Tesseract OCR (Windows)
   Because Docling integrates directly with the C++ binary, you must install Tesseract locally.

Download the 64-bit Windows installer.

During installation, expand Additional language data (download) and check Spanish.

Locate the tesseract.exe file (e.g., C:\Users\username\tesseract.exe or C:\Program Files\Tesseract-OCR\tesseract.exe).

Update the tesseract_cmd path in the Python script to match your installation.

💻 Usage
Run the extraction script via the command line. Use the --debug flag to see the real-time routing decisions made by the Gatekeeper.

Bash
# Process a native digital PDF (Routes to Tier 1)
python detector_docling.py --pdf input/digital_invoice.pdf --debug

# Process a scanned image (Routes to Tier 2)
python detector_docling.py --pdf input/scanned_invoice.pdf --debug
Expected Output
The script saves the extracted Markdown structure to the /output folder, preserving complex table alignments, empty cells (_—), and localized currency symbols, ready for strict JSON mapping.

Plaintext
[DEBUG] Reading : input/scanned_invoice.pdf
[DEBUG] Attempting digital extraction with PyMuPDF...
[DEBUG] Scanned image detected. Routing to Docling + Tesseract...
Characters extracted : 1411
Saved to             : output/scanned_invoice.txt