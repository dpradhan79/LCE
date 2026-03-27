import json
from os import PathLike
from pathlib import Path
from typing import Union, Any, Dict, List, Literal

import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfReader
from typing_extensions import override

from src.shared.content_reader.file_io.reader import Reader
from src.shared.utils.utils import Utility

PDF_PROCESSOR = Literal["pypdf", "pdfplumber", "pdf2image;pytesseract"]


class PDFReader(Reader):
    """
    Reads PDF files (single file or folder of PDFs) and
    emits page-level documents with rich metadata.
    """

    def __init__(
            self,
            file_path_pdf: Union[str, PathLike],
            pdf_processor: PDF_PROCESSOR = "pdfplumber",
            use_logging: bool = True,
    ):
        super().__init__(file_path_pdf, use_logging)
        self.pdf_processor = pdf_processor

    @override
    def read(self) -> List[Dict[str, Any]]:
        documents: List[Dict[str, Any]] = []

        if self.logger:
            self.logger.debug(f"PDF processor selected: {self.pdf_processor}")
            self.logger.debug(f"PDF path: {self.file_path}")

        if self.file_path.is_file():
            documents.extend(self._read_single_pdf(self.file_path))

        elif self.file_path.is_dir():
            pdf_files = list(self.file_path.glob("*.pdf"))
            for pdf_file in pdf_files:
                documents.extend(self._read_single_pdf(pdf_file))

        if self.logger:
            self.logger.debug(
                f"PDF extraction completed. Total documents: {len(documents)}"
            )
            self.logger.debug(f'Documents - \n {json.dumps(documents, indent=2)}')
        return documents

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _read_single_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        if self.logger:
            self.logger.debug(f"Reading PDF file: {pdf_path}")

        if self.pdf_processor == "pypdf":
            return self._read_with_pypdf(pdf_path)

        if self.pdf_processor == "pdfplumber":
            return self._read_with_pdfplumber(pdf_path)

        if self.pdf_processor == "pdf2image;pytesseract":
            return self._read_with_pdf2image_pytesseract(pdf_path)

        raise ValueError(f"Unsupported pdf processor: {self.pdf_processor}")

    def _read_with_pypdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        documents: List[Dict[str, Any]] = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            documents.append(
                self._build_document(
                    pdf_path=pdf_path,
                    page_number=page_number,
                    total_pages=total_pages,
                    text=text,
                    width=float(page.mediabox.width),
                    height=float(page.mediabox.height),
                    rotation=page.get("/Rotate", 0),
                )
            )

        return documents

    def _read_with_pdfplumber(self, pdf_path: Path) -> List[Dict[str, Any]]:
        documents: List[Dict[str, Any]] = []

        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)

            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text(x_tolerance=2, y_tolerance=2)
                if not text:
                    continue

                documents.append(
                    self._build_document(
                        pdf_path=pdf_path,
                        page_number=page_number,
                        total_pages=total_pages,
                        text=text,
                        width=page.width,
                        height=page.height,
                        rotation=0,
                    )
                )

        return documents

    def _build_document(
            self,
            pdf_path: Path,
            page_number: int,
            total_pages: int,
            text: str,
            width: float | None,
            height: float | None,
            rotation: int,
    ) -> Dict[str, Any]:
        inferred_title = Utility.infer_title(text)

        return {
            "id": f"{pdf_path.stem}::page::{page_number}",
            "text": text,
            "metadata": {
                "source_file": pdf_path.name,
                "source_path": str(pdf_path.parent),
                "page_number": page_number,
                "total_pages": total_pages,
                "pdf_processor": self.pdf_processor,
                "page_width": width,
                "page_height": height,
                "rotation": rotation,
                "inferred_title": inferred_title,
                "content_type": "text",
            },
        }

    def _read_with_pdf2image_pytesseract(self, pdf_path: Path) -> List[Dict[str, Any]]:
        poppler_path = Utility.find_rel_path("tools", "bin")
        tesseract_path = Utility.find_rel_path("tools", "tesseract/tesseract.exe")
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

        page_images = convert_from_path(self.file_path, poppler_path=poppler_path)

        total_pages = len(page_images)
        documents: List[Dict[str, Any]] = []

        for page_number, page in enumerate(page_images, start=1):
            text = pytesseract.image_to_string(page)
            if not text:
                continue
            width, height = page.size
            documents.append(
                self._build_document(
                    pdf_path=pdf_path,
                    page_number=page_number,
                    total_pages=total_pages,
                    text=text,
                    width=float(width),
                    height=float(height),
                    rotation=0),
            )

            return documents
