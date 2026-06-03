from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter, SemanticSplitterNodeParser, HierarchicalNodeParser,get_leaf_nodes
from llama_index.core.schema import TextNode

class Chunker:

    def __init__(self):
        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-base-en-v1.5"
        )

    def clean_chunks(self, chunks, minimum_chars=50):
        MIN_CHARS = minimum_chars

        chunks = [
            node
            for node in chunks
            if node.text
            and node.text.strip()
            and len(node.text.strip()) >= MIN_CHARS
        ]

        return chunks

    def chunk_into_sentence(self, documents):
        '''
        Split the document into Nodes, with node being a sentence
        '''

        sentence_splitter = SentenceSplitter(
            chunk_size=512, 
            chunk_overlap=50
        )

        nodes = []
        for doc in documents:
            chunks = sentence_splitter.split_text(doc.text)
            for i, chunk in enumerate(chunks, start=1):
                node = TextNode(text=chunk)
                node.metadata = doc.metadata.copy()
                node.metadata["chunk_index"] = i
                nodes.append(node)

        return nodes

    def chunk_on_semantic(self, documents):
        '''
        Splits a document into Nodes, with each node being a group of semantically related sentences.
        '''

        semantic_splitter = SemanticSplitterNodeParser(
            buffer_size=2,
            breakpoint_percentile_threshold=75,
            embed_model=self.embed_model
        )

        nodes = []
        for doc in documents:
            chunks = semantic_splitter.sentence_splitter(doc.text)
            for i, chunk in enumerate(chunks, start=1):
                node = TextNode(text=chunk)
                node.metadata = doc.metadata.copy()
                node.metadata["chunk_index"] = i
                nodes.append(node)

        return nodes

    def chunk_on_hierarchy(documents):
        '''
        Splits a document into a recursive hierarchy Nodes using a NodeParser.
        '''
        
        hierarchial_splitter = HierarchicalNodeParser.from_defaults(
            chunk_sizes=[1026, 516]
        )

        hierarchial_chunks = hierarchial_splitter.get_nodes_from_documents(documents)

        leaf_chunks = get_leaf_nodes(hierarchial_chunks)

        return hierarchial_chunks, leaf_chunks