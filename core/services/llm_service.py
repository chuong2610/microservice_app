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
        chat_model: str = "gpt-4o-mini",
        embedding_model: str = "text-embedding-3-small",
        azure_endpoint: Optional[str] = None,
        azure_api_version: str = "2024-08-01-preview",
        api_key: Optional[str] = None,
    ) -> None:
        self.provider = provider
        self.chat_model = chat_model
        self.embedding_model = embedding_model
        self.azure_endpoint = azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_api_version = azure_api_version
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if self.provider == "ollama":
            self.ollama_base_url = os.getenv("OLLAMA_BASE_URL")
            self._http = requests.Session()
        elif self.provider == "azure":
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
        else:
            if not self.api_key:
                raise ValueError("Missing OPENAI_API_KEY for OpenAI provider")

            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """Generates chat completion text for given system and user prompts."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if self.provider == "ollama":
            url = f"{self.ollama_base_url}/api/chat"
            payload = {
                "model": self.chat_model or "qwen2.5:3b",
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0.2},
            }
            resp = self._http.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "message" in data and isinstance(data["message"], dict):
                return data["message"].get("content", "")
            if isinstance(data, dict) and "choices" in data and data["choices"]:
                return data["choices"][0].get("message", {}).get("content", "")
            return ""
        else:
            response = self._client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.2,
            )
            return response.choices[0].message.content or ""

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Creates embeddings for a batch of input texts."""
        if not texts:
            return []
        if self.provider == "ollama":
            url = f"{self.ollama_base_url}/api/embeddings"
            model = self.embedding_model or os.getenv("OLLAMA_EMBED_MODEL")
            embeddings: List[List[float]] = []
            
            resp = self._http.post(url, json={"model": model, "input": texts}, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "embedding" in data:
                embeddings.append(data["embedding"])
            elif isinstance(data, dict) and "embeddings" in data and isinstance(data["embeddings"], list):
                embeddings.append(data["embeddings"][0])
            else:
                embeddings.append([])
                
            return embeddings
        else:
            response = self._client.embeddings.create(
                model=self.embedding_model,
                input=texts,
            )
            return [d.embedding for d in response.data]


def build_default_service() -> LLMService:
    """Constructs LLMService from environment variables with sensible defaults."""
    
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "ollama":
        chat_model = os.getenv("LLM_CHAT_MODEL")
        embedding_model = os.getenv("LLM_EMBED_MODEL", os.getenv("OLLAMA_EMBED_MODEL"))
    else:
        chat_model = os.getenv("LLM_CHAT_MODEL")
        embedding_model = os.getenv("LLM_EMBED_MODEL")
    
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    
    return LLMService(
        provider=provider,
        chat_model=chat_model,
        embedding_model=embedding_model,
        azure_endpoint=azure_endpoint,
        azure_api_version=azure_api_version,
    )

