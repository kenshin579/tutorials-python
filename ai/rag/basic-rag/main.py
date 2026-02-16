"""
기본 RAG 챗봇 - 출처 표시 + 대화형 루프를 지원하는 RAG 예제

사용법:
    1. 의존성 설치: pip install -e .
    2. 환경 변수 설정: export OPENAI_API_KEY=your_api_key
    3. docs/ 디렉토리에 마크다운 문서 배치
    4. 인덱싱: python main.py index
    5. 단일 질의: python main.py query "청약철회 기간은?"
    6. 대화 모드: python main.py chat
"""

import os
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


# ── 2단계: 유사도 검색 + 출처 표시 ────────────────────────
def retrieve_with_sources(vector_store, question: str, k: int = 3):
    """유사도 점수와 함께 관련 문서를 검색하고 출처 정보를 반환"""
    results = vector_store.similarity_search_with_relevance_scores(question, k=k)

    sources = []
    for doc, score in results:
        source_file = os.path.basename(doc.metadata.get("source", "알 수 없음"))
        sources.append(
            {
                "file": source_file,
                "score": score,
                "preview": doc.page_content[:80] + "...",
            }
        )
    return results, sources


def format_docs(docs_with_scores):
    """검색 결과를 컨텍스트 문자열로 변환"""
    return "\n\n".join(doc.page_content for doc, _score in docs_with_scores)


def print_sources(sources):
    """출처 정보를 포맷팅하여 출력"""
    print("\n📚 참조 문서:")
    for i, src in enumerate(sources, 1):
        print(f"  [{i}] {src['file']} (유사도: {src['score']:.3f})")
        print(f"      {src['preview']}")


# ── 3단계: 질의응답 ──────────────────────────────────────
def build_chain(vector_store):
    """RAG 체인을 구성하여 반환"""

    prompt = ChatPromptTemplate.from_template(
        """다음 컨텍스트를 기반으로 질문에 답변하세요.
컨텍스트에 답이 없으면 "해당 정보를 찾을 수 없습니다"라고 답변하세요.

컨텍스트:
{context}

질문: {question}
답변:"""
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    chain = (
        {"context": retriever | format_docs_simple, "question": RunnablePassthrough()}
        | prompt
        | ChatOpenAI(model="gpt-4o", temperature=0)
        | StrOutputParser()
    )
    return chain


def format_docs_simple(docs):
    """retriever용 포맷 함수 (점수 없이 Document 리스트)"""
    return "\n\n".join(doc.page_content for doc in docs)


def query(question: str):
    """단일 질문에 대해 답변 생성 + 출처 표시"""

    vector_store = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

    # 출처 정보가 포함된 검색
    results, sources = retrieve_with_sources(vector_store, question)

    # 체인으로 답변 생성
    chain = build_chain(vector_store)
    answer = chain.invoke(question)

    print(f"\n💬 질문: {question}")
    print(f"\n🤖 답변: {answer}")
    print_sources(sources)


# ── 4단계: 대화형 루프 ───────────────────────────────────
def chat():
    """대화형 모드 - 반복적으로 질문하고 답변을 받을 수 있다"""

    vector_store = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    chain = build_chain(vector_store)

    print("=" * 50)
    print("RAG 챗봇 대화 모드")
    print("종료: quit 또는 exit 입력")
    print("=" * 50)

    while True:
        try:
            question = input("\n❓ 질문: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n대화를 종료합니다.")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("대화를 종료합니다.")
            break

        # 출처 포함 검색
        results, sources = retrieve_with_sources(vector_store, question)

        # 답변 생성
        answer = chain.invoke(question)

        print(f"\n🤖 답변: {answer}")
        print_sources(sources)


# ── 실행 ─────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python main.py [index|query|chat]")
        print("  index         - docs/ 디렉토리의 문서를 인덱싱")
        print("  query <질문>  - 단일 질문에 답변")
        print("  chat          - 대화형 모드 시작")
        sys.exit(1)

    command = sys.argv[1]
    if command == "index":
        index_documents()
    elif command == "query":
        question = sys.argv[2] if len(sys.argv) > 2 else "청약철회 기간은?"
        query(question)
    elif command == "chat":
        chat()
    else:
        print(f"알 수 없는 명령: {command}")
