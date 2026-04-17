"""Email Model

Defines email-related classes using inheritance to support different email types.
"""

from datetime import datetime
from typing import Optional
from enum import Enum

from .base import AbstractEmail


class EmailStatus(str, Enum):
    """Email status enumeration."""

    PENDING = "pending"          # Awaiting processing
    CLASSIFIED = "classified"    # Category assigned
    REPLIED = "replied"          # Reply generated
    APPROVED = "approved"        # Reply approved by professor
    SENT = "sent"                # Reply sent to student


class Email(AbstractEmail):
    """Email class.

    Inherits from AbstractEmail and implements full email functionality.
    """

    def __init__(
        self,
        id: str,
        subject: str,
        body: str,
        sender_email: str,
        sender_name: Optional[str] = None,
        status: EmailStatus = EmailStatus.PENDING,
    ):
        """Initialize an email.

        Args:
            id: Unique email identifier.
            subject: Email subject line.
            body: Email body content.
            sender_email: Sender's email address.
            sender_name: Sender's display name.
            status: Current email status.
        """
        super().__init__(id, subject, body, sender_email, sender_name)
        self.__status = status
        self.__category = None  # Composition: Email "has-a" Category
        self.__reply = None     # Composition: Email "has-a" Reply
        self.__is_duplicate = False

    @property
    def status(self) -> EmailStatus:
        """Get the email status."""
        return self.__status

    @status.setter
    def status(self, value: EmailStatus) -> None:
        """Set the email status."""
        self.__status = value

    @property
    def category(self):
        """Get the assigned category."""
        return self.__category

    @category.setter
    def category(self, value) -> None:
        """Set the category."""
        self.__category = value

    @property
    def reply(self):
        """Get the associated reply."""
        return self.__reply

    @reply.setter
    def reply(self, value) -> None:
        """Set the reply."""
        self.__reply = value

    @property
    def is_duplicate(self) -> bool:
        """Check whether this email is a duplicate."""
        return self.__is_duplicate

    @is_duplicate.setter
    def is_duplicate(self, value: bool) -> None:
        """Set the duplicate flag."""
        self.__is_duplicate = value

    def to_dict(self) -> dict:
        """Convert the email to a dictionary.

        Returns:
            A dictionary containing all email fields.
        """
        return {
            "id": self.id,
            "subject": self.subject,
            "body": self.body,
            "sender_email": self.sender_email,
            "sender_name": self.sender_name,
            "status": self.status.value,
            "category": self.category.name if self.category else None,
            "is_duplicate": self.is_duplicate,
            "timestamp": self.timestamp.isoformat(),
        }


class StudentEmail(Email):
    """Student email class.

    Inherits from Email, representing an email sent by a student.
    """

    def __init__(
        self,
        id: str,
        subject: str,
        body: str,
        sender_email: str,
        sender_name: Optional[str] = None,
        student_id: Optional[str] = None,
    ):
        """Initialize a student email.

        Args:
            id: Unique email identifier.
            subject: Email subject line.
            body: Email body content.
            sender_email: Sender's email address.
            sender_name: Sender's display name.
            student_id: Student ID number.
        """
        super().__init__(id, subject, body, sender_email, sender_name)
        self.__student_id = student_id

    @property
    def student_id(self) -> Optional[str]:
        """Get the student ID."""
        return self.__student_id


class FAQEmail(Email):
    """FAQ email class.

    Inherits from Email, representing a frequently asked question (duplicate).
    """

    def __init__(
        self,
        id: str,
        subject: str,
        body: str,
        sender_email: str,
        sender_name: Optional[str] = None,
        faq_id: Optional[str] = None,
    ):
        """Initialize a FAQ email.

        Args:
            id: Unique email identifier.
            subject: Email subject line.
            body: Email body content.
            sender_email: Sender's email address.
            sender_name: Sender's display name.
            faq_id: Associated FAQ entry ID.
        """
        super().__init__(id, subject, body, sender_email, sender_name)
        self.__faq_id = faq_id
        self.is_duplicate = True  # FAQ emails are duplicates by default

    @property
    def faq_id(self) -> Optional[str]:
        """Get the associated FAQ ID."""
        return self.__faq_id

    @faq_id.setter
    def faq_id(self, value: str) -> None:
        """Set the associated FAQ ID."""
        self.__faq_id = value
