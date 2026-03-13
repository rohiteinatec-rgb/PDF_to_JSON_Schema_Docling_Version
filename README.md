# PDF_to_JSON_Schema

This project extracts raw text from invoice PDFs and saves it as plain text files. The goal is to facilitate further processing, such as converting the extracted data into structured JSON schemas for automation and analysis.

## Features
- Extracts text from digital and scanned PDFs (using PyMuPDF)
- Saves output as .txt files in the output directory
- Command-line interface with debug mode

## Usage

1. Install dependencies (recommended: use a virtual environment):
   ```
   pip install pymupdf
   ```

2. Run the detector script:
   ```
   python pipeline/detector.py --pdf input/your_invoice.pdf --debug
   ```
   - `--pdf`: Path to the PDF file to process
   - `--debug`: (Optional) Enable debug output

3. Output will be saved in the `output/` directory with the same name as the PDF file.

## Project Structure
- `pipeline/detector.py`: Main script for PDF text extraction
- `input/`: Place your PDF files here
- `output/`: Extracted text files are saved here

## Example
See `pipeline/output/digital_invoice_test.txt` for a sample output.

## License
MIT License

## Author
Your Name

