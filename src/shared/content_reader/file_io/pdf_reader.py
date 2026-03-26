import json
from os import PathLike
from pathlib import Path
from typing import Union, Any

from pypdf import PdfReader
from typing_extensions import override

from src.shared.content_reader.file_io.reader import Reader


class PDFReader(Reader):
    def __init__(self, file_path_pdf: Union[str, PathLike], use_logging=True):
        super().__init__(file_path_pdf, use_logging)

    @override
    def read(self) -> dict[str, Any]:
        all_text_dict = {}
        if self.file_path.is_file():

            if self.logger:
                self.logger.debug(f'PDF File being read - {self.file_path}')
            pdf_reader = PdfReader(self.file_path)
            for page_number, page in enumerate(pdf_reader.pages, start=1):
                text = page.extract_text()
                if text:
                    all_text_dict[f'{self.file_path.stem}_{page_number}'] = text

        elif self.file_path.is_dir():
            if self.logger:
                self.logger.debug(f'PDF File being read - {self.file_path}')
            files = list(Path(self.file_path).glob("*.pdf"))
            for file in files:

                pdf_reader = PdfReader(file)
                for page_number, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text:
                        all_text_dict[f'{file.stem}_{page_number}'] = text

            if self.logger:
                self.logger.debug(
                    f'Text Retrieved from path - {self.file_path} - {json.dumps(all_text_dict, indent=2)}')

        return all_text_dict
