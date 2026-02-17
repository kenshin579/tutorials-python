"""Hybrid Search (BM25 + 벡터) - 키워드 검색과 시맨틱 검색을 결합하여 검색 품질을 향상시킨다.

사용법:
    python 02_hybrid_search.py "연차휴가 일수"
    python 02_hybrid_search.py "쉬는 날은 며칠?"
"""

import sys

from langchain_classic.retrievers.ensemble import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

from shared import load_docs_as_chunks, load_vector_store


def print_results(title: str, docs):
    print(f"\n== {title} ==")
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "알 수 없음").split("/")[-1]
        preview = doc.page_content[:100].replace("\n", " ")
        print(f"  [{i}] {source}")
        print(f"      {preview}...")
    print()


def run(question: str):
    # 문서 청크 로드 (BM25용)
    chunks = load_docs_as_chunks()

    # 벡터 저장소 로드
    vector_store = load_vector_store()

    # ── 1. BM25 (키워드 검색) ──
    bm25_retriever = BM25Retriever.from_documents(chunks, k=3)
    bm25_results = bm25_retriever.invoke(question)

    # ── 2. 벡터 (시맨틱 검색) ──
    vector_retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    vector_results = vector_retriever.invoke(question)

    # ── 3. Hybrid (BM25 + 벡터) ──
    ensemble = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.4, 0.6],  # 키워드 40%, 시맨틱 60%
    )
    hybrid_results = ensemble.invoke(question)

    # ── 결과 출력 ──
    print(f"\n질문: {question}")
    print("=" * 60)

    print_results("BM25 (키워드) 검색 결과", bm25_results)
    print_results("벡터 (시맨틱) 검색 결과", vector_results)
    print_results("Hybrid (BM25 40% + 벡터 60%) 검색 결과", hybrid_results)

    # ── 비교 분석 ──
    bm25_contents = {doc.page_content[:50] for doc in bm25_results}
    vector_contents = {doc.page_content[:50] for doc in vector_results}
    only_bm25 = len(bm25_contents - vector_contents)
    only_vector = len(vector_contents - bm25_contents)
    overlap = len(bm25_contents & vector_contents)

    print("== 검색 결과 비교 ==")
    print(f"  BM25에서만 검색됨: {only_bm25}개")
    print(f"  벡터에서만 검색됨: {only_vector}개")
    print(f"  양쪽 모두 검색됨:  {overlap}개")
    print(f"  Hybrid 결과 총:    {len(hybrid_results)}개 (중복 제거)")


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "연차휴가 일수"
    run(q)
