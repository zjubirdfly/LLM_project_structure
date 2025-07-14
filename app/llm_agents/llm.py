from typing import Dict
import os

import json
from google import genai
from app.core.config import settings
from openai import AsyncOpenAI
from google.genai.types import GenerateContentResponse

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

    async def generate_response(self, model_id: str, prompt: str):
        response: GenerateContentResponse = self.client.models.generate_content(
            model=model_id, contents=[prompt]
        )
        generated_text = ""
        if (
            response.candidates
            and response.candidates[0].content
            and response.candidates[0].content.parts
        ):
            for part in response.candidates[0].content.parts:
                if part.text:
                    generated_text += part.text
        else:
            print("Warning: No text content found in the non-streaming response.")

        return generated_text

    async def generate_next_state(
        self, model_id: str, prompt: str, output_schema: Dict
    ) -> str:
        generation_config = {
            "max_output_tokens": 200,
            "response_mime_type": "application/json",
            "response_schema": output_schema,
        }
        model = self.client.models.generate_content(
            model=model_id,
            contents=[prompt],
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": output_schema,
            },
        )
        response = model.generate_content(prompt)
        return json.loads(response.text)["state"]
