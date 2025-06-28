from abc import ABC, abstractmethod
from typing import Dict
import os

import openai
import google.generativeai as genai


class BaseLLM(ABC):
    """Abstract base class for all LLMs."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class GPTLLM(BaseLLM):
    """LLM wrapper for OpenAI's GPT models."""

    def __init__(self, model_id: str):
        self.model_id = model_id
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables.")
        openai.api_key = self.api_key

    def generate(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()


class GeminiLLM(BaseLLM):
    """LLM wrapper for Google's Gemini models."""

    def __init__(self, model_id: str):
        self.model_id = model_id
        self.api_key = os.environ.get("GOOGLE_API_KEY", "")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_id)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()


def generate_response(prompt: str, model_id: str) -> str:
    """Factory interface to get response from a selected model."""
    if model_id.startswith("gpt"):
        llm = GPTLLM(model_id)
    elif model_id.startswith("gemini"):
        llm = GeminiLLM(model_id)
    else:
        raise ValueError(f"Unsupported model ID: {model_id}")
    
    return llm.generate(prompt)