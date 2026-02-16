"""
최소 MVP RAG 챗봇 - 단일 파일로 동작하는 기본 RAG 예제

사용법:
    1. 의존성 설치: pip install -e .
    2. 환경 변수 설정: export OPENAI_API_KEY=your_api_key
    3. docs/ 디렉토리에 마크다운 문서 배치
    4. 인덱싱: python main.py index
    5. 질의: python main.py query "RAG란 무엇인가요?"
"""

import sys

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_DIR = "./chroma_db"
DOCS_DIR = "./docs"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# ── 1단계: 문서 인덱싱 ──────────────────────────────────
def index_documents():
    """문서를 로드 → 청킹 → 임베딩 → 벡터 저장소에 저장"""

    # 문서 로드
    loader = DirectoryLoader(DOCS_DIR, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    print(f"로드된 문서: {len(documents)}개")

    # 청킹
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"생성된 청크: {len(chunks)}개")

    # 벡터 저장소 생성
    Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)
    print("인덱싱 완료!")


# ── 2단계: 질의응답 ──────────────────────────────────────
def query(question: str):
    """질문을 받아 관련 문서를 검색하고 LLM으로 답변 생성"""

    # 벡터 저장소 로드 & 검색기 생성
    vector_store = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 프롬프트 템플릿
    prompt = ChatPromptTemplate.from_template(
        """다음 컨텍스트를 기반으로 질문에 답변하세요.
컨텍스트에 답이 없으면 "해당 정보를 찾을 수 없습니다"라고 답변하세요.

컨텍스트:
{context}

질문: {question}
답변:"""
    )

    # 검색된 문서를 텍스트로 결합
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # RAG 체인 구성 (LCEL)
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | ChatOpenAI(model="gpt-4o", temperature=0)
        | StrOutputParser()
    )

    answer = chain.invoke(question)
    print(f"\n질문: {question}")
    print(f"답변: {answer}")


# ── 실행 ─────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python main.py [index|query] [질문]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "index":
        index_documents()
    elif command == "query":
        question = sys.argv[2] if len(sys.argv) > 2 else "RAG란 무엇인가요?"
        query(question)
    else:
        print(f"알 수 없는 명령: {command}")
