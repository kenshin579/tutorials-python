# adv-rag - RAG 최적화 샘플 코드

> **블로그 편 2**: "RAG 기반 블로그 Q&A 챗봇 만들기 (2) - 프롬프트 엔지니어링과 RAG 최적화"에서 참조하는 샘플 코드

## 프로젝트 구조

```
adv-rag/
├── README.md
├── pyproject.toml
├── docs/                              # 테스트용 마크다운 문서 (basic-rag 재활용)
│   ├── consumer-protection-act.md
│   ├── labor-standards-act.md
│   └── tenant-protection-act.md
│
├── 01_prompt_engineering.py           # 프롬프트 엔지니어링 기법 비교
├── 02_hybrid_search.py                # Hybrid Search (BM25 + 벡터)
├── 03_reranking.py                    # Re-ranking (Cohere Rerank)
├── 04_multi_query_retrieval.py        # Multi-query Retrieval
├── 05_context_compression.py          # Contextual Compression
├── 06_conversation_memory.py          # 대화 히스토리 관리 (Buffer vs Summary)
├── 07_ragas_evaluation.py             # RAGAS 자동 평가
├── eval_dataset.json                  # 평가용 데이터셋 (Q&A 쌍 + ground truth)
└── shared.py                          # 공통 유틸리티 (임베딩, 벡터 저장소 로드 등)
```

## 블로그 섹션 ↔ 코드 매핑

| 블로그 섹션 | 파일 | 핵심 내용 |
|------------|------|----------|
| 1. 프롬프트 엔지니어링 기법 | `01_prompt_engineering.py` | 동일 질문에 대해 4가지 프롬프트 전략 비교 |
| 2.1 검색 품질 향상 - Hybrid Search | `02_hybrid_search.py` | BM25 + 벡터 검색 결합 |
| 2.1 검색 품질 향상 - Re-ranking | `03_reranking.py` | Cohere Rerank으로 검색 결과 재정렬 |
| 2.1 검색 품질 향상 - Multi-query | `04_multi_query_retrieval.py` | 질문을 여러 변형으로 확장하여 검색 |
| 2.2 컨텍스트 윈도우 관리 | `05_context_compression.py` | 검색 결과 압축으로 노이즈 제거 |
| 2.3 대화 히스토리 관리 | `06_conversation_memory.py` | Buffer vs Summary 메모리 비교 |
| 4. RAG 품질 평가 | `07_ragas_evaluation.py` + `eval_dataset.json` | RAGAS 자동 평가 파이프라인 |

> 블로그 섹션 3 (RAFT)과 5 (프로덕션 고려사항)는 개념 설명 위주이므로 별도 샘플 코드 없음

---

## 각 파일 상세 명세

### `shared.py` - 공통 유틸리티

basic-rag의 인덱싱/벡터 저장소 로딩 로직을 재사용 가능하게 분리한다.

```python
# 주요 함수
def get_embeddings()          # OpenAIEmbeddings 인스턴스 반환
def load_vector_store()       # ChromaDB 벡터 저장소 로드
def index_documents()         # docs/ 문서 인덱싱 (basic-rag과 동일 로직)
def load_docs_as_chunks()     # 문서 로드 + 청킹 결과 반환 (BM25 등에서 사용)
```

---

### `01_prompt_engineering.py` - 프롬프트 엔지니어링 기법 비교

동일한 질문 + 동일한 검색 결과에 대해 4가지 프롬프트 전략의 답변 차이를 비교한다.

**구현 항목:**

| 기법 | 설명 |
|------|------|
| Zero-shot | 컨텍스트만 제공, 예시 없음 |
| Few-shot | 2~3개의 Q&A 예시를 프롬프트에 포함 |
| CoT (Chain-of-Thought) | "단계별로 생각하세요" 지시 추가 |
| Role-specific | 시스템 프롬프트로 "법률 전문가" 역할 부여 |

```python
# 실행
python 01_prompt_engineering.py "청약철회 기간은?"

# 출력 예시
== Zero-shot ==
답변: ...

== Few-shot ==
답변: ...

== Chain-of-Thought ==
답변: ...

== Role-specific ==
답변: ...
```

**포인트**: 동일 입력에 프롬프트만 바꿔서 품질 차이를 직관적으로 보여주는 것이 핵심

---

### `02_hybrid_search.py` - Hybrid Search (BM25 + 벡터)

키워드 검색(BM25)과 시맨틱 검색(벡터)을 결합하여 검색 품질을 향상시킨다.

**구현 항목:**
- `BM25Retriever`: 키워드 기반 검색 (langchain_community)
- `ChromaDB retriever`: 벡터 기반 검색
- `EnsembleRetriever`: 두 검색 결과를 가중치 기반으로 결합

