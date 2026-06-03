from qdrant_client import QdrantClient, models
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.settings import Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore

class VectorStore:

    def __init__(self, collection_name):
        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-base-en-v1.5"
        )
        Settings.embed_model = self.embed_model
        self.collection_name = collection_name
        self.client = QdrantClient(":memory:")

    def get_index(self, chunks):
        '''
        Embed the chunks
        '''

        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,
                    distance=models.Distance.COSINE
                ),
                sparse_vectors_config={
                    "text-sparse-new": models.SparseVectorParams()
                }
            )

        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            enable_hybrid=True,
            fastembed_sparse_model="Qdrant/bm25"
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex(
            nodes=chunks,
            storage_context=storage_context
        )

        return index
