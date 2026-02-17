"""RAGAS 자동 평가 - RAG 파이프라인의 품질을 정량적으로 측정한다.

사용법:
    python 07_ragas_evaluation.py

평가 지표:
    - Faithfulness: 답변이 컨텍스트에 기반하는가? (환각 여부)
    - Answer Relevancy: 답변이 질문에 관련 있는가?
    - Context Recall: 검색된 문서가 ground truth를 얼마나 커버하는가?
"""

import json
import os

from datasets import Dataset
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
from ragas import evaluate
from ragas.llms import llm_factory
from ragas.metrics import AnswerRelevancy, ContextRecall, Faithfulness

from shared import API_KEY, get_llm, load_vector_store

EVAL_DATASET_PATH = os.path.join(os.path.dirname(__file__), "eval_dataset.json")

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


def generate_answers(eval_data: list) -> dict:
    """각 질문에 대해 RAG 파이프라인으로 답변 + 컨텍스트를 생성"""
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()
    chain = PROMPT | llm | StrOutputParser()

    questions, answers, contexts_list, ground_truths = [], [], [], []

    for item in eval_data:
        question = item["question"]
        ground_truth = item["ground_truth"]

        # 검색
        docs = retriever.invoke(question)
        contexts = [doc.page_content for doc in docs]
        context_str = format_docs(docs)

        # 답변 생성
        answer = chain.invoke({"context": context_str, "question": question})

        questions.append(question)
        answers.append(answer)
        contexts_list.append(contexts)
        ground_truths.append(ground_truth)

        print(f"  생성 완료: {question[:30]}...")

    return {
        "question": questions,
        "answer": answers,
        "contexts": contexts_list,
        "ground_truth": ground_truths,
    }


def run():
    # ── 1. 평가 데이터셋 로드 ──
    with open(EVAL_DATASET_PATH, encoding="utf-8") as f:
        eval_data = json.load(f)
    print(f"평가 데이터셋: {len(eval_data)}개 질문")

    # ── 2. RAG 파이프라인으로 답변 생성 ──
    print("\nRAG 답변 생성 중...")
    result_data = generate_answers(eval_data)
    dataset = Dataset.from_dict(result_data)

    # ── 3. RAGAS 평가 실행 ──
    print("\nRAGAS 평가 실행 중...")
    client = OpenAI(api_key=API_KEY)
    evaluator_llm = llm_factory("gpt-4o", client=client)
    metrics = [
        Faithfulness(llm=evaluator_llm),
        AnswerRelevancy(llm=evaluator_llm),
        ContextRecall(llm=evaluator_llm),
    ]
    result = evaluate(dataset, metrics=metrics)

    # ── 4. 결과 출력 ──
    print("\n" + "=" * 60)
    print("RAGAS 평가 결과")
    print("=" * 60)

    scores = result.to_pandas()
    metric_names = {
        "faithfulness": "Faithfulness",
        "answer_relevancy": "Answer Relevancy",
        "context_recall": "Context Recall",
    }

    print(f"\n{'Metric':<30} {'Score':>8}")
    print("-" * 40)
    for col in scores.columns:
        if col in metric_names:
            mean_score = scores[col].mean()
            print(f"  {metric_names[col]:<28} {mean_score:.3f}")

    # ── 5. 질문별 상세 결과 ──
    print(f"\n{'=' * 60}")
    print("질문별 상세 결과")
    print(f"{'=' * 60}")

    for i, row in scores.iterrows():
        question = row.get("question", eval_data[i]["question"])
        print(f"\n  Q: {question}")
        for col in scores.columns:
            if col in metric_names:
                print(f"    - {metric_names[col]}: {row[col]:.3f}")


if __name__ == "__main__":
    run()
