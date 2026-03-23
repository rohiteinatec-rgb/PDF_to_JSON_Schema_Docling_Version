# 🧠 PDF to JSON Schema: AI Extraction Pipeline (Docling Version)

An enterprise-grade, AI-driven extraction pipeline designed to handle the most difficult documents: **Scanned Invoices, Image-based PDFs, and Complex Layouts.** Unlike standard OCR engines that simply read text left-to-right, this pipeline uses **IBM's Docling** (DocLayNet) to semantically understand the document's structure, perfectly reconstructing tables and reading text from photographs before normalizing it into Markdown for JSON parsing.

## 🛡️ Enterprise Defenses (The Gatekeeper)

Before the heavy AI models are loaded into memory, the document must pass a strict defensive gauntlet:
1. **Resource Exhaustion Protection (DoS):** Hardcoded `MAX_PAGES` limit to prevent malicious or glitched PDFs from spiking server RAM.
2. **Security & Integrity Checks:** Automatically catches corrupted files and password-protected/encrypted PDFs upfront to prevent infinite pipeline hangs.
3. **Memory-Safe Execution:** Wraps all C-binding PyMuPDF operations in Python context managers to guarantee memory release, even during fatal errors.

## 🚀 Smart AI Routing Architecture

Once the document is validated, the pipeline dynamically analyzes the page geometry to apply the most efficient extraction method:

* **Track A: Digital PDF (Fast Track)**
  If the page contains native digital text, the pipeline bypasses the heavy OCR vision models. It runs Docling with `OCR=False` to instantly map the table layouts using purely digital data, keeping processing times under 1 second.
* **Track B: Scanned/Image PDF (Deep Learning Track)**
  If the page is an image or a photograph converted to a PDF, the pipeline spins up Docling's PyTorch-based vision models (`OCR=True`) to visually read the document, reconstruct the invisible gridlines, and output structured Markdown.

## 📋 Prerequisites & Installation

Ensure your system has **Python 3.8+** installed. *(Note: Unlike older OCR pipelines, this version does NOT require Docker).*

Install the required extraction and AI libraries:
bash
pip install docling PyMuPDF

🛠️ Usage Workflow

1. Extract the PDF to Markdown
Run the detector script to validate the PDF and extract layout-aware text.
Bash
python pipeline/detector_docling.py --pdf input/scanned_invoice.pdf --debug

2. Parse the Markdown to JSON
Pass the resulting text file into the parser to generate the final JSON schema.

Bash
python pipeline/parser_json.py --input output/scanned_invoice.txt --debug


## 📂 Project Structure

PDF_to_JSON_Schema_Docling/
├── input/                  # Place your complex/scanned PDF files here
├── output/                 # Extracted Markdown and final JSON files are saved here
├── pipeline/
│   ├── detector_docling.py # Main enterprise script for AI extraction
│   └── parser_json.py      # Script to convert Markdown tables to JSON
└── README.md

## 📄 License
Einatec License

## ✍️ Author
Einatec Team / Rohit


### Key Upgrades from your old README:
1. **Removed Docker:** Docling runs strictly in Python, so I removed the Docker prerequisite to save future developers from confusion.
2. **Updated the Routing Logic:** Explained how the new script uses Docling's `OCR=False` for fast-tracking digital files and `OCR=True` for heavy image lifting.
3. **Carried over the Defenses:** The README sets the expectation that this isn't just a script, it's a secure backend ingestion layer.

Whenever you have this pushed to your new repository, let me know! We can immediately dive into writing the `detector_docling.py` code with our enterprise defenses perfectly integrated.