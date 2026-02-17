"""Re-ranking - 초기 검색 결과를 Cohere Rerank으로 재정렬하여 정밀도를 높인다.

사용법:
    python 03_reranking.py "임대차 보증금 반환"

환경 변수:
    COHERE_API_KEY - Cohere API 키 필요
"""

import sys

from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

from shared import load_vector_store


def run(question: str):
    vector_store = load_vector_store()

    # ── 1. 기본 검색 (넓게 10개) ──
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    base_results = base_retriever.invoke(question)

    # ── 2. Re-ranking (상위 3개로 압축) ──
    reranker = CohereRerank(model="rerank-v3.5", top_n=3)
    reranking_retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=base_retriever,
    )
    reranked_results = reranking_retriever.invoke(question)

    # ── 결과 출력 ──
    print(f"\n질문: {question}")
    print("=" * 60)

    print(f"\n== Re-ranking 전 (벡터 유사도 순, 상위 5개/{len(base_results)}개) ==")
    for i, doc in enumerate(base_results[:5], 1):
        source = doc.metadata.get("source", "알 수 없음").split("/")[-1]
        preview = doc.page_content[:80].replace("\n", " ")
        print(f"  [{i}] {source}")
        print(f"      {preview}...")

    print(f"\n== Re-ranking 후 (Cohere Rerank, 상위 {len(reranked_results)}개) ==")
    for i, doc in enumerate(reranked_results, 1):
        source = doc.metadata.get("source", "알 수 없음").split("/")[-1]
        relevance = doc.metadata.get("relevance_score", "N/A")
        preview = doc.page_content[:80].replace("\n", " ")
        print(f"  [{i}] {source} (relevance: {relevance})")
        print(f"      {preview}...")

    # ── 순위 변동 분석 ──
    print("\n== 순위 변동 분석 ==")
    base_order = [doc.page_content[:50] for doc in base_results]
    for i, doc in enumerate(reranked_results, 1):
        content_key = doc.page_content[:50]
        if content_key in base_order:
            original_rank = base_order.index(content_key) + 1
            change = original_rank - i
            arrow = "↑" if change > 0 else ("↓" if change < 0 else "→")
            print(f"  Rerank [{i}] ← 원래 [{original_rank}] {arrow} ({change:+d})")
        else:
            print(f"  Rerank [{i}] ← 새로 등장")


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "임대차 보증금 반환"
    run(q)
