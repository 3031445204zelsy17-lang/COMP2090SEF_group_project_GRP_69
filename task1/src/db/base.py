"""Database Client Abstract Base Class

Defines the common interface for all database backends.
SupabaseClient and SqliteClient both implement this interface,
demonstrating OOP Abstraction and Polymorphism.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class DatabaseClient(ABC):
    """Abstract base class for database operations.

    Defines a common interface that both SupabaseClient (online)
    and SqliteClient (offline demo) must implement.
    Demonstrates OOP Abstraction concept.
    """

    # ==================== User Operations ====================

    @abstractmethod
    async def create_user(
        self,
        name: str,
        email: str,
        role: str,
        password_hash: str,
    ) -> Dict[str, Any]:
        """Create a new user."""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user by email address."""
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user by ID."""
        pass

    # ==================== Category Operations ====================

    @abstractmethod
    async def get_categories(self) -> List[Dict[str, Any]]:
        """Retrieve all categories ordered by priority."""
        pass

    @abstractmethod
    async def create_category(
        self,
        name: str,
        priority: int,
        keywords: List[str],
    ) -> Dict[str, Any]:
        """Create a new category."""
        pass

    # ==================== Knowledge Source Operations ====================

    @abstractmethod
    async def get_knowledge_sources(self) -> List[Dict[str, Any]]:
        """Retrieve all knowledge sources."""
        pass

    @abstractmethod
    async def get_knowledge_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single knowledge source by ID."""
        pass

    @abstractmethod
    async def create_knowledge_source(
        self,
        title: str,
        content: str,
        keywords: List[str],
        category: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new knowledge source."""
        pass

    @abstractmethod
    async def update_knowledge_source(
        self,
        source_id: str,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        """Update a knowledge source."""
        pass

    @abstractmethod
    async def delete_knowledge_source(self, source_id: str) -> bool:
        """Delete a knowledge source."""
        pass

    # ==================== Email Operations ====================

    @abstractmethod
    async def get_emails(
        self,
        status: Optional[str] = None,
        category_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Retrieve emails with optional filters."""
        pass

    @abstractmethod
    async def get_email(self, email_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single email by ID."""
        pass

    @abstractmethod
    async def create_email(
        self,
        subject: str,
        body: str,
        sender_email: str,
        sender_name: Optional[str] = None,
        category_id: Optional[str] = None,
        is_duplicate: bool = False,
    ) -> Dict[str, Any]:
        """Create a new email."""
        pass

    @abstractmethod
    async def update_email(
        self,
        email_id: str,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        """Update an email."""
        pass

    @abstractmethod
    async def count_emails(self, status: Optional[str] = None) -> int:
        """Count emails."""
        pass

    # ==================== Reply Operations ====================

    @abstractmethod
    async def get_reply_by_id(self, reply_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a reply by ID."""
        pass

    @abstractmethod
    async def get_reply_by_email(self, email_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the reply for a specific email."""
        pass

    @abstractmethod
    async def create_reply(
        self,
        email_id: str,
        content: str,
        is_auto: bool = True,
        referenced_sources: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new reply."""
        pass

    @abstractmethod
    async def update_reply(
        self,
        reply_id: str,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        """Update a reply."""
        pass

    @abstractmethod
    async def approve_reply(self, reply_id: str) -> bool:
        """Approve a reply."""
        pass

    @abstractmethod
    async def delete_reply(self, reply_id: str) -> bool:
        """Delete a reply."""
        pass

    # ==================== Statistics Operations ====================

    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Retrieve system-wide statistics."""
        pass
