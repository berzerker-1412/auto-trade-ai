"""MiniMax Chat Completion Client — OpenAI-compatible API"""

import os
import json
import requests
from typing import List, Dict, Any, Optional


class MiniMaxChatClient:
    """
    MiniMax Chat Completions — OpenAI-compatible endpoint.

    Base URL: https://api.minimax.io/v1
    Model: MiniMax-Text-01 or MiniMax-M2.5

    Environment vars:
        MINIMAX_API_KEY — from ~/.hermes/.env
        MINIMAX_BASE_URL — default: https://api.minimax.io/v1
        MINIMAX_MODEL_NAME — default: MiniMax-Text-01
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY", "")
        self.base_url = base_url or os.getenv("MINIMAX_BASE_URL", "https://api.minimax.io/v1")
        self.model = model or os.getenv("MINIMAX_MODEL_NAME", "MiniMax-Text-01")

        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY is required")

    def _post(
        self,
        endpoint: str,
        body: Dict[str, Any],
        timeout: int = 60,
    ) -> Dict[str, Any]:
        """POST to MiniMax OpenAI-compatible endpoint"""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(url, json=body, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()

    def chat_completions_create(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1024,
        response_format: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a chat completion (OpenAI-compatible).

        คล้าย OpenAI SDK: client.chat.completions.create(
            messages=[...], model="...", temperature=0.3
        )
        """
        body: Dict[str, Any] = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            body["response_format"] = response_format

        # MiniMax supports additional params
        if "top_p" in kwargs:
            body["top_p"] = kwargs["top_p"]
        if "stream" in kwargs:
            body["stream"] = kwargs["stream"]

        return self._post("chat/completions", body)

    def create(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1024,
        response_format: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Alias สำหรับ chat_completions_create — คล้าย OpenAI SDK"""
        return self.chat_completions_create(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
            **kwargs,
        )
