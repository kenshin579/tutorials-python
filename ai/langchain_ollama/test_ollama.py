from unittest import TestCase

from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class Test(TestCase):
    def test_ollam_example(self):
        # Ollama 모델 초기화 (기본 모델은 llama3.2, 다른 모델도 지정 가능)
        llm = Ollama(
            model="llama3.2",  # 사용할 모델 지정 (예: llama3.2, mistral, gemma 등)
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        )

        # 간단한 프롬프트로 모델 호출
        response = llm("파이썬이란 무엇인가요?")
        print(f"\n완성된 응답: {response}")

    def test_langchain_chain_example(self):
        # Ollama 모델 초기화
        llm = Ollama(model="llama3.2")

        # 프롬프트 템플릿 정의
        template = """
           다음 주제에 대해 간략하게 설명해주세요:

           주제: {topic}
           """

        prompt = PromptTemplate(template=template, input_variables=["topic"])

        # LLMChain 생성
        chain = LLMChain(llm=llm, prompt=prompt)

        # Chain 실행
        result = chain.run("인공지능의 역사")
        print(result)


    def test_chat_example(self):
        from langchain.memory import ConversationBufferMemory
        from langchain.chains import ConversationChain

        # Ollama 모델 초기화
        llm = Ollama(model="llama3.2")

        # 대화 메모리 생성
        memory = ConversationBufferMemory()

        # 대화 체인 생성
        conversation = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=True
        )

        # 첫 번째 질문
        print(conversation.predict(input="안녕하세요! 당신은 누구인가요?"))

        # 두 번째 질문 (이전 대화 기억)
        print(conversation.predict(input="파이썬에 대해 설명해주세요."))

    # 문서 검색 및 질의응답 예제
    def test_document_qa_example(self):
        from langchain.embeddings import OllamaEmbeddings
        from langchain.text_splitter import CharacterTextSplitter
        from langchain.vectorstores import Chroma
        from langchain.document_loaders import TextLoader
        from langchain.chains import RetrievalQA

        # 문서 로드 (예: sample_document.txt 파일)
        loader = TextLoader("sample_document.txt")
        documents = loader.load()

        # 문서 분할
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        # Ollama 임베딩 초기화
        embeddings = OllamaEmbeddings(model="llama3.2")

        # 벡터 저장소 생성
        db = Chroma.from_documents(texts, embeddings)

        # Ollama 모델 초기화
        llm = Ollama(model="llama3.2")

        # 검색 기반 질의응답 체인 생성
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever()
        )

        # 질문에 대한 답변 얻기
        query = "이 문서의 주요 내용은 무엇인가요?"
        result = qa.run(query)
        print(result)