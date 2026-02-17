"""프롬프트 엔지니어링 기법 비교 - 동일 질문에 대해 4가지 프롬프트 전략의 답변 차이를 비교한다.

사용법:
    python 01_prompt_engineering.py "청약철회 기간은?"
    python 01_prompt_engineering.py "연차휴가는 며칠인가요?"
"""

import sys

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from shared import get_llm, load_vector_store

# ── 1. 프롬프트 템플릿 정의 ──────────────────────────────

ZERO_SHOT = ChatPromptTemplate.from_template(
    """다음 컨텍스트를 기반으로 질문에 답변하세요.
컨텍스트에 답이 없으면 "해당 정보를 찾을 수 없습니다"라고 답변하세요.

컨텍스트:
{context}

질문: {question}
답변:"""
)

FEW_SHOT = ChatPromptTemplate.from_template(
    """다음 컨텍스트를 기반으로 질문에 답변하세요.
컨텍스트에 답이 없으면 "해당 정보를 찾을 수 없습니다"라고 답변하세요.

다음은 좋은 답변의 예시입니다:

예시 1)
질문: 법정 근로시간은 어떻게 되나요?
답변: 1주간의 근로시간은 휴게시간을 제외하고 40시간을 초과할 수 없으며, 1일 근로시간은 8시간을 초과할 수 없습니다. (근거: 근로기준법)

예시 2)
질문: 임대차 계약 최소 기간은?
답변: 기간을 정하지 않거나 2년 미만으로 정한 임대차는 2년으로 봅니다. 다만, 임차인은 2년 미만의 기간이 유효함을 주장할 수 있습니다. (근거: 주택임대차보호법)

컨텍스트:
{context}

질문: {question}
답변:"""
)

COT = ChatPromptTemplate.from_template(
    """다음 컨텍스트를 기반으로 질문에 답변하세요.
컨텍스트에 답이 없으면 "해당 정보를 찾을 수 없습니다"라고 답변하세요.

답변 시 다음 단계를 따르세요:
1. 먼저 질문의 핵심 키워드를 파악하세요
2. 컨텍스트에서 관련 조항을 찾으세요
3. 해당 조항의 내용을 정리하세요
4. 최종 답변을 간결하게 작성하세요

컨텍스트:
{context}

질문: {question}

단계별 분석:"""
)

ROLE_SPECIFIC = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 10년 경력의 법률 전문가입니다. "
            "법률 용어를 쉽게 풀어서 설명하고, 관련 법률 조항을 명시하며, "
            "실생활에서 주의할 점도 함께 안내합니다. "
            "컨텍스트에 없는 내용은 답변하지 않습니다.",
        ),
        (
            "human",
            "다음 컨텍스트를 참고하여 질문에 답변해주세요.\n\n"
            "컨텍스트:\n{context}\n\n질문: {question}",
        ),
    ]
)

PROMPTS = {
    "Zero-shot": ZERO_SHOT,
    "Few-shot": FEW_SHOT,
    "Chain-of-Thought": COT,
    "Role-specific": ROLE_SPECIFIC,
}


# ── 2. 실행 ──────────────────────────────────────────────


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def run(question: str):
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()

    # 검색은 한 번만 수행하여 동일 컨텍스트 보장
    retrieved_docs = retriever.invoke(question)
    context = format_docs(retrieved_docs)

    print(f"\n질문: {question}")
    print(f"검색된 컨텍스트: {len(context)}자 ({len(retrieved_docs)}개 청크)")
    print("=" * 60)

    for name, prompt in PROMPTS.items():
        chain = prompt | llm | StrOutputParser()
        answer = chain.invoke({"context": context, "question": question})

        print(f"\n== {name} ==")
        print(f"답변: {answer}")
        print("-" * 60)


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "청약철회 기간은?"
    run(q)
