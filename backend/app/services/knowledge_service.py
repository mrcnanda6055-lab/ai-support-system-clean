from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

# Simple in-memory vector store (upgrade to DB later)
_embeddings = OpenAIEmbeddings()
_vector_store = None

def load_knowledge(docs: list[str]):
    global _vector_store
    _vector_store = FAISS.from_texts(docs, _embeddings)

def search_knowledge(query: str, k: int = 3):
    if not _vector_store:
        return []
    results = _vector_store.similarity_search(query, k=k)
    return [r.page_content for r in results]
