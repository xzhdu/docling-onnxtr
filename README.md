# docling-onnxtr

Docling integration with the [OnnxTR](https://github.com/felixdittrich92/OnnxTR) OCR engine and [OpenCLIP](https://github.com/mlfoundations/open_clip) text embedding pipeline.

## Features

- **OnnxTR OCR Engine**: Leverages lightweight, high-performance ONNX Runtime models for text detection and recognition.
- **Automatic OCR Detection**: Automatically identifies pages or document regions that lack programmatic text layers and runs OCR on them.
- **Hybrid Semantic Chunking**: Uses Docling's `HybridChunker` to split documents into structured, contextual chunks respecting headings, paragraphs, and tables.
- **Vector Embeddings**: Generates multimodal vector embeddings for each text chunk using the `EmbeddingComponent` (OpenCLIP `xlm-roberta-base-ViT-B-32`).
- **Rich Metadata Export**: Exports chunks with comprehensive metadata ready for vector databases:
  - `file_id`: Document identifier / filename
  - `page_number` & `page_numbers`: Primary page and all spanned page numbers
  - `ocr_text`: Chunk text extracted via OCR
  - `is_ocr`: Flag indicating OCR provenance
  - `ocr_engine`: Name of the OCR engine (`OnnxTR`)
  - `embedding`: Vector representation (512-dim)
  - `embedding_metadata`: Model name, execution time, and timestamp

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

Process a document, chunk it, generate text embeddings, and export chunks to JSON:

```bash
# Convert, chunk, and embed a document (default output: <document_stem>.chunks.json)
python docling_onnxtr.py path/to/document.pdf

# Specify a custom output JSON file or output directory
python docling_onnxtr.py path/to/document.pdf output.json
python docling_onnxtr.py path/to/document_scan.jpg ./output_dir/
```

### Output JSON Format

The output JSON contains an array of chunk records:

```json
[
  {
    "chunk_id": 0,
    "file_id": "document.pdf",
    "page_number": 1,
    "page_numbers": [1],
    "ocr_text": "Sample extracted text from document...",
    "is_ocr": true,
    "ocr_engine": "OnnxTR",
    "embedding": [0.0123, -0.0456, ...],
    "embedding_metadata": {
      "file_name": "document.pdf",
      "model_name": "OpenCLIP xlm-roberta-base-ViT-B-32",
      "representation_type": "FixRes",
      "embedding_dim": 512,
      "execution_time_ms": 12.45,
      "timestamp": 1724581234.56
    }
  }
]
```

## Components

- [OpenCLIP Embedding Component](components/embedding/README.md) – Modular component for generating multimodal text and image embeddings.