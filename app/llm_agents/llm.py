from typing import Dict
import os

import json
import google.generativeai as genai
from app.core.config import settings

# class BaseLLM(ABC):
#     """Abstract base class for all LLMs."""

#     @abstractmethod
#     def generate_response(self, prompt: str) -> str:
#         pass

#     @abstractmethod
#     def generate_next_state(self, prompt: str) -> Optional[str]:
#         pass


# class GPTLLM(BaseLLM):
#     """LLM wrapper for OpenAI's GPT models."""

#     def __init__(self, model_id: str):
#         self.model_id = model_id
#         self.api_key = os.environ.get("OPENAI_API_KEY", "")
#         if not self.api_key:
#             raise ValueError("OPENAI_API_KEY is not set in environment variables.")
#         openai.api_key = self.api_key

#     def generate_response(self, prompt: str) -> str:
#         response = openai.ChatCompletion.create(
#             model=self.model_id,
#             messages=[{"role": "user", "content": prompt}]
#         )
#         return response.choices[0].message.content.strip()

#     def generate_next_state(self, prompt: str) -> Optional[str]:
#         try:
#             response = openai.ChatCompletion.create(
#                 model=self.model,
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0,
#                 response_format="json"  # Requires GPT-4 or GPT-3.5-Turbo with function calling or JSON mode
#             )

#             content = response.choices[0].message.content
#             data = json.loads(content)

#             # Optional: validate the result
#             assert "state" in data, "Missing 'state' in model output"
#             return data["state"]

#         except Exception as e:
#             print(f"Error generating next state: {e}")
#             return "welcome"  # default fallback


class GeminiLLM:
    """LLM wrapper for Google's Gemini models."""

    def __init__(self):
        self.api_key = settings.google_api_key
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
        print(f"api_key: {self.api_key}")
        genai.configure(api_key=self.api_key)

    def generate_response(self, model_id: str, prompt: str):
        model = genai.GenerativeModel(model_id)
        result = model.generate_content(prompt, stream=True)
        print(f"DEBUG: Type from model.generate_content: {type(result)}")
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
