from typing import Dict

import json
from google import genai
from app.core import settings
from openai import AsyncOpenAI
from google.genai.types import GenerateContentResponse
import textwrap
from app.log_utils import Logger


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
                {"role": "system", "content": textwrap.dedent(system_prompt)},
                {"role": "user", "content": textwrap.dedent(user_prompt)},
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

    async def generate_response(self, session_id: str, model_id: str, prompt: str):
        response: GenerateContentResponse = self.client.models.generate_content(
            model=model_id, contents=[textwrap.dedent(prompt)]
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
            Logger.log_session(
                session_id=session_id,
                message="Warning: No text content found in the non-streaming response.",
                level="WARNING",
            )
            print("Warning: No text content found in the non-streaming response.")
        Logger.log_session(
            session_id=session_id,
            message=json.dumps(
                {
                    "model_id": model_id,
                    "prompt": prompt,
                    "response": str(response),
                    "event": "generate_response",
                }
            ),
            level="INFO",
        )

        return generated_text

    async def generate_next_state(
        self, session_id: str, model_id: str, prompt: str, output_schema: Dict
    ) -> str:
        response: GenerateContentResponse = self.client.models.generate_content(
            model=model_id,
            contents=[textwrap.dedent(prompt)],
            config={
                "response_mime_type": "application/json",
                "response_schema": output_schema,
            },
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
            Logger.log_session(
                session_id=session_id,
                message="Warning: No text content found in the non-streaming response.",
                level="WARNING",
            )
            print("Warning: No text content found in the non-streaming response.")
        Logger.log_session(
            session_id=session_id,
            message=json.dumps(
                {
                    "model_id": model_id,
                    "prompt": prompt,
                    "response": str(response),
                    "event": "generate_next_state",
                }
            ),
            level="INFO",
        )
        return json.loads(generated_text)["state"]
