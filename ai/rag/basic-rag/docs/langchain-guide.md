# LangChain 프레임워크 가이드

## LangChain이란?

LangChain은 LLM 기반 애플리케이션을 개발하기 위한 오픈소스 프레임워크다. 프롬프트 관리, 체인 구성, 외부 도구 연동, 메모리 관리 등 LLM 앱 개발에 필요한 기능을 제공한다.

## 핵심 개념

### LCEL (LangChain Expression Language)

LCEL은 LangChain의 선언적 체인 구성 문법이다. 파이프(`|`) 연산자로 컴포넌트를 연결하여 데이터 처리 파이프라인을 구성한다.

```python
chain = prompt | llm | output_parser
result = chain.invoke({"question": "질문"})
```

### Document Loaders

다양한 형식의 문서를 LangChain의 Document 객체로 변환하는 컴포넌트다.
- TextLoader: 텍스트 파일
- PyPDFLoader: PDF 파일
- WebBaseLoader: 웹 페이지
- CSVLoader: CSV 파일

### Text Splitters

긴 문서를 작은 청크로 분할하는 컴포넌트다.
- CharacterTextSplitter: 고정 크기 분할
- RecursiveCharacterTextSplitter: 재귀적 분할 (권장)
- SemanticChunker: 의미 기반 분할

### Vector Stores

임베딩된 벡터를 저장하고 유사도 검색을 수행하는 컴포넌트다.
- ChromaDB: 경량 오픈소스, 프로토타이핑에 적합
- FAISS: Meta 개발, 고성능 검색
- Pinecone: 완전 관리형 클라우드 서비스

### Retrievers

벡터 저장소에서 관련 문서를 검색하는 컴포넌트다. `as_retriever()` 메서드로 벡터 저장소를 검색기로 변환할 수 있다.

## RAG 체인 구성 예시

```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

이 체인은 질문을 받아 관련 문서를 검색하고, 프롬프트에 삽입한 뒤 LLM으로 답변을 생성한다.