```python
# 핵심 코드 구조
bm25_retriever = BM25Retriever.from_documents(chunks, k=3)
vector_retriever = vector_store.as_retriever(search_kwargs={"k": 3})
ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]  # 키워드 40%, 시맨틱 60%
)

# 실행: 3가지 검색 방식 결과 비교
python 02_hybrid_search.py "연차휴가 일수"

# 출력 예시
== BM25 (키워드) 검색 결과 ==
  [1] labor-standards-act.md - "...연차휴가..."

== 벡터 (시맨틱) 검색 결과 ==
  [1] labor-standards-act.md - "...유급휴가..."

== Hybrid (BM25 + 벡터) 검색 결과 ==
  [1] labor-standards-act.md - "...연차휴가..." (결합 점수: 0.92)
```

**포인트**: "연차휴가"라는 정확한 키워드가 있을 때 BM25가 강하고, "쉬는 날은 며칠?"처럼 의미만 통하는 경우 벡터가 강한 것을 보여줌

---

### `03_reranking.py` - Re-ranking

초기 검색 결과를 Cross-encoder 또는 Cohere Rerank으로 재정렬하여 정밀도를 높인다.

**구현 항목:**
- 초기 검색: top_k=10으로 넓게 검색
- Re-ranking: Cohere Rerank API로 상위 3개 재정렬
- 비교: Re-ranking 전/후 순위 변화 출력

```python
# 핵심 코드 구조
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

base_retriever = vector_store.as_retriever(search_kwargs={"k": 10})
reranker = CohereRerank(model="rerank-v3.5", top_n=3)
reranking_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever
)

# 실행
python 03_reranking.py "임대차 보증금 반환"

# 출력 예시
== Re-ranking 전 (벡터 유사도 순) ==
  [1] tenant-protection-act.md (score: 0.82) - "대항력의 요건..."
  [2] tenant-protection-act.md (score: 0.79) - "보증금 반환 청구..."
  [3] consumer-protection-act.md (score: 0.71) - "환불 의무..."

== Re-ranking 후 (Cohere Rerank) ==
  [1] tenant-protection-act.md (relevance: 0.95) - "보증금 반환 청구..."  ← 순위 상승
  [2] tenant-protection-act.md (relevance: 0.88) - "대항력의 요건..."
  [3] tenant-protection-act.md (relevance: 0.42) - "임대차 기간..."       ← 관련 없는 문서 제거됨
```

**포인트**: Re-ranking이 단순 유사도 검색의 순위 오류를 교정하는 것을 직관적으로 보여줌

---

### `04_multi_query_retrieval.py` - Multi-query Retrieval

LLM이 원래 질문을 여러 관점으로 변형하여 검색 범위를 넓힌다.

**구현 항목:**
- `MultiQueryRetriever`: LLM이 질문 3개 변형 생성 → 각각 검색 → 결과 합산
- 원본 질문 단일 검색 vs Multi-query 검색 결과 비교

```python
# 핵심 코드 구조
from langchain.retrievers.multi_query import MultiQueryRetriever

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    llm=ChatOpenAI(model="gpt-4o", temperature=0)
)

# 실행
python 04_multi_query_retrieval.py "퇴직금 받을 수 있는 조건"

# 출력 예시
== LLM이 생성한 변형 질문 ==
  1. 퇴직금 지급 요건은 무엇인가?
  2. 퇴직금을 받기 위한 근속 기간은?
  3. 퇴직금 산정 기준과 지급 조건은?

== 단일 질문 검색 결과 (3개) ==
  ...

== Multi-query 검색 결과 (중복 제거 후 5개) ==
  ...  ← 더 다양한 관련 문서 검색됨
```

---

### `05_context_compression.py` - Contextual Compression

검색된 문서에서 질문과 관련 있는 부분만 추출하여 LLM에 전달한다.

**구현 항목:**
- `LLMChainExtractor`: LLM으로 관련 부분만 추출
- 압축 전/후 컨텍스트 길이 및 답변 품질 비교

```python
# 핵심 코드 구조
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(ChatOpenAI(model="gpt-4o-mini", temperature=0))
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vector_store.as_retriever(search_kwargs={"k": 5})
)

# 실행
python 05_context_compression.py "최저임금 위반 시 벌칙"

# 출력 예시
== 압축 전 컨텍스트 (2,847자) ==
  [1] 근로기준법 제6장 임금... (전체 청크)

== 압축 후 컨텍스트 (412자) ==
  [1] 최저임금 미만 지급 시 3년 이하 징역 또는 2천만원 이하 벌금...

토큰 절감: 85%
```

---

### `06_conversation_memory.py` - 대화 히스토리 관리

멀티턴 대화에서 컨텍스트를 유지하는 두 가지 메모리 전략을 비교한다.

**구현 항목:**
- `ConversationBufferMemory`: 전체 대화 기록 유지 (토큰 소비 큼)
- `ConversationSummaryMemory`: 대화를 요약하여 유지 (토큰 절약)
- 시뮬레이션: 미리 정의된 5턴 대화를 두 방식으로 실행 후 비교

