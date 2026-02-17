"""Contextual Compression - 검색된 문서에서 질문과 관련 있는 부분만 추출하여 LLM에 전달한다.

사용법:
    python 05_context_compression.py "최저임금 위반 시 벌칙"
"""

import sys

from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from shared import get_llm, load_vector_store

PROMPT = ChatPromptTemplate.from_template(
    """다음 컨텍스트를 기반으로 질문에 답변하세요.
컨텍스트에 답이 없으면 "해당 정보를 찾을 수 없습니다"라고 답변하세요.

컨텍스트:
{context}

질문: {question}
답변:"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def run(question: str):
    vector_store = load_vector_store()
    llm = get_llm()

    # ── 1. 기본 검색 (압축 전) ──
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    base_results = base_retriever.invoke(question)
    base_context = format_docs(base_results)

    # ── 2. 압축 검색 ──
    compressor = LLMChainExtractor.from_llm(get_llm(model="gpt-4o-mini"))
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever,
    )
    compressed_results = compression_retriever.invoke(question)
    compressed_context = format_docs(compressed_results)

    # ── 3. 각각의 컨텍스트로 답변 생성 ──
    chain = PROMPT | llm | StrOutputParser()
    base_answer = chain.invoke({"context": base_context, "question": question})
    compressed_answer = chain.invoke(
        {"context": compressed_context, "question": question}
    )

    # ── 결과 출력 ──
    print(f"\n질문: {question}")
    print("=" * 60)

    print(f"\n== 압축 전 컨텍스트 ({len(base_context)}자, {len(base_results)}개 청크) ==")
    for i, doc in enumerate(base_results, 1):
        source = doc.metadata.get("source", "알 수 없음").split("/")[-1]
        preview = doc.page_content[:80].replace("\n", " ")
        print(f"  [{i}] {source}: {preview}...")

    print(f"\n== 압축 후 컨텍스트 ({len(compressed_context)}자, {len(compressed_results)}개 청크) ==")
    for i, doc in enumerate(compressed_results, 1):
        source = doc.metadata.get("source", "알 수 없음").split("/")[-1]
        preview = doc.page_content[:80].replace("\n", " ")
        print(f"  [{i}] {source}: {preview}...")

    # ── 비교 ──
    reduction = (
        (1 - len(compressed_context) / len(base_context)) * 100
        if base_context
        else 0
    )
    print(f"\n== 비교 ==")
    print(f"  압축 전: {len(base_context)}자")
    print(f"  압축 후: {len(compressed_context)}자")
    print(f"  토큰 절감: {reduction:.1f}%")

    print(f"\n== 압축 전 답변 ==")
    print(f"  {base_answer}")

    print(f"\n== 압축 후 답변 ==")
    print(f"  {compressed_answer}")


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "최저임금은 얼마인가요?"
    run(q)
