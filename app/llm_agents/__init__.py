from .llm import GeminiLLM, GPTLLM

gemini = GeminiLLM()
gpt = GPTLLM()

__all__ = ["gemini", "gpt"]