```python
# 실행 (미리 정의된 대화 시나리오 자동 실행)
python 06_conversation_memory.py

# 출력 예시
== 대화 시나리오 (5턴) ==
  Q1: 청약철회 기간이 어떻게 되나요?
  Q2: 그 기간이 지나면 어떻게 되나요?      ← "그 기간" = 이전 맥락 참조
  Q3: 환불은 언제까지 해줘야 하나요?
  Q4: 위반하면 벌칙이 있나요?               ← "위반" = 이전 맥락 참조
  Q5: 처음 질문으로 돌아가서, 전자상거래 외 다른 경우도 동일한가요?

== ConversationBufferMemory 결과 ==
  [5턴 후 메모리 크기] 1,847 토큰
  [Q2 답변] 7일이 경과하면 청약철회 권리가 소멸...  ✅ 맥락 유지
  [Q5 답변] 방문판매의 경우 14일로...                ✅ 맥락 유지

== ConversationSummaryMemory 결과 ==
  [5턴 후 메모리 크기] 312 토큰 (83% 절감)
  [Q2 답변] 청약철회 기간 경과 시...                 ✅ 맥락 유지
  [Q5 답변] 방문판매는 14일...                       ✅ 맥락 유지 (요약에서 복원)
```

**포인트**: 짧은 대화에서는 Buffer가 충분하지만, 대화가 길어질수록 Summary가 효율적이라는 트레이드오프를 보여줌

---

### `07_ragas_evaluation.py` + `eval_dataset.json` - RAGAS 평가

RAG 파이프라인의 품질을 정량적으로 측정한다.

**eval_dataset.json 구조:**
```json
[
  {
    "question": "청약철회 기간은 며칠인가요?",
    "ground_truth": "소비자는 계약내용에 관한 서면을 받은 날부터 7일 이내에 청약의 철회를 할 수 있다.",
    "contexts": []
  },
  {
    "question": "연차휴가는 며칠인가요?",
    "ground_truth": "1년간 80% 이상 출근한 근로자에게 15일의 유급휴가가 주어진다.",
    "contexts": []
  }
]
```
- 10~15개의 Q&A 쌍 (docs/ 문서 기반)
- `contexts`는 실행 시 RAG 파이프라인이 자동으로 채움

**구현 항목:**
- basic-rag 체인으로 각 질문에 대한 답변 + 검색 컨텍스트 생성
- RAGAS 평가 지표 3가지 측정:
  - **Context Relevance**: 검색된 문서가 질문에 관련 있는가?
  - **Faithfulness**: 답변이 컨텍스트에 기반하는가? (환각 여부)
  - **Answer Correctness**: 답변이 ground truth와 일치하는가?

```python
# 실행
python 07_ragas_evaluation.py

# 출력 예시
== RAGAS 평가 결과 ==
┌──────────────────────────────────┬────────┐
│ Metric                           │ Score  │
├──────────────────────────────────┼────────┤
│ Context Relevance                │ 0.847  │
│ Faithfulness                     │ 0.923  │
│ Answer Correctness               │ 0.891  │
│ Overall (harmonic mean)          │ 0.886  │
└──────────────────────────────────┴────────┘

== 질문별 상세 결과 ==
  Q: 청약철회 기간은?
    - Context Relevance: 0.93
    - Faithfulness: 1.00
    - Answer Correctness: 0.95
  ...
```

---

## 의존성 (`pyproject.toml`)

```toml
[project]
name = "adv-rag"
version = "0.1.0"
description = "RAG 최적화 샘플 코드 - 프롬프트 엔지니어링, Hybrid Search, Re-ranking, RAGAS 평가"
requires-python = ">=3.11"
dependencies = [
    "langchain>=0.3.0",
    "langchain-openai>=0.3.0",
    "langchain-chroma>=0.2.0",
    "langchain-community>=0.3.0",
    "langchain-cohere>=0.4.0",          # Re-ranking (Cohere Rerank)
    "rank-bm25>=0.2.0",                 # BM25 검색
    "ragas>=0.2.0",                     # RAG 평가 프레임워크
]
```

## 필요한 환경 변수

```bash
export OPENAI_API_KEY=your_openai_key       # 필수 (임베딩 + LLM)
export COHERE_API_KEY=your_cohere_key       # 03_reranking.py에서 사용
```

## 실행 순서

```bash
cd tutorials-python/ai/rag/adv-rag

# 1. 의존성 설치
pip install -e .

# 2. 문서 인덱싱 (basic-rag과 동일한 docs/ 사용)
python shared.py index

# 3. 각 예제 개별 실행
python 01_prompt_engineering.py "청약철회 기간은?"
python 02_hybrid_search.py "연차휴가 일수"
python 03_reranking.py "임대차 보증금 반환"
python 04_multi_query_retrieval.py "퇴직금 받을 수 있는 조건"
python 05_context_compression.py "최저임금 위반 시 벌칙"
python 06_conversation_memory.py
python 07_ragas_evaluation.py
```
