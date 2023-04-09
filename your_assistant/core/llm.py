"""Core logic of custom LLMs.
"""
import os
from typing import List, Optional

import openai
from Bard import Chatbot as BardChat
from langchain.llms.base import LLM
from revChatGPT.V1 import Chatbot


class ChatGPT(LLM):
    test_mode: bool = False
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.1

    @property
    def _llm_type(self) -> str:
        return "ChatGPT"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
    ) -> str:
        """Call the LLM. In test mode, return a test response.

        Args:
            prompt (str): The prompt to the LLM.
            stop (Optional[List[str]]): The stop tokens. Will be ignored.

        Returns:
            str: The response from the LLM.
        """
        response = ""
        if self.test_mode:
            response = "This is a test chatgpt response."
            return response

        # Check token availability.
        access_token = os.getenv("OPENAI_API_KEY")
        if not access_token:
            return "Please set OPENAI_API_KEY before chatting with ChatGPT."

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content  # type: ignore


class RevChatGPT(LLM):
    test_mode: bool = False

    @property
    def _llm_type(self) -> str:
        return "RevChatGPT"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call the LLM. In test mode, return a test response.

        Args:
            prompt (str): The prompt to the LLM.
            stop (Optional[List[str]]): The stop tokens. Will be ignored.

        Returns:
            str: The response from the LLM.
        """
        response = ""
        if self.test_mode:
            response = "This is a test revchatgpt response."
            return response

        # Check token availability.
        access_token = os.getenv("CHATGPT_ACCESS_TOKEN")
        if not access_token:
            return "Please set CHATGPT_ACCESS_TOKEN before chatting with ChatGPT."

        chatgpt = Chatbot(
            config={
                "access_token": access_token,
            }
        )
        for data in chatgpt.ask(prompt):
            response = data["message"]
        return response


class RevBard(LLM):
    test_mode: bool = False

    @property
    def _llm_type(self) -> str:
        return "RevBard"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call the LLM. In test mode, return a test response.

        Args:
            prompt (str): The prompt to the LLM.
            stop (Optional[List[str]]): The stop tokens. Will be ignored.

        Returns:
            str: The response from the LLM.
        """
        response = ""
        if self.test_mode:
            response = "This is a test revbard response."
            return response

        # Check token availability.
        access_token = os.getenv("BARD_SESSION_TOKEN")
        if not access_token:
            return "Please set BARD_SESSION_TOKEN before chatting with Bard."

        bard = BardChat(session_id=os.getenv("BARD_SESSION_TOKEN"))
        response = bard.ask(message=prompt)
        return response["content"]  # type: ignore