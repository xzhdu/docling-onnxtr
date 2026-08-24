from pathlib import Path
import sys
from typing import Optional, Union

from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import DoclingDocument
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


def process_document(
    input_path: Union[str, Path],
    output_json_path: Optional[Union[str, Path]] = None,
    force_full_page_ocr: bool = False,
) -> DoclingDocument:
    """
    Process a document with Docling using OnnxTR OCR and optionally save document model to JSON.

    The saved document model contains the full structured representation,
    including page numbers and bounding box coordinates for each text element.
    """
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Document not found: {input_file}")

    converter = create_document_converter(force_full_page_ocr=force_full_page_ocr)
    conv_res = converter.convert(input_file)
    doc: DoclingDocument = conv_res.document

    if output_json_path is not None:
        out_file = Path(output_json_path)
        if out_file.is_dir():
            out_file = out_file / f"{input_file.stem}.docling.json"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        doc.save_as_json(out_file)

    return doc


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python docling_onnxtr.py <path_to_document> [output_json_path]")
        return

    doc_path = Path(sys.argv[1])
    out_json_path = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else doc_path.with_name(f"{doc_path.stem}.docling.json")
    )

    print(f"Processing '{doc_path}' using OnnxTR OCR...")
    doc = process_document(doc_path, output_json_path=out_json_path)

    text_items_count = sum(
        1
        for item, _ in doc.iterate_items()
        if hasattr(item, "text") and item.text and getattr(item, "prov", None)
    )

    print(f"Successfully processed: {doc.name}")
    print(f"Total pages: {len(doc.pages)}")
    print(f"Extracted text items with bounding boxes: {text_items_count}")
    print(f"Saved document model to: {out_json_path}")


if __name__ == "__main__":
    main()
