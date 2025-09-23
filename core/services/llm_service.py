"""LLM service abstraction supporting OpenAI, Azure OpenAI, and Ollama for chat and embeddings."""

from typing import List, Literal, Optional, Dict, Any
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    """Provides chat completion and embeddings with OpenAI, Azure OpenAI, or Ollama."""

    def __init__(
        self,
        provider: Literal["openai", "azure", "ollama"] = "openai",
        chat_model: Optional[str] = None,
        embedding_model: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        azure_api_version: str = "2024-08-01-preview",
        api_key: Optional[str] = None,
    ) -> None:
        self.provider = provider
        
        # Set default models based on provider
        if provider == "ollama":
            self.chat_model = chat_model or os.getenv("OLLAMA_CHAT_MODEL")
            self.embedding_model = embedding_model or os.getenv("OLLAMA_EMBED_MODEL")
        elif provider == "azure":
            self.chat_model = chat_model or os.getenv("AZURE_OPENAI_CHAT_MODEL")
            self.embedding_model = embedding_model or os.getenv("AZURE_OPENAI_EMBED_MODEL")
            self.azure_endpoint = azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
            self.azure_api_version = azure_api_version or os.getenv("AZURE_OPENAI_API_VERSION")
            self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        else:
            self.chat_model = chat_model or os.getenv("OPENAI_CHAT_MODEL")
            self.embedding_model = embedding_model or os.getenv("OPENAI_EMBED_MODEL")
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if self.provider == "azure":
            if not self.azure_api_key:
                raise ValueError("Missing AZURE_OPENAI_API_KEY for Azure provider")
            if not self.azure_endpoint:
                raise ValueError("Missing AZURE_OPENAI_ENDPOINT for Azure provider")
            from openai import AzureOpenAI
            self._client = AzureOpenAI(
                api_key=self.azure_api_key,
                api_version=self.azure_api_version,
                azure_endpoint=self.azure_endpoint,
            )
            self._mode = "azure"
        elif self.provider == "ollama":
            # Use OpenAI-compatible SDK against Ollama's /v1
            self.ollama_base_url = os.getenv("OLLAMA_BASE_URL")
            # print(f"DEBUG: Ollama using chat_model={self.chat_model}, embedding_model={self.embedding_model}")
            from openai import OpenAI
            self._client = OpenAI(
                base_url=f"{self.ollama_base_url}/v1",
                api_key="ollama"  # any non-empty string works
            )
            self._mode = "openai_like"
        else:
            if not self.api_key:
                raise ValueError("Missing OPENAI_API_KEY for OpenAI provider")
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
            self._mode = "openai_like"

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """Generates chat completion text for given system and user prompts."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if self._mode == "azure":
            resp = self._client.chat.completions.create(
                model=self.chat_model, messages=messages, temperature=0.2
            )
            return (resp.choices[0].message.content or "").strip()

        # OpenAI-compatible (OpenAI & Ollama)
        # 1) Try chat/completions
        try:
            resp = self._client.chat.completions.create(
                model=self.chat_model, messages=messages, temperature=0.2
            )
            choice0 = resp.choices[0]
            content = getattr(getattr(choice0, "message", None), "content", None)
            # Some servers may also populate .text on chat responses
            text = getattr(choice0, "text", None)

            if content and content.strip():
                return content.strip()
            if text and text.strip():
                return text.strip()
            # If we got here, the route worked but it returned nothing useful → fall back.
        except Exception as e:
            print(f"DEBUG: chat.completions failed: {e}")

        # 2) Fallback: classic completions (prompt)
        try:
            prompt = f"{system_prompt}\n\n{user_prompt}".strip()
            resp = self._client.completions.create(
                model=self.chat_model, prompt=prompt, temperature=0.2
            )
            choice0 = resp.choices[0]
            text = getattr(choice0, "text", None)
            if text and text.strip():
                return text.strip()
            msg = getattr(choice0, "message", None)
            if msg and getattr(msg, "content", None):
                return msg.content.strip()
        except Exception as e:
            print(f"DEBUG: completions fallback failed: {e}")

        return ""

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Creates embeddings for a batch of input texts."""
        if not texts:
            return []
        
        if self.provider == "azure":
            response = self._client.embeddings.create(
                model=self.embedding_model,
                input=texts,
            )
            return [d.embedding for d in response.data]

        # OpenAI-compatible (OpenAI & Ollama)
        try:
            r = self._client.embeddings.create(model=self.embedding_model, input=texts)
            return [d.embedding for d in r.data]
        except Exception:
            # If the server lacks /v1/embeddings, return empty vectors (same shape as texts)
            return [[] for _ in texts]


def build_default_service() -> LLMService:
    """Constructs LLMService from environment variables with sensible defaults."""
    
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "ollama":
        chat_model = os.getenv("LLM_CHAT_MODEL", "qwen2.5:3b")
        embedding_model = os.getenv("LLM_EMBED_MODEL", os.getenv("OLLAMA_EMBED_MODEL", "bge-m3"))
    else:
        chat_model = os.getenv("LLM_CHAT_MODEL", "gpt-4o-mini")
        embedding_model = os.getenv("LLM_EMBED_MODEL", "text-embedding-3-small")
    
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    
    return LLMService(
        provider=provider,
        chat_model=chat_model,
        embedding_model=embedding_model,
        azure_endpoint=azure_endpoint,
        azure_api_version=azure_api_version,
    )

