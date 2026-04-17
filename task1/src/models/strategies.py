"""Reply Strategy Implementations

Implements concrete reply generation strategies, demonstrating
OOP Polymorphism concept.
- AutoReplyStrategy: LLM + knowledge base powered automatic reply
- TemplateReplyStrategy: Template-based automatic reply
- ManualReplyStrategy: Professor-edited manual reply
"""

from datetime import datetime
from typing import Optional, List, Dict, TYPE_CHECKING

from .base import ReplyStrategy
from .reply import Reply

if TYPE_CHECKING:
    from .email import Email
    from .knowledge_source import KnowledgeSource


class AutoReplyStrategy(ReplyStrategy):
    """Auto-reply strategy.

    Generates replies using an LLM combined with knowledge base context.
    """

    def __init__(
        self,
        llm_client,
        knowledge_sources: Optional[List["KnowledgeSource"]] = None,
        category_name: str = "其他",
    ):
        # Composition: AutoReplyStrategy "has-a" llm_client and knowledge_sources,
        # combining independent objects to build complex behavior.
        self._llm_client = llm_client
        self._knowledge_sources = knowledge_sources or []
        self._category_name = category_name

    async def generate(self, email: "Email") -> Reply:
        """Generate a reply using LLM and knowledge base context."""
        content, referenced_ids = await self._llm_client.generate_reply(
            email_subject=email.subject,
            email_body=email.body,
            category_name=self._category_name,
            knowledge_sources=self._knowledge_sources,
        )

        return Reply(
            content=content,
            is_auto=True,
            email_id=email.id,
            referenced_sources=referenced_ids,
        )

    def get_strategy_name(self) -> str:
        return "AutoReply (LLM + Knowledge Base)"

    def update_context(
        self,
        knowledge_sources: Optional[List["KnowledgeSource"]] = None,
        category_name: Optional[str] = None,
    ) -> None:
        """Update the strategy's context for the next generation call.

        Provides a controlled interface for modifying internal state,
        preserving encapsulation by avoiding direct attribute access.

        Args:
            knowledge_sources: Updated list of relevant knowledge sources.
            category_name: Updated category name for prompt context.
        """
        if knowledge_sources is not None:
            self._knowledge_sources = knowledge_sources
        if category_name is not None:
            self._category_name = category_name


class TemplateReplyStrategy(ReplyStrategy):
    """Template reply strategy.

    Generates replies using pre-defined templates. Selects a template
    based on the email's category and fills in placeholders.
    Demonstrates OOP Polymorphism — shares the same ReplyStrategy interface
    as AutoReplyStrategy and ManualReplyStrategy, but uses a completely
    different reply generation approach.
    """

    # Default templates for each category type
    DEFAULT_TEMPLATES: Dict[str, str] = {
        "academic": (
            "Dear Student,\n\n"
            "Thank you for your academic inquiry about {subject}. "
            "Please refer to the course materials and lecture notes for more details. "
            "If you need further assistance, feel free to visit during office hours.\n\n"
            "Best regards"
        ),
        "administrative": (
            "Dear Student,\n\n"
            "Thank you for your administrative request about {subject}. "
            "Please visit the university administration office or check the student portal "
            "for the relevant forms and procedures.\n\n"
            "Best regards"
        ),
        "faq": (
            "Dear Student,\n\n"
            "Your question about {subject} is a frequently asked question. "
            "You may find the answer in the course FAQ section. "
            "If you still have questions, please do not hesitate to ask.\n\n"
            "Best regards"
        ),
        "default": (
            "Dear Student,\n\n"
            "Thank you for your email about {subject}. "
            "We will get back to you as soon as possible.\n\n"
            "Best regards"
        ),
    }

    def __init__(
        self,
        templates: Optional[Dict[str, str]] = None,
        category_name: str = "default",
    ):
        """Initialize the template reply strategy.

        Args:
            templates: Custom template dictionary. Keys are category names,
                       values are template strings with {subject} placeholder.
                       Falls back to DEFAULT_TEMPLATES if not provided.
            category_name: The email's classification category name.
        """
        self._templates = templates or self.DEFAULT_TEMPLATES
        self._category_name = category_name

    async def generate(self, email: "Email") -> Reply:
        """Generate a reply by selecting and filling a template.

        Args:
            email: The email to reply to.

        Returns:
            A Reply object with the template-filled content.
        """
        # Select template by category name, fall back to default
        template = self._templates.get(
            self._category_name.lower(),
            self._templates["default"],
        )
        # Fill in the email subject as context
        content = template.format(subject=email.subject)

        return Reply(
            content=content,
            is_auto=True,
            email_id=email.id,
        )

    def get_strategy_name(self) -> str:
        return f"TemplateReply (category={self._category_name})"


class ManualReplyStrategy(ReplyStrategy):
    """Manual reply strategy.

    Used for replies manually edited by the professor.
    """

    def __init__(self, content: str):
        self._content = content

    async def generate(self, email: "Email") -> Reply:
        """Return the manually written reply content."""
        return Reply(
            content=self._content,
            is_auto=False,
            email_id=email.id,
        )

    def get_strategy_name(self) -> str:
        return "ManualReply"
