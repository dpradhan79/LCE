from src.backend.ai.rag.chunking.chunk_documents import chunk_documents
from src.backend.ai.rag.vector_store.in_memory_faiss import InMemoryFAISS
from src.shared.content_reader.file_io.pdf_reader import PDFReader
from src.shared.content_reader.file_io.reader import Reader
from src.shared.utils.utils import Utility


def test_in_memory_faiss():
    # Step 1: PageDocuments come from your PDF ingestion pipeline
    pdf_folder_to_look_for = "docs"
    pdf_file_in_folder = "maths/arithmetic_progression.pdf"
    result_pdf_path = Utility.find_rel_path(pdf_folder_to_look_for, pdf_file_in_folder)
    reader: Reader = PDFReader(result_pdf_path, pdf_processor="pdfplumber")
    data = reader.read()
    page_documents = data  # your PDFReader output

    # Step 2: Chunking
    chunks = chunk_documents(page_documents)

    # Step 3: Build FAISS index
    faiss_store = InMemoryFAISS()
    faiss_store.build_index(chunks)

    # Step 4: Retrieval
    query = "Give an example on Arithmetic Progression on salary increment"
    retrieved_chunks = faiss_store.query(query, top_k=4)

    for c in retrieved_chunks:
        print(
            f'Page {c["metadata"]["page_number"]} | Chunk {c["metadata"]["chunk_index"]}\n'
            f'{c["text"]}\n'
        )
