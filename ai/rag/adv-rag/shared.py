"""공통 유틸리티 - 임베딩, 벡터 저장소, 문서 로딩"""

import os
import sys

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")

API_KEY = os.environ.get("TUTORIAL_PYTHON_OPEN_API_KEY", "")

# RAGAS 등 OPENAI_API_KEY 환경 변수를 직접 읽는 라이브러리를 위해 설정
if API_KEY:
    os.environ["OPENAI_API_KEY"] = API_KEY


def get_embeddings():
    """OpenAI 임베딩 인스턴스 반환"""
    return OpenAIEmbeddings(model="text-embedding-3-small", api_key=API_KEY)


def get_llm(model: str = "gpt-4o", temperature: float = 0):
    """ChatOpenAI 인스턴스 반환"""
    return ChatOpenAI(model=model, temperature=temperature, api_key=API_KEY)


def load_vector_store():
    """ChromaDB 벡터 저장소 로드"""
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=get_embeddings())


def load_docs_as_chunks(chunk_size: int = 500, chunk_overlap: int = 50):
    """문서 로드 + 청킹 결과 반환"""
    loader = DirectoryLoader(DOCS_DIR, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(documents)


def index_documents():
    """docs/ 문서를 인덱싱하여 ChromaDB에 저장"""
    chunks = load_docs_as_chunks()
    print(f"로드된 청크: {len(chunks)}개")
    Chroma.from_documents(chunks, get_embeddings(), persist_directory=CHROMA_DIR)
    print("인덱싱 완료!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "index":
        index_documents()
    else:
        print("사용법: python shared.py index")
