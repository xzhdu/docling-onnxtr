# docling-onnxtr

Docling integration with the [OnnxTR](https://github.com/felixdittrich92/OnnxTR) OCR engine via the [docling-OCR-OnnxTR](https://github.com/felixdittrich92/docling-OCR-OnnxTR) plugin.

## Features

- **OnnxTR OCR Engine**: Leverages lightweight, high-performance ONNX Runtime models for text detection and recognition.
- **Automatic OCR Detection**: Automatically identifies pages or document regions that lack programmatic text layers and runs OCR on them.
- **Format Support**: Processes both PDF documents and standalone image scans (`.jpg`, `.png`, `.tiff`, etc.).
- **Document Model Export**: Saves structured `DoclingDocument` JSON representation preserving:
  - Extracted text elements
  - Page numbers (`prov[].page_no`)
  - Bounding box coordinates (`prov[].bbox`)

## Installation

1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

*(For GPU acceleration, install `docling-ocr-onnxtr[gpu]` instead).*

## Usage

### Command Line Interface (CLI)

Convert a document and export its document model to a JSON file:

```bash
# Convert a document (default output: <document_stem>.docling.json)
python docling_onnxtr.py path/to/document.pdf

# Specify a custom output JSON file or output directory
python docling_onnxtr.py path/to/document.pdf output.json
python docling_onnxtr.py path/to/document_scan.jpg ./output_dir/
```