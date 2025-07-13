from typing import Dict
import os

import json
from google import genai
from app.core.config import settings
from openai import AsyncOpenAI

# class BaseLLM(ABC):
#     """Abstract base class for all LLMs."""

#     @abstractmethod
#     def generate_response(self, prompt: str) -> str:
#         pass

#     @abstractmethod
#     def generate_next_state(self, prompt: str) -> Optional[str]:
#         pass


class GPTLLM:
    """LLM wrapper for OpenAI's GPT models."""

    def __init__(self):
        self.api_key = settings.openai_api_key
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables.")
        print(f"open ai api_key: {self.api_key}")
        self.client = AsyncOpenAI(api_key=self.api_key)

    def generate_response(self, model_id: str, system_prompt: str, user_prompt: str):
        return self.client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            stream=True,
        )

    def generate_next_state(self, prompt: str) -> str:
        # TODO: Implement logic to generate the next state based on the prompt
        return "welcome"


class GeminiLLM:
    """LLM wrapper for Google's Gemini models."""

    def __init__(self):
        self.api_key = settings.google_api_key
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
        print(f"gemini api_key: {self.api_key}")
        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, model_id: str, prompt: str):
        result = self.client.models.generate_content_stream(
            model=model_id, contents=[prompt]
        )
        print(f"DEBUG: client.generate_content: {result}")
        return result

    def generate_next_state(
        self, model_id: str, prompt: str, output_schema: Dict
    ) -> str:
        model = genai.GenerativeModel(
            model_name=model_id,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": output_schema,
            },
        )
        response = model.generate_content(prompt)
        return json.loads(response.text)["state"]
