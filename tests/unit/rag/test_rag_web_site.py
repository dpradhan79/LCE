import os

import bs4
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings

from src.backend.ai.llm.llm_factory.llm_factory import SupportedLLMs
from src.shared.consts import const_config
from src.shared.utils.utils import Utility


def test_rag_web_site_in_memory_sentence_transformer():
    web_url = "https://lilianweng.github.io/posts/2023-06-23-agent/"

    # models
    options = {
        "api_key": Utility.get_encrypted_key(
            os.getenv(const_config.ENV.AZURE.AZURE_OPENAI_API_KEY)),
        "base_url": os.getenv(const_config.ENV.AZURE.AZURE_OPENAI_ENDPOINT),
        "use_responses_api": True,
        # follows responses API leading multiple blocks in LLM O/P content for each type
        "reasoning": {"effort": "low", "summary": "auto"}  # reasoning not supported by gpt-4o series

    }
    llm = SupportedLLMs.get_chat_model(provider="openai", model="gpt-5.4-mini", **options)

    # Load Website
    from langchain_community.document_loaders import WebBaseLoader

    loader = WebBaseLoader(
        web_path=web_url,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        )

    )
    data = loader.load()

    # Chunking
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    chunker = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = chunker.split_documents(data)

    # Indexing/Embedding
    from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store: VectorStore = InMemoryVectorStore(embedding_model)
    doc_id_list = vector_store.add_documents(documents=chunks)

    # Retrieval
    query = "What are the key takeaways from Lilian's post on agents?"
    list_retrieved = vector_store.similarity_search_with_score(query=query, k=5)
    for retrieved_docs, similarity_score in list_retrieved:
        assert retrieved_docs.page_content is not None
        assert 0 < similarity_score < 1
        print(f"Similarity Score - {similarity_score} \n Retrieved chunk: {retrieved_docs.page_content}\n")


def test_rag_web_site_in_chrome_db():
    # web_url = "https://lilianweng.github.io/posts/2023-06-23-agent/"
    web_url_2 = "https://docs.langchain.com/oss/python/langchain/models"

    # Load Website
    from langchain_community.document_loaders import WebBaseLoader

    loader = WebBaseLoader(
        web_path=web_url_2,
        # bs_kwargs=dict(
        #     parse_only=bs4.SoupStrainer(
        #         class_=("post-content", "post-title", "post-header")
        #     )
        # )

    )
    data = loader.load()
    assert len(data) > 0
    assert len(data[0].page_content) > 0
    d_list = []
    for d in data:
        d.metadata.update(
            {"category": "langchain", "type": "models"})  # adding metadata to use as filter during retrieval
        d_list.append(d)
    data = d_list
    # Chunking
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    chunker = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = chunker.split_documents(data)

    # Indexing/Embedding
    from langchain_core.vectorstores import VectorStore
    from langchain_chroma import Chroma

    vector_store: VectorStore = Chroma(collection_name="langchain",
                                       embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
                                       persist_directory=const_config.PARENT_DIR / "chromadb")

    import hashlib

    def doc_id(doc):
        return hashlib.sha256(
            (doc.page_content + str(doc.metadata)).encode()
        ).hexdigest()

    vector_store.add_documents(chunks, ids=[doc_id(doc) for doc in chunks])

    retriever: VectorStoreRetriever = vector_store.as_retriever(search_kwargs={"k": 3, "filter": {"type": "models"}})

    # Retrieval
    query = "What are Parameters to models"
    query_response = retriever.con.invoke(query)
    assert query_response is not None
    for q_r in query_response:
        assert q_r.page_content is not None
        print(f"Retrieved chunk: {q_r.page_content}\n")

    list_response = vector_store.similarity_search_with_score(query=query, k=5, filter={"type": "models"})
    assert query_response is not None
    for q_r, score in list_response:
        assert q_r.page_content is not None
        assert 0 < score < 1.3, f'Score {score} is out of expected range [0,1.3]'
        print(f"Score - {score} \n Retrieved chunk: {q_r.page_content}\n")
