"""Email Service

Provides CRUD operations for emails.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.email import Email, StudentEmail, FAQEmail, EmailStatus
# Note: StudentEmail and FAQEmail inherit from Email, demonstrating OOP Inheritance.
from ..models.category import Category
from ..models.factory import EmailFactory
from ..db.supabase_client import get_db


class EmailService:
    """Email service.

    Handles email creation, retrieval, updating, and deletion.
    """

    def __init__(self):
        self._db = get_db()
        self._classification_service = None

    def _get_classification_service(self):
        """Lazily load the classification service."""
        if self._classification_service is None:
            from .classification_service import ClassificationService
            self._classification_service = ClassificationService()
        return self._classification_service

    async def create_email(
        self,
        subject: str,
        body: str,
        sender_email: str,
        sender_name: Optional[str] = None,
        student_id: Optional[str] = None,
        auto_classify: bool = True,
    ) -> Email:
        """Create a new email.

        Args:
            subject: Email subject line.
            body: Email body content.
            sender_email: Sender's email address.
            sender_name: Sender's display name.
            student_id: Student ID (optional).
            auto_classify: Whether to automatically classify the email.

        Returns:
            The created Email object.
        """
        # Create a student email instance
        email = StudentEmail(
            id="",  # Temporary ID, updated after save
            subject=subject,
            body=body,
            sender_email=sender_email,
            sender_name=sender_name,
            student_id=student_id,
        )

        # Save to database
        data = await self._db.create_email(
            subject=subject,
            body=body,
            sender_email=sender_email,
            sender_name=sender_name,
        )

        # Update from database response
        if data:
            email = self._dict_to_email(data)

            # Auto-classify if enabled
            if auto_classify:
                try:
                    classification_service = self._get_classification_service()
                    category = await classification_service.auto_classify(email)
                    if category:
                        email.category = category
                        email.status = EmailStatus.CLASSIFIED
                except Exception as e:
                    print(f"Auto-classification failed: {e}")

        return email

    async def get_emails(
        self,
        status: Optional[str] = None,
        category_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Email]:
        """Retrieve a list of emails with optional filters.

        Args:
            status: Filter by email status.
            category_id: Filter by category ID.
            limit: Maximum number of emails to return.
            offset: Pagination offset.

        Returns:
            A list of Email objects.
        """
        data_list = await self._db.get_emails(
            status=status,
            category_id=category_id,
            limit=limit,
            offset=offset,
        )
        return [self._dict_to_email(data) for data in data_list]

    async def get_email(self, email_id: str) -> Optional[Email]:
        """Retrieve a single email by ID.

        Args:
            email_id: The email ID to look up.

        Returns:
            The Email object, or None if not found.
        """
        data = await self._db.get_email(email_id)
        return self._dict_to_email(data) if data else None

    async def update_status(self, email_id: str, status: EmailStatus) -> bool:
        """Update the status of an email.

        Args:
            email_id: The email ID to update.
            status: The new status.

        Returns:
            True if the update was successful.
        """
        result = await self._db.update_email(email_id, status=status.value)
        return result is not None

    async def update_category(self, email_id: str, category_id: str) -> bool:
        """Update the category of an email.

        Args:
            email_id: The email ID to update.
            category_id: The new category ID.

        Returns:
            True if the update was successful.
        """
        result = await self._db.update_email(
            email_id,
            category_id=category_id,
            status=EmailStatus.CLASSIFIED.value,
        )
        return result is not None

    async def mark_as_duplicate(self, email_id: str) -> bool:
        """Mark an email as a duplicate.

        Args:
            email_id: The email ID to mark.

        Returns:
            True if the update was successful.
        """
        result = await self._db.update_email(email_id, is_duplicate=True)
        return result is not None

    async def count_emails(self, status: Optional[str] = None) -> int:
        """Count emails using an efficient database COUNT query.

        Args:
            status: Optional status filter.

        Returns:
            Number of matching emails.
        """
        return await self._db.count_emails(status=status)

    def _dict_to_email(self, data: Dict[str, Any]) -> Email:
        """Convert a dictionary to an Email subclass instance.

        Delegates to EmailFactory.from_dict for polymorphic object creation
        (Factory Pattern).

        Args:
            data: Dictionary returned from the database.

        Returns:
            An Email or its subclass instance.
        """
        return EmailFactory.from_dict(data)
