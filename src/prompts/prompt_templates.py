from llama_index.core.prompts import RichPromptTemplate

class Prompts:
    def __init__(self):
        self.prompt_template = None

    def generate_prompt_template(self):
        '''
        Contains the prompt for generating answer with only on context
        '''

        qa_prompt = RichPromptTemplate(
            """
            {% chat role="system" %}
            You are a research assistant specialized in answering questions from scientific papers.

            Rules:
            - Answer ONLY using the provided context.
            - Do NOT use outside knowledge.
            - Every factual statement must contain a citation.
            - If the sentences in the paragraph is from same page cite at the end of the paragraph.
            - Format the title correctly
            - Citation format:

            [Source: <title>, Page <page_number>]

            - If multiple chunks support a statement, cite all relevant sources.
            - If the answer cannot be found in the context, say:
            "I could not find this information in the provided documents."

            {% endchat %}

            {% chat role="user" %}

            QUESTION
            --------
            {{ query }}

            DOCUMENT INFORMATION
            --------------------

            {{ document_info }}

            RETRIEVED CONTEXT
            -----------------

            {{ context_str }}

            Generate a detailed answer with citations.

            {% endchat %}
            """
        )

        return qa_prompt

    def format_prompt(self, query, reranked_nodes, document_metadata):
        '''
        Insert Query, Reranked nodes and documents metadata into the prompt template
        '''
        self.prompt_template = self.generate_prompt_template()

        used_docs = set()
        for node in reranked_nodes:
            used_docs.add(node.metadata["name"])
        
        document_info = ""
        for doc_name in used_docs:
            doc = document_metadata[doc_name]
            document_info+=f"""
            Title: {doc["title"]}

            Author: {", ".join(doc["author"])}

            Abstract: {doc["abstract"][:1000]}

            """
        
        context_str = ""
        for i, node in enumerate(reranked_nodes, start=1):
            context_str += f"""
            Chunk {i}

            Name: {node.metadata["title"]}
            Page Number: {node.metadata["page_number"]}
            Chunk Index of Document: {node.metadata["chunk_index"]}

            {node.text}

            """

        formatted_prompt = self.prompt_template.format(
            query = query,
            document_info=document_info,
            context_str=context_str
        )

        return formatted_prompt