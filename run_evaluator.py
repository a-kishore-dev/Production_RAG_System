import os
from dotenv import load_dotenv

load_dotenv()

from src.evaluation.evaluator import evaluate_rag

evaluate_rag()