from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from ragas.llms import llm_factory
from openai import OpenAI
from src.pipeline.rag_pipeline import RAGPipeline
from datasets import Dataset
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from ragas.embeddings import LlamaIndexEmbeddingsWrapper
from llama_index.core import Settings

def evaluate_rag():
    import os
    from dotenv import load_dotenv

    load_dotenv()

    groq_api_key = os.getenv("GROQ_API_KEY")
    gemini_api_key = os.getenv("GOOGLE_API_KEY")

    rag = RAGPipeline(
            dir_path="data/pdfs/",
            collection_name="knowledge_base",
            gemini_model_name="gemini-3.5-flash",
            gemini_api_key=gemini_api_key,
            groq_model_name="llama-3.1-8b-instant",
            groq_api_key=groq_api_key
        )

    hf_embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    embeddings = LlamaIndexEmbeddingsWrapper(hf_embed_model)

    questions = [
        "What is the Transformer architecture?",
        "Why was the Transformer proposed instead of RNNs and CNNs?",
        "What is scaled dot-product attention?",
        "Why is the attention score divided by sqrt(dk)?",
        "What is multi-head attention?",
        "How does the Transformer decoder work?",
        "What are the components of an encoder layer?",
        "What is self-attention?",
        "How does masking work in the decoder?",
        "What are positional encodings and why are they needed?",
        "How many attention heads are used in the base Transformer?",
        "What feed-forward network is used inside Transformer layers?",
        "What BLEU score did the Transformer achieve on WMT 2014 English-German translation?",
        "What BLEU score did the Transformer achieve on WMT 2014 English-French translation?",
        "What are the three applications of multi-head attention in the Transformer?"
    ]

    ground_truths = [
        "The Transformer is a sequence transduction architecture based entirely on attention mechanisms without using recurrence or convolutions.",

        "The Transformer was proposed to overcome the limitations of recurrent and convolutional networks while enabling greater parallelization and better modeling of long-range dependencies.",

        "Scaled dot-product attention computes attention by taking the dot product between queries and keys, dividing by sqrt(dk), applying softmax, and using the resulting weights to combine values.",

        "The attention score is divided by sqrt(dk) to prevent large dot-product values from causing extremely small gradients after the softmax operation.",

        "Multi-head attention projects queries, keys, and values into multiple learned subspaces, performs attention in parallel, concatenates the outputs, and applies a final projection.",

        "The decoder consists of six identical layers, each containing masked self-attention, encoder-decoder attention, and a position-wise feed-forward network.",

        "Each encoder layer contains a multi-head self-attention mechanism followed by a position-wise feed-forward network, along with residual connections and layer normalization.",

        "Self-attention allows each position in a sequence to attend to all positions in the same sequence and compute context-aware representations.",

        "Decoder masking prevents a position from attending to future tokens by masking illegal connections before the softmax operation.",

        "Positional encodings inject information about token order because the Transformer contains no recurrence or convolution.",

        "The base Transformer model uses 8 attention heads.",

        "The feed-forward network consists of two linear transformations with a ReLU activation between them.",

        "The Transformer achieved a BLEU score of 28.4 on the WMT 2014 English-German translation task.",

        "The Transformer achieved a BLEU score of 41.8 on the WMT 2014 English-French translation task.",

        "Multi-head attention is used for encoder self-attention, decoder self-attention, and encoder-decoder attention."
    ]

    responses = []
    retrieved_contexts = []

    for query in questions:
        response, nodes_with_score = rag.predict(query=query)
        responses.append(response)
        retrieved_contexts.append([nodes.get_content() for nodes in nodes_with_score[:3]])

    dataset_dict = {
        "user_input": questions,
        "response": responses,
        "retrieved_contexts": retrieved_contexts,
        "reference": ground_truths
    }
    eval_dataset = Dataset.from_dict(dataset_dict)

    client = OpenAI(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    evaluator_llm = llm_factory(model="llama-3.3-70b-versatile", provider="openai", client=client)

    results = evaluate(
        dataset=eval_dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        llm=evaluator_llm,
        embeddings=embeddings,
    )

    print(results)

    results.to_pandas().to_csv("ragas_result.csv", index=False)
    
