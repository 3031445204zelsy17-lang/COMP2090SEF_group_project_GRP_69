"""Knowledge Source API Routes

Provides CRUD endpoints for managing knowledge base entries
(course materials, FAQs, etc.) and a semantic search endpoint
for finding relevant sources based on email content.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..services.knowledge_service import KnowledgeService
from .auth import get_current_user

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge Sources"])

# Singleton service instance
_knowledge_service: Optional[KnowledgeService] = None


def get_knowledge_service() -> KnowledgeService:
    """Return the singleton KnowledgeService instance."""
    global _knowledge_service
    if _knowledge_service is None:
        _knowledge_service = KnowledgeService()
    return _knowledge_service


class KnowledgeSourceCreate(BaseModel):
    """Request body for creating a knowledge source."""
    title: str
    content: str
    keywords: List[str] = []
    category: Optional[str] = None


class KnowledgeSourceUpdate(BaseModel):
    """Request body for updating a knowledge source."""
    title: Optional[str] = None
    content: Optional[str] = None
    keywords: Optional[List[str]] = None
    category: Optional[str] = None


class KnowledgeSourceResponse(BaseModel):
    """Response body for knowledge source data."""
    id: str
    title: str
    content: str
    keywords: List[str]
    category: Optional[str]
    created_at: str
    updated_at: str


@router.get("", response_model=List[KnowledgeSourceResponse])
async def list_knowledge_sources():
    """List all knowledge sources in the system."""
    service = get_knowledge_service()
    sources = await service.get_all_sources()

    return [
        KnowledgeSourceResponse(
            id=source.id,
            title=source.title,
            content=source.content,
            keywords=source.keywords,
            category=source.category,
            created_at=source.created_at.isoformat(),
            updated_at=source.updated_at.isoformat(),
        )
        for source in sources
    ]


@router.get("/{source_id}", response_model=KnowledgeSourceResponse)
async def get_knowledge_source(source_id: str):
    """Retrieve a single knowledge source by ID."""
    service = get_knowledge_service()
    source = await service.get_source(source_id)

    if not source:
        raise HTTPException(status_code=404, detail="Knowledge source not found")

    return KnowledgeSourceResponse(
        id=source.id,
        title=source.title,
        content=source.content,
        keywords=source.keywords,
        category=source.category,
        created_at=source.created_at.isoformat(),
        updated_at=source.updated_at.isoformat(),
    )


@router.post("", response_model=KnowledgeSourceResponse)
async def create_knowledge_source(source: KnowledgeSourceCreate, current_user=Depends(get_current_user)):
    """Create a new knowledge source entry (requires authentication)."""
    service = get_knowledge_service()

    created_source = await service.create_source(
        title=source.title,
        content=source.content,
        keywords=source.keywords,
        category=source.category,
    )

    return KnowledgeSourceResponse(
        id=created_source.id,
        title=created_source.title,
        content=created_source.content,
        keywords=created_source.keywords,
        category=created_source.category,
        created_at=created_source.created_at.isoformat(),
        updated_at=created_source.updated_at.isoformat(),
    )


@router.put("/{source_id}", response_model=KnowledgeSourceResponse)
async def update_knowledge_source(source_id: str, update: KnowledgeSourceUpdate, current_user=Depends(get_current_user)):
    """Update an existing knowledge source (partial update supported)."""
    service = get_knowledge_service()

    updated_source = await service.update_source(
        source_id=source_id,
        title=update.title,
        content=update.content,
        keywords=update.keywords,
        category=update.category,
    )

    if not updated_source:
        raise HTTPException(status_code=404, detail="Knowledge source not found")

    return KnowledgeSourceResponse(
        id=updated_source.id,
        title=updated_source.title,
        content=updated_source.content,
        keywords=updated_source.keywords,
        category=updated_source.category,
        created_at=updated_source.created_at.isoformat(),
        updated_at=updated_source.updated_at.isoformat(),
    )


@router.delete("/{source_id}")
async def delete_knowledge_source(source_id: str, current_user=Depends(get_current_user)):
    """Delete a knowledge source by ID."""
    service = get_knowledge_service()

    success = await service.delete_source(source_id)
    if not success:
        raise HTTPException(status_code=404, detail="Knowledge source not found")

    return {"message": "Knowledge source deleted"}


@router.post("/search")
async def search_knowledge_sources(query: str, top_k: int = 5):
    """Search for knowledge sources relevant to the given query text.

    Uses keyword matching and content similarity to rank results.
    """
    service = get_knowledge_service()

    results = await service.search_relevant_sources(
        email_content=query,
        top_k=top_k,
    )

    return {
        "results": [
            {
                "source": {
                    "id": source.id,
                    "title": source.title,
                    "content": source.content[:200] + "..." if len(source.content) > 200 else source.content,
                    "keywords": source.keywords,
                },
                "score": score,
            }
            for source, score in results
        ]
    }
