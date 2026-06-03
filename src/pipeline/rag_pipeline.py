from src.ingestion.loader import Ingestion
from src.chunking.chunker import Chunker
from src.vectordb.vector_store import VectorStore
from src.retrieval.retriever import Retriever
from src.reranking.reranker import ReRanker
from src.query_enhancer.enhancer import HydeQueryEnhancer
from src.llm.llm_client import LLMClient
from src.prompts.prompt_templates import Prompts


import os
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GOOGLE_API_KEY")

class RAGPipeline:

    def __init__(self, dir_path, collection_name, gemini_model_name, gemini_api_key, groq_model_name, groq_api_key):
        self.llm_client = LLMClient()
        self.groq_llm = self.llm_client.get_groq_llm(
                    model_name=groq_model_name, 
                    api_key=groq_api_key
                )
        self.gemini_llm = self.llm_client.get_gemini_llm(
                    model_name=gemini_model_name,
                    api_key=gemini_api_key
                )

        self.ingestion = Ingestion(dir_path=dir_path)
        self.document, self.documents_metadata = self.ingestion.parse_all_pdfs()

        self.chunker = Chunker()
        self.chunks = self.chunker.chunk_into_sentence(documents=self.document)

        self.vector_store = VectorStore(collection_name=collection_name)
        self.index = self.vector_store.get_index(self.chunks)

        self.retriever = Retriever(index=self.index, llm=self.groq_llm)
        self.hybrid_retriever = self.retriever.get_hybrid_retriever()

        self.query_enhancer = HydeQueryEnhancer(retriever=self.hybrid_retriever, llm=self.groq_llm)

        self.hyde_retriever = self.query_enhancer.get_hyde_retriever()

        self.prompts_template = Prompts()

    def predict(self, query):

        retrieved_nodes = self.hyde_retriever.retrieve(query)

        reranker = ReRanker(query = query, retrieved_nodes=retrieved_nodes)

        reranked_nodes = reranker.rerank_nodes()
        
        formatted_prompt_template = self.prompts_template.format_prompt(
            query=query,
            reranked_nodes=reranked_nodes,
            document_metadata=self.documents_metadata,
        )

        response = self.gemini_llm.complete(
            prompt=formatted_prompt_template
        )

        return response.text, reranked_nodes

