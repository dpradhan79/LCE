from src.shared.content_reader.file_io.pdf_reader import PDFReader
from src.shared.content_reader.file_io.reader import Reader
from src.shared.utils.utils import Utility


def test_pdf_reader_single_file():
    pdf_folder_to_look_for = "docs"
    pdf_file_in_folder = "maths/arithmetic_progression.pdf"
    result_pdf_path = Utility.find_rel_path(pdf_folder_to_look_for, pdf_file_in_folder)
    reader: Reader = PDFReader(result_pdf_path)
    data = reader.read()
    assert data is not None, f'No Data Could Be Read From PDF File - {result_pdf_path}'
    assert len(data) > 0, f'PDF Reader Returns Empty From PDF File - {result_pdf_path}'


def test_pdf_multiple_files():
    pdf_folder_to_look_for = "docs"
    pdf_files = "maths"
    result_pdf_path = Utility.find_rel_path(pdf_folder_to_look_for, pdf_files)
    reader: Reader = PDFReader(result_pdf_path)
    data = reader.read()
    assert data is not None, f'No Data Could Be Read From PDF File - {result_pdf_path}'
    assert len(data) > 0, f'PDF Reader Returns Empty From PDF File - {result_pdf_path}'
