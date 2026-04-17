"""Knowledge Source Service

Provides CRUD operations and intelligent search for knowledge sources.
"""

from typing import List, Optional, Dict, Any

from ..models.knowledge_source import KnowledgeSource
from ..db.supabase_client import get_db


class KnowledgeService:
    """Knowledge source service.

    Handles creation, retrieval, updating, deletion, and relevance-based
    search of knowledge source entries.
    """

    def __init__(self):
        self._db = get_db()

    async def create_source(
        self,
        title: str,
        content: str,
        keywords: Optional[List[str]] = None,
        category: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> KnowledgeSource:
        """Create a new knowledge source.

        Args:
            title: Source title.
            content: Source body content.
            keywords: List of keyword tags.
            category: Associated classification category.
            created_by: ID of the creator.

        Returns:
            The created KnowledgeSource object.
        """
        # Create the model object
        source = KnowledgeSource(
            title=title,
            content=content,
            keywords=keywords or [],
            category=category,
            created_by=created_by,
        )

        # Save to database
        data = await self._db.create_knowledge_source(
            title=title,
            content=content,
            keywords=keywords or [],
            category=category,
            created_by=created_by,
        )

        # Set the database-assigned ID
        if data:
            source.id = data["id"]

        return source

    async def get_all_sources(self) -> List[KnowledgeSource]:
        """Retrieve all knowledge sources.

        Returns:
            A list of all KnowledgeSource objects.
        """
        data_list = await self._db.get_knowledge_sources()
        return [self._dict_to_source(data) for data in data_list]

    async def get_source(self, source_id: str) -> Optional[KnowledgeSource]:
        """Retrieve a single knowledge source by ID.

        Args:
            source_id: The source ID.

        Returns:
            The KnowledgeSource object, or None if not found.
        """
        data = await self._db.get_knowledge_source(source_id)
        return self._dict_to_source(data) if data else None

    async def update_source(
        self,
        source_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        category: Optional[str] = None,
    ) -> Optional[KnowledgeSource]:
        """Update a knowledge source.

        Args:
            source_id: The source ID to update.
            title: New title.
            content: New content.
            keywords: New keyword list.
            category: New category.

        Returns:
            The updated KnowledgeSource object, or None on failure.
        """
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if content is not None:
            update_data["content"] = content
        if keywords is not None:
            update_data["keywords"] = keywords
        if category is not None:
            update_data["category"] = category

        if not update_data:
            return await self.get_source(source_id)

        data = await self._db.update_knowledge_source(source_id, **update_data)
        return self._dict_to_source(data) if data else None

    async def delete_source(self, source_id: str) -> bool:
        """Delete a knowledge source.

        Args:
            source_id: The source ID to delete.

        Returns:
            True if the deletion was successful.
        """
        return await self._db.delete_knowledge_source(source_id)

    async def search_relevant_sources(
        self,
        email_content: str,
        top_k: int = 3,
        min_score: float = 0.1,
    ) -> List[tuple[KnowledgeSource, float]]:
        """Search for knowledge sources relevant to an email's content.

        Uses keyword matching and content overlap to calculate relevance.

        Args:
            email_content: The email content to match against.
            top_k: Maximum number of results to return.
            min_score: Minimum relevance score threshold.

        Returns:
            A list of (KnowledgeSource, score) tuples, sorted by score descending.
        """
        # Load all sources and calculate relevance scores
        all_sources = await self.get_all_sources()

        # Score each source
        scored_sources = []
        for source in all_sources:
            score = source.calculate_relevance_score(email_content)
            if score >= min_score:
                scored_sources.append((source, score))

        # Sort by score descending
        scored_sources.sort(key=lambda x: x[1], reverse=True)

        return scored_sources[:top_k]

    def _dict_to_source(self, data: Dict[str, Any]) -> KnowledgeSource:
        """Convert a dictionary to a KnowledgeSource object.

        Args:
            data: Dictionary returned from the database.

        Returns:
            A KnowledgeSource instance.
        """
        source = KnowledgeSource(
            title=data["title"],
            content=data["content"],
            keywords=data.get("keywords", []),
            category=data.get("category"),
            source_id=data["id"],
            created_by=data.get("created_by"),
        )
        return source
