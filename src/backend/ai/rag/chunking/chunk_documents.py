import re
from typing import List, Dict, Any

from src.shared.utils.utils import Utility


def chunk_page_document(
        page_doc: Dict[str, Any],
        chunk_size: int = 500,
        overlap: int = 50,
) -> List[Dict[str, Any]]:
    """
    Chunk a single PageDocument into overlapping, RAG-ready chunks.
    """

    text = page_doc["text"].strip()
    list_replace_noisy_words = [("MartHEMaTICS", "MATHEMATICS")]
    list_pop_noisy_words = ["1062CHOS", "Reprint 2025-26"]
    text = Utility.normalize_headers_footers(text, list_replace_noisy_words, list_pop_noisy_words)

    # 1. Split into paragraph-like units using blank lines
    paragraphs = [
        p.strip()
        for p in re.split(r"\n{2,}", text)
        if p.strip()
    ]

    chunks = []
    buffer = ""
    chunk_index = 0

    for para in paragraphs:
        # 2. If adding this paragraph stays within size, accumulate
        if len(buffer) + len(para) <= chunk_size:
            buffer += (" " + para if buffer else para)

        # 3. Otherwise flush current buffer as a chunk
        else:
            chunks.append(
                {
                    "id": f'{page_doc["id"]}_chunk_{chunk_index}',
                    "text": buffer.strip(),
                    "metadata": {
                        **page_doc["metadata"],
                        "chunk_index": chunk_index,
                    },
                }
            )

            chunk_index += 1

            # 4. Apply overlap: carry last N characters forward
            buffer = buffer[-overlap:] + " " + para

    # 5. Flush remaining buffer
    if buffer.strip():
        chunks.append(
            {
                "id": f'{page_doc["id"]}_chunk_{chunk_index}',
                "text": buffer.strip(),
                "metadata": {
                    **page_doc["metadata"],
                    "chunk_index": chunk_index,
                },
            }
        )

    return chunks


def chunk_documents(pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    all_chunks = []
    for page in pages:
        all_chunks.extend(chunk_page_document(page))
    return all_chunks
