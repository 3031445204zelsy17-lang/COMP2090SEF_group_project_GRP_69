"""Supabase Database Client

Wraps all Supabase (PostgreSQL) database operations.
Uses the Singleton Pattern to ensure only one database connection instance.
Inherits from DatabaseClient abstract base class for backend swapping.
"""

import asyncio
from typing import Optional, List, Any, Dict
from datetime import datetime
import os

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

from .base import DatabaseClient
from ..config import get_settings


class SupabaseClient(DatabaseClient):
    """Supabase database client.

    Uses the Singleton Pattern to ensure a single database connection instance.
    Inherits from DatabaseClient for backend swapping (Polymorphism).
    """

    __instance: Optional["SupabaseClient"] = None
    __client: Optional[Client] = None

    def __new__(cls) -> "SupabaseClient":
        """Singleton Pattern implementation.

        Ensures only one database connection instance exists globally,
        avoiding redundant connections. The instance is created on the
        first call and reused on subsequent calls.
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        """Initialize the database connection.

        Since __new__ may be called multiple times but only creates one
        instance, we check self.__client here to avoid re-initialization.
        """
        if self.__client is not None:
            return

        if not SUPABASE_AVAILABLE:
            raise ImportError("Please install supabase: pip install supabase")

        settings = get_settings()

        if not settings.supabase_url or not settings.supabase_key:
            raise ValueError(
                "Please configure SUPABASE_URL and SUPABASE_KEY in the .env file"
            )

        self.__client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )

    @property
    def client(self) -> Client:
        """Get the Supabase client instance."""
        if self.__client is None:
            raise RuntimeError("Database connection not initialized")
        return self.__client

    # ==================== User Operations ====================

    async def create_user(
        self,
        name: str,
        email: str,
        role: str,
        password_hash: str,
    ) -> Dict[str, Any]:
        """Create a new user.

        Args:
            name: User's full name.
            email: User's email address.
            role: User's role (e.g., "professor", "student").
            password_hash: Hashed password.

        Returns:
            The created user data.
        """
        def _query():
            result = self.client.table("users").insert({
                "name": name,
                "email": email,
                "role": role,
                "password_hash": password_hash,
            }).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user by email address.

        Args:
            email: The email address to look up.

        Returns:
            User data dictionary, or None if not found.
        """
        def _query():
            result = self.client.table("users").select("*").eq("email", email).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user by ID.

        Args:
            user_id: The user ID to look up.

        Returns:
            User data dictionary, or None if not found.
        """
        def _query():
            result = self.client.table("users").select("*").eq("id", user_id).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    # ==================== Category Operations ====================

    async def get_categories(self) -> List[Dict[str, Any]]:
        """Retrieve all categories ordered by priority."""
        def _query():
            result = self.client.table("categories").select("*").order("priority").execute()
            return result.data or []
        return await asyncio.to_thread(_query)

    async def create_category(
        self,
        name: str,
        priority: int,
        keywords: List[str],
    ) -> Dict[str, Any]:
        """Create a new category.

        Args:
            name: Category display name.
            priority: Priority level (1-10).
            keywords: List of associated keywords.

        Returns:
            The created category data.
        """
        def _query():
            result = self.client.table("categories").insert({
                "name": name,
                "priority": priority,
                "keywords": keywords,
            }).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    # ==================== Knowledge Source Operations ====================

    async def get_knowledge_sources(self) -> List[Dict[str, Any]]:
        """Retrieve all knowledge sources ordered by creation date (newest first)."""
        def _query():
            result = self.client.table("knowledge_sources").select("*").order("created_at", desc=True).execute()
            return result.data or []
        return await asyncio.to_thread(_query)

    async def get_knowledge_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single knowledge source by ID.

        Args:
            source_id: The source ID.

        Returns:
            Source data dictionary, or None if not found.
        """
        def _query():
            result = self.client.table("knowledge_sources").select("*").eq("id", source_id).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def create_knowledge_source(
        self,
        title: str,
        content: str,
        keywords: List[str],
        category: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new knowledge source.

        Args:
            title: Source title.
            content: Source body content.
            keywords: List of keyword tags.
            category: Associated category name.
            created_by: ID of the user who created this source.

        Returns:
            The created knowledge source data.
        """
        def _query():
            result = self.client.table("knowledge_sources").insert({
                "title": title,
                "content": content,
                "keywords": keywords,
                "category": category,
                "created_by": created_by,
            }).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def update_knowledge_source(
        self,
        source_id: str,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        """Update a knowledge source with the given fields.

        Args:
            source_id: The source ID to update.
            **kwargs: Fields to update.

        Returns:
            The updated source data, or None on failure.
        """
        kwargs["updated_at"] = datetime.now().isoformat()

        def _query():
            result = self.client.table("knowledge_sources").update(kwargs).eq("id", source_id).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def delete_knowledge_source(self, source_id: str) -> bool:
        """Delete a knowledge source.

        Args:
            source_id: The source ID to delete.

        Returns:
            True if the deletion was successful.
        """
        def _query():
            result = self.client.table("knowledge_sources").delete().eq("id", source_id).execute()
            return len(result.data) > 0 if result.data else False
        return await asyncio.to_thread(_query)

    # ==================== Email Operations ====================

    async def get_emails(
        self,
        status: Optional[str] = None,
        category_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of emails with optional filters.

        Args:
            status: Filter by email status.
            category_id: Filter by category ID.
            limit: Maximum number of results.
            offset: Pagination offset.

        Returns:
            A list of email data dictionaries.
        """
        def _query():
            query = self.client.table("emails").select("*, categories(*)")

            if status:
                query = query.eq("status", status)
            if category_id:
                query = query.eq("category_id", category_id)

            result = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            return result.data or []
        return await asyncio.to_thread(_query)

    async def get_email(self, email_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single email by ID (with joined category data).

        Args:
            email_id: The email ID.

        Returns:
            Email data dictionary with category, or None if not found.
        """
        def _query():
            result = self.client.table("emails").select("*, categories(*)").eq("id", email_id).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def create_email(
        self,
        subject: str,
        body: str,
        sender_email: str,
        sender_name: Optional[str] = None,
        category_id: Optional[str] = None,
        is_duplicate: bool = False,
    ) -> Dict[str, Any]:
        """Create a new email.

        Args:
            subject: Email subject line.
            body: Email body content.
            sender_email: Sender's email address.
            sender_name: Sender's display name.
            category_id: Assigned category ID.
            is_duplicate: Whether the email is a duplicate.

        Returns:
            The created email data.
        """
        def _query():
            result = self.client.table("emails").insert({
                "subject": subject,
                "body": body,
                "sender_email": sender_email,
                "sender_name": sender_name,
                "category_id": category_id,
                "is_duplicate": is_duplicate,
                "status": "pending",
            }).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def update_email(
        self,
        email_id: str,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        """Update an email with the given fields.

        Args:
            email_id: The email ID to update.
            **kwargs: Fields to update.

        Returns:
            The updated email data, or None on failure.
        """
        def _query():
            result = self.client.table("emails").update(kwargs).eq("id", email_id).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def count_emails(self, status: Optional[str] = None) -> int:
        """Count emails using an efficient database COUNT query.

        Args:
            status: Optional status filter.

        Returns:
            Number of matching emails.
        """
        def _query():
            query = self.client.table("emails").select("id", count="exact")
            if status:
                query = query.eq("status", status)
            result = query.execute()
            return result.count if result.count is not None else len(result.data)
        return await asyncio.to_thread(_query)

    # ==================== Reply Operations ====================

    async def get_reply_by_id(self, reply_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a reply by ID.

        Args:
            reply_id: The reply ID.

        Returns:
            Reply data dictionary, or None if not found.
        """
        def _query():
            result = self.client.table("replies").select("*").eq("id", reply_id).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def get_reply_by_email(self, email_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the reply for a specific email.

        Args:
            email_id: The email ID.

        Returns:
            Reply data dictionary, or None if no reply exists.
        """
        def _query():
            result = self.client.table("replies").select("*").eq("email_id", email_id).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def create_reply(
        self,
        email_id: str,
        content: str,
        is_auto: bool = True,
        referenced_sources: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new reply.

        Args:
            email_id: The email ID this reply belongs to.
            content: Reply body content.
            is_auto: Whether this is an auto-generated reply.
            referenced_sources: List of referenced knowledge source IDs.

        Returns:
            The created reply data.
        """
        def _query():
            result = self.client.table("replies").insert({
                "email_id": email_id,
                "content": content,
                "is_auto": is_auto,
                "referenced_sources": referenced_sources or [],
            }).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def update_reply(
        self,
        reply_id: str,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        """Update a reply with the given fields.

        Args:
            reply_id: The reply ID to update.
            **kwargs: Fields to update.

        Returns:
            The updated reply data, or None on failure.
        """
        def _query():
            result = self.client.table("replies").update(kwargs).eq("id", reply_id).execute()
            return result.data[0] if result.data else None
        return await asyncio.to_thread(_query)

    async def approve_reply(self, reply_id: str) -> bool:
        """Approve a reply by setting is_approved to True.

        Args:
            reply_id: The reply ID to approve.

        Returns:
            True if the approval was successful.
        """
        def _query():
            result = self.client.table("replies").update({"is_approved": True}).eq("id", reply_id).execute()
            return len(result.data) > 0 if result.data else False
        return await asyncio.to_thread(_query)

    async def delete_reply(self, reply_id: str) -> bool:
        """Delete a reply.

        Args:
            reply_id: The reply ID to delete.

        Returns:
            True if the deletion was successful.
        """
        def _query():
            result = self.client.table("replies").delete().eq("id", reply_id).execute()
            return len(result.data) > 0 if result.data else False
        return await asyncio.to_thread(_query)

    # ==================== Statistics Operations ====================

    async def get_stats(self) -> Dict[str, Any]:
        """Retrieve system-wide statistics.

        Returns a summary of email counts by status, reply metrics,
        and knowledge base usage.
        """
        def _query():
            # Get email counts grouped by status
            emails_result = self.client.table("emails").select("status").execute()
            emails = emails_result.data or []

            status_counts = {}
            for email in emails:
                status = email.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1

            # Get reply statistics
            replies_result = self.client.table("replies").select("is_auto, is_approved").execute()
            replies = replies_result.data or []

            auto_replies = sum(1 for r in replies if r.get("is_auto"))
            approved_replies = sum(1 for r in replies if r.get("is_approved"))

            # Get knowledge source count
            sources_result = self.client.table("knowledge_sources").select("id").execute()
            sources_count = len(sources_result.data) if sources_result.data else 0

            return {
                "total_emails": len(emails),
                "status_counts": status_counts,
                "auto_replies": auto_replies,
                "approved_replies": approved_replies,
                "knowledge_sources": sources_count,
            }
        return await asyncio.to_thread(_query)


# Module-level registry for backend swapping (demo mode)
_db_backend: Optional[DatabaseClient] = None


def set_db_backend(client: DatabaseClient) -> None:
    """Set the database backend.

    Used by demo mode to inject SqliteClient before any services are instantiated.
    When set, all get_db() calls return the injected client instead of SupabaseClient.

    Args:
        client: A DatabaseClient instance (e.g. SqliteClient for demo mode).
    """
    global _db_backend
    _db_backend = client


def get_db() -> DatabaseClient:
    """Get the database client.

    Returns the injected backend if set (demo mode),
    otherwise returns the SupabaseClient singleton.
    """
    if _db_backend is not None:
        return _db_backend
    return SupabaseClient()
