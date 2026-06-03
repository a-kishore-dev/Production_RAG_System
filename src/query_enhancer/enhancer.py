from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.retrievers import TransformRetriever

class HydeQueryEnhancer:
    
    def __init__(self, retriever, llm):
        self.llm = llm
        self.retriever = retriever
        self.hyde_query_transform = HyDEQueryTransform(
            llm = self.llm, 
            include_original=True
        )

    def get_hyde_retriever(self):
        '''
        Create hyde retriever that uses generated hypothetical answer
        as query and retrieve.
        '''

        hyde_retreiver = TransformRetriever(self.retriever, query_transform=self.hyde_query_transform)

        return hyde_retreiver
    

