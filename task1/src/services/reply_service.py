"""Reply Service

Provides reply generation, review, and management functionality.
"""

from typing import List, Optional, Tuple
from datetime import datetime

from ..models.email import Email, EmailStatus
from ..models.reply import Reply
from ..models.knowledge_source import KnowledgeSource
from ..models.strategies import ReplyStrategy, AutoReplyStrategy, ManualReplyStrategy
from ..models.category import Category
from ..models.factory import EmailFactory
from ..db.supabase_client import get_db
from ..llm.deepseek_client import get_llm_client
from .knowledge_service import KnowledgeService


class ReplyService:
    """Reply service.

    Handles reply generation, review, and sending.
    Uses the Strategy Pattern to support different reply generation methods.
    """

    def __init__(self):
        # Composition: ReplyService composes multiple independent service objects
        # to build complex reply generation functionality.
        self._db = get_db()
        self._llm = get_llm_client()
        self._knowledge_service = KnowledgeService()
        self._strategy: ReplyStrategy = AutoReplyStrategy(self._llm, knowledge_sources=[], category_name="其他")

    def set_strategy(self, strategy: ReplyStrategy):
        """Set the reply generation strategy.

        Switching strategy objects enables different reply generation methods (Polymorphism).
        Example: set_strategy(ManualReplyStrategy("manual reply content"))

        Args:
            strategy: A ReplyStrategy instance (AutoReplyStrategy or ManualReplyStrategy).
        """
        self._strategy = strategy

    async def generate_reply(
        self,
        email: Email,
        use_knowledge_sources: bool = True,
        top_k_sources: int = 3,
        force_regenerate: bool = False,
    ) -> Reply:
        """Generate a reply for an email.

        Uses the Strategy Pattern via self._strategy (a ReplyStrategy subclass)
        to achieve polymorphic reply generation:
        - AutoReplyStrategy: LLM + knowledge base automatic reply
        - ManualReplyStrategy: Pre-written manual reply

        Args:
            email: The email to reply to.
            use_knowledge_sources: Whether to search for relevant knowledge sources.
            top_k_sources: Maximum number of knowledge sources to use.
            force_regenerate: Whether to regenerate even if a reply exists.

        Returns:
            The generated Reply object.
        """
        # Check for existing reply
        existing_reply = await self.get_reply_by_email(email.id)
        if existing_reply and not force_regenerate:
            return existing_reply

        # Retrieve relevant knowledge sources for AutoReplyStrategy
        knowledge_sources: List[KnowledgeSource] = []
        if use_knowledge_sources:
            email_content = f"{email.subject} {email.body}"
            scored_sources = await self._knowledge_service.search_relevant_sources(
                email_content,
                top_k=top_k_sources,
                min_score=0.1,
            )
            knowledge_sources = [source for source, _ in scored_sources]

        # Get the category name
        category_name = email.category.name if email.category else "其他"

        # Update the strategy's context via its public method (preserves encapsulation)
        if isinstance(self._strategy, AutoReplyStrategy):
            self._strategy.update_context(
                knowledge_sources=knowledge_sources,
                category_name=category_name,
            )

        # Generate reply through strategy pattern (Polymorphism: same interface, different implementations)
        reply = await self._strategy.generate(email)

        # Save to database
        data = await self._db.create_reply(
            email_id=email.id,
            content=reply.content,
            is_auto=reply.is_auto,
            referenced_sources=reply.referenced_sources,
        )

        if data:
            reply.id = data["id"]

        return reply

    async def get_reply(self, reply_id: str) -> Optional[Reply]:
        """Retrieve a reply by ID.

        Args:
            reply_id: The reply ID.

        Returns:
            The Reply object, or None if not found.
        """
        data = await self._db.get_reply_by_id(reply_id)
        if not data:
            return None
        return self._dict_to_reply(data)

    async def get_reply_by_email(self, email_id: str) -> Optional[Reply]:
        """Retrieve the reply for a specific email.

        Args:
            email_id: The email ID.

        Returns:
            The Reply object, or None if no reply exists.
        """
        data = await self._db.get_reply_by_email(email_id)
        if not data:
            return None

        return self._dict_to_reply(data)

    async def update_reply(
        self,
        reply_id: str,
        content: Optional[str] = None,
    ) -> Optional[Reply]:
        """Update a reply's content.

        Args:
            reply_id: The reply ID to update.
            content: The new content.

        Returns:
            The updated Reply object, or None on failure.
        """
        if content is None:
            return None

        data = await self._db.update_reply(reply_id, content=content)
        return self._dict_to_reply(data) if data else None

    async def approve_reply(self, reply_id: str) -> bool:
        """Approve a reply.

        Args:
            reply_id: The reply ID to approve.

        Returns:
            True if the approval was successful.
        """
        return await self._db.approve_reply(reply_id)

    async def reject_reply(self, reply_id: str) -> bool:
        """Reject a reply (marks it as unapproved for regeneration).

        Args:
            reply_id: The reply ID to reject.

        Returns:
            True if the rejection was successful.
        """
        data = await self._db.update_reply(reply_id, is_approved=False)
        return data is not None

    async def regenerate_reply(
        self,
        email: Email,
        old_reply_id: str,
    ) -> Reply:
        """Regenerate a reply by deleting the old one and creating a new one.

        Args:
            email: The email object.
            old_reply_id: The ID of the old reply to replace.

        Returns:
            The newly generated Reply.
        """
        # Delete the old reply
        await self._db.delete_reply(old_reply_id)

        # Force regeneration
        return await self.generate_reply(email, force_regenerate=True)

    async def send_reply(self, reply_id: str) -> Optional[dict]:
        """Send a reply: auto-approve if needed, then mark the email as sent.

        All database operations are performed through the service layer
        instead of direct database access from the API.

        Args:
            reply_id: The reply ID to send.

        Returns:
            A dict with email_id and sent_at, or None if the reply is not found.
        """
        reply = await self.get_reply(reply_id)
        if not reply:
            return None

        # Auto-approve if not yet approved
        await self._db.approve_reply(reply_id)

        # Update email status to "sent"
        sent_at = datetime.now().isoformat()
        if reply.email_id:
            await self._db.update_email(reply.email_id, status="sent")

        return {"email_id": reply.email_id, "sent_at": sent_at}

    async def get_pending_replies(self, limit: int = 50) -> List[Tuple[Email, Reply]]:
        """Retrieve replies that are pending professor review.

        Args:
            limit: Maximum number of results.

        Returns:
            A list of (Email, Reply) tuples awaiting review.
        """
        # Get classified but unreviewed emails
        emails = await self._db.get_emails(status="replied", limit=limit)

        result = []
        for email_data in emails:
            email = self._dict_to_email(email_data)
            reply_data = await self._db.get_reply_by_email(email.id)

            if reply_data and not reply_data.get("is_approved"):
                reply = self._dict_to_reply(reply_data)
                result.append((email, reply))

        return result

    def _dict_to_reply(self, data: dict) -> Reply:
        """Convert a dictionary to a Reply object."""
        reply = Reply(
            content=data["content"],
            is_auto=data.get("is_auto", True),
            email_id=data.get("email_id"),
            referenced_sources=data.get("referenced_sources", []),
        )
        reply.id = data["id"]
        reply.approved = data.get("is_approved", False)
        return reply

    def _dict_to_email(self, data: dict):
        """Convert a dictionary to an Email subclass object.

        Delegates to EmailFactory.from_dict for polymorphic object creation
        (Factory Pattern).
        """
        return EmailFactory.from_dict(data)
