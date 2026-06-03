from llama_index.core.retrievers import QueryFusionRetriever

class Retriever:
    
    def __init__(self, index, llm):
        self.index = index
        self.llm = llm

    def get_hybrid_retriever(self):
        '''
        Create a Hybrid retriever object to retrieve a query
        using Keyword and Semantic
        '''

        dense_retriever = self.index.as_retriever(
            vector_store_query_mode = "default",
            similarity_top_k=20
        )

        sparse_retriever = self.index.as_retriever(
            vector_store_query_mode = "sparse",
            sparse_top_k = 20
        )

        hybrid_retriever = QueryFusionRetriever(
            retrievers=[dense_retriever, sparse_retriever],
            llm=self.llm,
            similarity_top_k=20,
            num_queries=3,
            mode= "reciprocal_rerank",
            use_async=False,
            verbose=True,
        )

        return hybrid_retriever