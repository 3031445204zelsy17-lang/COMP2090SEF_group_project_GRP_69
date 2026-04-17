"""Statistics API Routes

Provides system-wide statistics including email counts by status,
auto-reply metrics, and knowledge base usage.
"""

from typing import Dict, Any

from fastapi import APIRouter

from ..db.supabase_client import get_db

router = APIRouter(prefix="/api/stats", tags=["Statistics"])


@router.get("")
async def get_stats() -> Dict[str, Any]:
    """Retrieve overall system statistics.

    Returns aggregate counts for emails, replies, and knowledge sources.
    """
    db = get_db()
    stats = await db.get_stats()

    return {
        "total_emails": stats["total_emails"],
        "status_counts": stats["status_counts"],
        "auto_replies": stats["auto_replies"],
        "approved_replies": stats["approved_replies"],
        "knowledge_sources": stats["knowledge_sources"],
        "pending_emails": stats["status_counts"].get("pending", 0),
        "classified_emails": stats["status_counts"].get("classified", 0),
        "replied_emails": stats["status_counts"].get("replied", 0),
    }


@router.get("/dashboard")
async def get_dashboard() -> Dict[str, Any]:
    """Retrieve dashboard summary with processing rate calculation.

    Computes the percentage of emails that have been processed
    (classified + replied + approved + sent) out of total emails.
    """
    db = get_db()
    stats = await db.get_stats()

    # Calculate processing rate (percentage of non-pending emails)
    total = stats["total_emails"]
    processed = (
        stats["status_counts"].get("classified", 0) +
        stats["status_counts"].get("replied", 0) +
        stats["status_counts"].get("approved", 0) +
        stats["status_counts"].get("sent", 0)
    )
    processing_rate = (processed / total * 100) if total > 0 else 0

    return {
        "summary": {
            "total_emails": total,
            "pending_emails": stats["status_counts"].get("pending", 0),
            "auto_replies": stats["auto_replies"],
            "approved_replies": stats["approved_replies"],
            "processing_rate": round(processing_rate, 1),
        },
        "by_status": stats["status_counts"],
        "knowledge_sources_count": stats["knowledge_sources"],
    }
