"""Multi-provider LLM client supporting OpenAI, Anthropic, Gemini, OpenRouter, and local fallback."""
import json
import os
from typing import List, Optional
import httpx
from pydantic import ValidationError

from app.config import settings
from app.llm.schema import DIRECTIVES_JSON_SCHEMA, LLMDirectiveItem, LLMDirectivesExtraction
from app.llm.prompt import SYSTEM_PROMPT, build_user_prompt
from app.llm.rule_based import RuleBasedParser
from app.utils.logging import logger


class LLMClient:
    """Multi-provider client with automated fallback and strict structured output."""

    def __init__(self) -> None:
        self.provider = settings.LLM_PROVIDER.lower()
        self.model = settings.LLM_MODEL
        self.timeout = settings.LLM_TIMEOUT_SECONDS

    async def extract_directives(self, operator_notes: List[str]) -> List[LLMDirectiveItem]:
        """Extract structured directives from operator notes with automated multi-tier fallback."""
        if not operator_notes:
            return []

        # Determine effective provider
        effective_provider = self._resolve_provider()
        logger.info(f"Using LLM provider '{effective_provider}' for {len(operator_notes)} notes")

        if effective_provider == "rule_based":
            return RuleBasedParser.parse_all(operator_notes)

        # Attempt remote LLM invocation
        try:
            if effective_provider == "openai" or effective_provider == "openrouter":
                raw_json = await self._call_openai(operator_notes)
            elif effective_provider == "anthropic":
                raw_json = await self._call_anthropic(operator_notes)
            elif effective_provider == "gemini":
                raw_json = await self._call_gemini(operator_notes)
            else:
                logger.warning(f"Unrecognized provider '{effective_provider}', falling back to rule-based parser")
                return RuleBasedParser.parse_all(operator_notes)

            if raw_json:
                parsed = self._parse_json_response(raw_json, len(operator_notes))
                if parsed:
                    return parsed
        except Exception as e:
            logger.warning(f"Remote LLM call failed with provider '{effective_provider}': {e}. Falling back to RuleBasedParser.")

        # Fallback to rule-based parser
        logger.info("Engaging RuleBasedParser fallback")
        return RuleBasedParser.parse_all(operator_notes)

    def _resolve_provider(self) -> str:
        """Resolve the active LLM provider based on settings and available environment keys."""
        if self.provider != "auto":
            return self.provider

        # Auto-detection priority
        if settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY") or (settings.LLM_API_KEY and "sk-" in settings.LLM_API_KEY):
            return "openai"
        if settings.ANTHROPIC_API_KEY or os.getenv("ANTHROPIC_API_KEY"):
            return "anthropic"
        if settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY"):
            return "gemini"
        if settings.LLM_API_KEY:
            return "openai"

        return "rule_based"

    async def _call_openai(self, notes: List[str]) -> Optional[str]:
        """Invoke OpenAI or OpenRouter API via AsyncOpenAI client."""
        from openai import AsyncOpenAI

        api_key = settings.OPENAI_API_KEY or settings.LLM_API_KEY or os.getenv("OPENAI_API_KEY")
        base_url = settings.LLM_BASE_URL

        client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=self.timeout)
        user_prompt = build_user_prompt(notes)

        response = await client.chat.completions.create(
            model=self.model,
            temperature=settings.LLM_TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content

    async def _call_anthropic(self, notes: List[str]) -> Optional[str]:
        """Invoke Anthropic API via AsyncAnthropic client."""
        from anthropic import AsyncAnthropic

        api_key = settings.ANTHROPIC_API_KEY or os.getenv("ANTHROPIC_API_KEY")
        client = AsyncAnthropic(api_key=api_key, timeout=self.timeout)
        user_prompt = build_user_prompt(notes)

        response = await client.messages.create(
            model=self.model if "claude" in self.model else "claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=settings.LLM_TEMPERATURE,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
        # Extract text content
        text_content = ""
        for block in response.content:
            if hasattr(block, "text"):
                text_content += block.text
        return text_content

    async def _call_gemini(self, notes: List[str]) -> Optional[str]:
        """Invoke Gemini API via REST endpoint."""
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"

        user_prompt = build_user_prompt(notes)
        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": settings.LLM_TEMPERATURE,
                "response_mime_type": "application/json",
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
        return None

    def _parse_json_response(self, raw_text: str, expected_count: int) -> Optional[List[LLMDirectiveItem]]:
        """Parse, validate, and sanitize raw JSON output from LLM."""
        if not raw_text:
            return None

        # Clean markdown codeblocks if present
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
            # Check if wrapped in directives key or direct list
            if isinstance(data, dict) and "directives" in data:
                items_data = data["directives"]
            elif isinstance(data, list):
                items_data = data
            else:
                logger.warning(f"Unexpected LLM JSON structure: {data}")
                return None

            items: List[LLMDirectiveItem] = []
            for item in items_data:
                items.append(LLMDirectiveItem.model_validate(item))

            if len(items) != expected_count:
                logger.warning(f"LLM returned {len(items)} items, expected {expected_count}")
                # If count mismatches, return None to trigger rule-based fallback
                return None

            return items
        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(f"Failed to parse LLM structured output JSON: {e}")
            return None
