"""DeepSeek API Client

Wraps the DeepSeek Chat API, supporting RAG-style reply generation
with injected knowledge source context.
"""

import httpx
import json
from functools import lru_cache
from typing import List, Optional, Tuple

from ..models.knowledge_source import KnowledgeSource
from ..config import get_settings


class DeepSeekClient:
    """DeepSeek API Client

    Wraps the DeepSeek Chat API, supporting RAG-style reply generation
    with injected knowledge source context.
    """

    # API tuning constants
    DEFAULT_TEMPERATURE: float = 0.7  # Balances creativity and consistency
    DEFAULT_MAX_TOKENS: int = 1000    # Limits response length for concise replies
    API_TIMEOUT_SECONDS: float = 30.0 # Timeout for API HTTP requests

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the DeepSeek client.

        Args:
            api_key: DeepSeek API key. Reads from config if not provided.
        """
        settings = get_settings()
        self.__api_key = api_key or settings.deepseek_api_key
        self.__base_url = settings.deepseek_base_url
        self.__model = settings.deepseek_model

        if not self.__api_key:
            raise ValueError("请配置 DEEPSEEK_API_KEY 环境变量")

    async def generate_reply(
        self,
        email_subject: str,
        email_body: str,
        category_name: str,
        knowledge_sources: Optional[List[KnowledgeSource]] = None,
    ) -> Tuple[str, List[str]]:
        """Generate a reply based on knowledge sources.

        Args:
            email_subject: Email subject line.
            email_body: Email body content.
            category_name: Classification category name.
            knowledge_sources: List of relevant knowledge sources.

        Returns:
            A tuple of (reply content, list of referenced source IDs).
        """
        # Build system prompt with RAG context
        system_prompt = self.__build_system_prompt(category_name, knowledge_sources)

        # Build user message
        user_message = f"邮件主题：{email_subject}\n\n邮件内容：\n{email_body}"

        # Call the API
        response = await self.__call_api(system_prompt, user_message)

        # Collect referenced source IDs
        referenced_ids = [s.id for s in (knowledge_sources or [])]

        return response, referenced_ids

    async def classify_email(
        self,
        email_subject: str,
        email_body: str,
        categories: List[str],
    ) -> str:
        """Classify an email using the LLM.

        Args:
            email_subject: Email subject line.
            email_body: Email body text.
            categories: List of available category names.

        Returns:
            The predicted category name.
        """
        system_prompt = f"""你是一个邮件分类助手。请根据邮件内容，将其归类到以下分类之一：
{', '.join(categories)}

只需要返回分类名称，不要返回其他内容。"""

        user_message = f"邮件主题：{email_subject}\n\n邮件内容：\n{email_body}"

        response = await self.__call_api(system_prompt, user_message)
        return response.strip()

    def __build_system_prompt(
        self,
        category_name: str,
        knowledge_sources: Optional[List[KnowledgeSource]],
    ) -> str:
        """Build the system prompt for reply generation.

        Args:
            category_name: Email category name.
            knowledge_sources: List of relevant knowledge sources.

        Returns:
            The assembled system prompt string.
        """
        # Part 1: Base role definition — defines the AI's identity and behavior rules
        prompt = """你是一位大学教授的邮件助手。你的职责是帮助学生解决问题。

请遵循以下原则：
1. 回复要专业、礼貌、简洁
2. 基于提供的参考资料回答问题
3. 如果参考资料中有相关信息，请引用
4. 如果问题超出资料范围，建议学生联系教授或相关部门
5. 使用中文回复
"""

        # Part 2: Inject knowledge source context (RAG pattern)
        # Retrieved knowledge base entries are appended so the LLM answers based on facts
        if knowledge_sources:
            prompt += "\n\n" + "=" * 50 + "\n"
            prompt += "参考资料（请基于以下资料回答问题）：\n"
            prompt += "=" * 50 + "\n\n"

            # Add each source with numbered labels for easy LLM referencing
            for i, source in enumerate(knowledge_sources, 1):
                prompt += f"【资料 {i}】{source.title}\n"
                prompt += f"{'─' * 40}\n"
                prompt += f"{source.content}\n\n"

        # Part 3: Append category info so the LLM can adjust its response style
        prompt += f"\n邮件分类：{category_name}\n"

        return prompt

    async def __call_api(self, system_prompt: str, user_message: str) -> str:
        """Call the DeepSeek Chat API.

        Args:
            system_prompt: System prompt for the AI assistant.
            user_message: User message content.

        Returns:
            The assistant's reply text from the API.
        """
        # Prepare authentication and content-type headers
        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Content-Type": "application/json",
        }

        # Build the chat completion payload using class constants
        payload = {
            "model": self.__model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": self.DEFAULT_TEMPERATURE,
            "max_tokens": self.DEFAULT_MAX_TOKENS,
        }

        # Use async HTTP client with configurable timeout
        async with httpx.AsyncClient(timeout=self.API_TIMEOUT_SECONDS) as client:
            response = await client.post(
                self.__base_url,
                headers=headers,
                json=payload,
            )

            # Handle non-200 responses — extract error message from JSON body if available
            if response.status_code != 200:
                error_msg = f"DeepSeek API error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = f"{error_msg} - {error_data.get('error', {}).get('message', '')}"
                except Exception:
                    pass
                raise RuntimeError(error_msg)

            # Extract the assistant's reply from the choices array
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def test_connection(self) -> bool:
        """Test the API connection.

        Returns:
            True if the connection is successful, False otherwise.
        """
        try:
            response = await self.__call_api(
                "你是一个助手。",
                "请回复 'OK' 表示连接成功。",
            )
            return "OK" in response or "ok" in response.lower()
        except Exception:
            return False

    async def chat_edit_reply(
        self,
        current_reply: str,
        user_instruction: str,
    ) -> str:
        """Edit a reply based on user instructions via conversational AI.

        Args:
            current_reply: The current reply content.
            user_instruction: User instruction (e.g., "reply in English").

        Returns:
            The modified reply content.
        """
        system_prompt = """你是一个邮件回复编辑助手。
用户会给你指令来修改当前的回复内容。
请根据用户指令调整回复，保持专业和礼貌。
只输出修改后的完整回复内容，不要解释。"""

        user_message = f"""当前回复内容：
{current_reply}

用户指令：{user_instruction}

请输出修改后的完整回复内容："""

        return await self.__call_api(system_prompt, user_message)


# Module-level registry for backend swapping (demo mode)
_llm_backend = None


def set_llm_backend(client) -> None:
    """Set the LLM backend.

    Used by demo mode to inject TemplateLLMClient before any services
    are instantiated. When set, all get_llm_client() calls return the
    injected client instead of DeepSeekClient.

    Args:
        client: An LLM client with the same method signatures as DeepSeekClient.
    """
    global _llm_backend
    _llm_backend = client


def get_llm_client() -> DeepSeekClient:
    """Get the LLM client.

    Returns the injected backend if set (demo mode),
    otherwise returns a DeepSeekClient instance.
    """
    if _llm_backend is not None:
        return _llm_backend
    return DeepSeekClient()
