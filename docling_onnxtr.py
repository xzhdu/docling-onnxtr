from pathlib import Path
import sys

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    DocumentConverter,
    ImageFormatOption,
    PdfFormatOption,
)
from docling_ocr_onnxtr import OnnxtrOcrOptions


def create_document_converter(
    force_full_page_ocr: bool = False,
) -> DocumentConverter:
    """Create and configure a Docling DocumentConverter using the OnnxTR OCR engine."""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.allow_external_plugins = True
    pipeline_options.ocr_options = OnnxtrOcrOptions(
        force_full_page_ocr=force_full_page_ocr
    )

    format_options = {
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
        InputFormat.IMAGE: ImageFormatOption(pipeline_options=pipeline_options),
    }

    return DocumentConverter(format_options=format_options)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python docling_onnxtr.py <path_to_document>")
        return

    doc_path = Path(sys.argv[1])
    if not doc_path.exists():
        print(f"Error: File not found at '{doc_path}'")
        sys.exit(1)

    print(f"Initializing converter and processing: {doc_path}...")
    converter = create_document_converter()
    conv_res = converter.convert(doc_path)
    print(f"Successfully converted document: {conv_res.document.name}")
    print(f"Pages: {len(conv_res.document.pages)}")


if __name__ == "__main__":
    main()
