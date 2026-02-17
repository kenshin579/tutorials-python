"""대화 히스토리 관리 - ConversationBufferMemory vs ConversationSummaryMemory 비교

사용법:
    python 06_conversation_memory.py
"""

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from shared import get_llm, load_vector_store

# ── 미리 정의된 대화 시나리오 ──────────────────────────────

SCENARIO = [
    "청약철회 기간이 어떻게 되나요?",
    "그 기간이 지나면 어떻게 되나요?",  # "그 기간" = 이전 맥락 참조
    "환불은 언제까지 해줘야 하나요?",
    "사업자가 환불을 안 해주면 어떤 불이익이 있나요?",  # 이전 맥락 참조
    "처음 질문으로 돌아가서, 전자상거래 외 방문판매도 동일한 기간인가요?",
]

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 법률 Q&A 챗봇입니다. 컨텍스트를 기반으로 답변하세요. "
            "컨텍스트에 답이 없으면 '해당 정보를 찾을 수 없습니다'라고 답변하세요.",
        ),
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "컨텍스트:\n{context}\n\n질문: {question}",
        ),
    ]
)

SUMMARY_PROMPT = ChatPromptTemplate.from_template(
    """다음 대화를 3줄 이내로 요약하세요. 핵심 주제와 중요한 정보만 포함하세요.

대화:
{conversation}

요약:"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def messages_to_text(messages: list) -> str:
    """메시지 리스트를 텍스트로 변환"""
    lines = []
    for msg in messages:
        role = "사용자" if isinstance(msg, HumanMessage) else "챗봇"
        lines.append(f"{role}: {msg.content}")
    return "\n".join(lines)


def estimate_tokens(messages: list) -> int:
    """메시지 리스트의 대략적인 토큰 수 추정 (한국어: ~1.5자당 1토큰)"""
    total_chars = sum(len(msg.content) for msg in messages)
    return int(total_chars / 1.5)


# ── Buffer 방식: 전체 대화 기록 유지 ─────────────────────

def run_buffer_memory(retriever) -> dict:
    """전체 대화 이력을 그대로 유지하는 방식"""
    llm = get_llm()
    chain = PROMPT | llm | StrOutputParser()
    history: list = []
    answers = []

    for question in SCENARIO:
        docs = retriever.invoke(question)
        context = format_docs(docs)

        answer = chain.invoke(
            {"history": history, "context": context, "question": question}
        )
        answers.append(answer)

        # 전체 대화를 그대로 쌓기
        history.append(HumanMessage(content=question))
        history.append(AIMessage(content=answer))

    return {
        "answers": answers,
        "history": history,
        "tokens": estimate_tokens(history),
    }


# ── Summary 방식: 대화를 요약하여 유지 ─────────────────────

def run_summary_memory(retriever) -> dict:
    """대화를 매 턴마다 요약하여 유지하는 방식"""
    llm = get_llm()
    chain = PROMPT | llm | StrOutputParser()
    summary_chain = SUMMARY_PROMPT | get_llm(model="gpt-4o-mini") | StrOutputParser()

    history: list = []
    full_conversation: list = []  # 요약용 전체 대화 (내부)
    answers = []

    for question in SCENARIO:
        docs = retriever.invoke(question)
        context = format_docs(docs)

        answer = chain.invoke(
            {"history": history, "context": context, "question": question}
        )
        answers.append(answer)

        # 전체 대화에 추가 (요약 입력용)
        full_conversation.append(HumanMessage(content=question))
        full_conversation.append(AIMessage(content=answer))

        # 매 턴 후 대화를 요약하여 히스토리 갱신
        conversation_text = messages_to_text(full_conversation)
        summary = summary_chain.invoke({"conversation": conversation_text})
        history = [AIMessage(content=f"[이전 대화 요약] {summary}")]

    return {
        "answers": answers,
        "history": history,
        "tokens": estimate_tokens(history),
    }


# ── 실행 및 비교 ────────────────────────────────────────

def run():
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    print("대화 시나리오 실행 중...\n")

    buffer_result = run_buffer_memory(retriever)
    summary_result = run_summary_memory(retriever)

    # ── 결과 출력 ──
    print("=" * 60)
    print("대화 시나리오")
    print("=" * 60)
    for i, q in enumerate(SCENARIO, 1):
        print(f"  Q{i}: {q}")

    print("\n" + "=" * 60)
    print("ConversationBufferMemory 결과")
    print("=" * 60)
    for i, (q, a) in enumerate(zip(SCENARIO, buffer_result["answers"]), 1):
        print(f"\n  Q{i}: {q}")
        print(f"  A{i}: {a[:150]}{'...' if len(a) > 150 else ''}")
    print(f"\n  [메모리 크기] ~{buffer_result['tokens']} 토큰")

    print("\n" + "=" * 60)
    print("ConversationSummaryMemory 결과")
    print("=" * 60)
    for i, (q, a) in enumerate(zip(SCENARIO, summary_result["answers"]), 1):
        print(f"\n  Q{i}: {q}")
        print(f"  A{i}: {a[:150]}{'...' if len(a) > 150 else ''}")
    print(f"\n  [메모리 크기] ~{summary_result['tokens']} 토큰")
    print(f"  [최종 요약] {summary_result['history'][0].content}")

    # ── 비교 ──
    buffer_tokens = buffer_result["tokens"]
    summary_tokens = summary_result["tokens"]
    reduction = (1 - summary_tokens / buffer_tokens) * 100 if buffer_tokens else 0

    print(f"\n{'=' * 60}")
    print("비교 분석")
    print(f"{'=' * 60}")
    print(f"  Buffer 메모리:  ~{buffer_tokens} 토큰")
    print(f"  Summary 메모리: ~{summary_tokens} 토큰")
    print(f"  토큰 절감:      {reduction:.0f}%")


if __name__ == "__main__":
    run()
