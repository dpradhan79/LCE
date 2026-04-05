from os import PathLike
from typing import Union

from pypdf import PdfReader
from typing_extensions import override

from src.shared.content_reader.file_io.reader import Reader


class PDFReader(Reader):
    def __init__(self, file_path_pdf: Union[str, PathLike], use_logging=True):
        super().__init__(file_path_pdf, use_logging)

    @override
    def read(self) -> str:
        reader = PdfReader(self.file_path)
        all_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
        return "\n".join(all_text)
