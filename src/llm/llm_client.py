from llama_index.llms.groq import Groq
from llama_index.llms.google_genai import GoogleGenAI

class LLMClient:
    def __init__(self):
        pass
        
    def get_gemini_llm(self, model_name, api_key):
        '''
        Return the gemini llm client
        '''
        gemini_llm = GoogleGenAI(
            model=model_name,
            api_key=api_key
        )

        return gemini_llm

    def get_groq_llm(self, model_name, api_key):
        '''
        Return the groq llm client
        '''
        groq_llm = Groq(
            model=model_name,
            api_key=api_key
        )
        
        return groq_llm
