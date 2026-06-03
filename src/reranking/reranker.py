from llama_index.core.postprocessor import SentenceTransformerRerank

class ReRanker:

    def __init__(self, query, retrieved_nodes):
        self.query = query
        self.retrieved_nodes = retrieved_nodes
        self.reranker_model = SentenceTransformerRerank(
            model="cross-encoder/ms-marco-MiniLM-L-6-v2",
            top_n=5
        )

    def rerank_nodes(self):
        '''
        Rerank the retrieved nodes using the cross encoder and return top 5 nodes
        '''

        reranked_nodes = self.reranker_model.postprocess_nodes(
            nodes=self.retrieved_nodes,
            query_str=self.query,
        )

        return reranked_nodes