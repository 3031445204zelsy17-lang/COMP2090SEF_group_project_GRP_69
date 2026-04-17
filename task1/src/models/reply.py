"""Reply Model

Defines the email reply model for storing auto-generated and manual replies.
"""

from datetime import datetime
from typing import List, Optional


class Reply:
    """Email reply class.

    Represents a reply to an email, which can be auto-generated or manually written.
    """

    def __init__(
        self,
        content: str,
        is_auto: bool = True,
        email_id: Optional[str] = None,
        referenced_sources: Optional[List[str]] = None,
    ):
        """Initialize a reply.

        Args:
            content: Reply body content.
            is_auto: Whether this is an auto-generated reply.
            email_id: ID of the email this reply belongs to.
            referenced_sources: List of knowledge source IDs referenced in this reply.
        """
        self.__id = None  # Set when saved to database
        self.__content = content
        self.__is_auto = is_auto
        self.__approved = False
        self.__email_id = email_id
        self.__referenced_sources = referenced_sources or []
        self.__rejection_reason: Optional[str] = None
        self.__timestamp = datetime.now()

    @property
    def id(self) -> Optional[str]:
        """Get the reply ID."""
        return self.__id

    @id.setter
    def id(self, value: str) -> None:
        """Set the reply ID."""
        self.__id = value

    @property
    def content(self) -> str:
        """Get the reply content."""
        return self.__content

    @content.setter
    def content(self, value: str) -> None:
        """Set the reply content."""
        self.__content = value

    @property
    def is_auto(self) -> bool:
        """Check whether this is an auto-generated reply."""
        return self.__is_auto

    @property
    def approved(self) -> bool:
        """Check whether the reply has been approved."""
        return self.__approved

    @approved.setter
    def approved(self, value: bool) -> None:
        """Set the approval status."""
        self.__approved = value

    @property
    def email_id(self) -> Optional[str]:
        """Get the associated email ID."""
        return self.__email_id

    @property
    def referenced_sources(self) -> List[str]:
        """Get a copy of the referenced source IDs."""
        return self.__referenced_sources.copy()

    @property
    def timestamp(self) -> datetime:
        """Get the reply timestamp."""
        return self.__timestamp

    @property
    def rejection_reason(self) -> Optional[str]:
        """Get the rejection reason, if any."""
        return self.__rejection_reason

    def set_rejection_reason(self, reason: str) -> None:
        """Set the rejection reason.

        Args:
            reason: The reason for rejecting this reply.
        """
        self.__rejection_reason = reason

    def add_referenced_source(self, source_id: str) -> None:
        """Add a referenced knowledge source.

        Args:
            source_id: The knowledge source ID to add.
        """
        if source_id not in self.__referenced_sources:
            self.__referenced_sources.append(source_id)

    def __repr__(self) -> str:
        return f"Reply(id={self.__id!r}, is_auto={self.__is_auto}, approved={self.__approved})"

    def to_dict(self) -> dict:
        """Convert the reply to a dictionary.

        Returns:
            A dictionary containing all reply fields.
        """
        return {
            "id": self.__id,
            "content": self.__content,
            "is_auto": self.__is_auto,
            "approved": self.__approved,
            "email_id": self.__email_id,
            "referenced_sources": self.__referenced_sources,
            "rejection_reason": self.__rejection_reason,
            "timestamp": self.__timestamp.isoformat(),
        }
