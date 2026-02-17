"""Multi-query Retrieval - LLM이 질문을 여러 관점으로 변형하여 검색 범위를 넓힌다.

사용법:
    python 04_multi_query_retrieval.py "퇴직금 받을 수 있는 조건"
"""

import logging
import sys

from langchain_classic.retrievers.multi_query import MultiQueryRetriever

from shared import get_llm, load_vector_store

# MultiQueryRetriever가 생성한 변형 질문을 로그로 출력
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)


def run(question: str):
    vector_store = load_vector_store()
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()

    # ── 1. 단일 질문 검색 ──
    single_results = base_retriever.invoke(question)

    # ── 2. Multi-query 검색 ──
    multi_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm,
    )
    multi_results = multi_retriever.invoke(question)

    # ── 결과 출력 ──
    print(f"\n질문: {question}")
    print("=" * 60)

    print(f"\n== 단일 질문 검색 결과 ({len(single_results)}개) ==")
    for i, doc in enumerate(single_results, 1):
        source = doc.metadata.get("source", "알 수 없음").split("/")[-1]
        preview = doc.page_content[:100].replace("\n", " ")
        print(f"  [{i}] {source}")
        print(f"      {preview}...")

    print(f"\n== Multi-query 검색 결과 (중복 제거 후 {len(multi_results)}개) ==")
    for i, doc in enumerate(multi_results, 1):
        source = doc.metadata.get("source", "알 수 없음").split("/")[-1]
        preview = doc.page_content[:100].replace("\n", " ")
        print(f"  [{i}] {source}")
        print(f"      {preview}...")

    # ── 비교 분석 ──
    single_contents = {doc.page_content[:50] for doc in single_results}
    multi_contents = {doc.page_content[:50] for doc in multi_results}
    new_docs = len(multi_contents - single_contents)

    print(f"\n== 비교 ==")
    print(f"  단일 검색: {len(single_results)}개")
    print(f"  Multi-query: {len(multi_results)}개")
    print(f"  추가로 발견된 문서: {new_docs}개")


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "퇴직금 받을 수 있는 조건"
    run(q)
