# OCR Image Search

A Python tool for processing images with OCR and searching through them based on text content.

## Features

- Support for PNG, JPEG, BMP, and TIFF formats
- Regex search support

## Requirements

- Python 3.6+
- Tesseract OCR
- Python packages: Pillow, pytesseract

## Installation

1. Install Tesseract OCR:
   - Windows: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```
### OCR Configuration
```py
processor = OCRProcessor(
    input_dir="./input",
    output_dir="./output",
    tesseract_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

```
