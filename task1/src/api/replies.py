"""Reply API Routes

Provides endpoints for reply generation, editing, approval, and sending.
Demonstrates OOP concepts: Professor class uses Encapsulation for
approve/reject operations; Strategy Pattern enables polymorphic reply generation.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..services.reply_service import ReplyService
from ..services.email_service import EmailService
from ..models.user import Professor
from ..models.reply import Reply
from .auth import get_current_user, require_professor

router = APIRouter(prefix="/api", tags=["Replies"])

# Singleton service instances
_reply_service: Optional[ReplyService] = None
_email_service: Optional[EmailService] = None


def get_reply_service() -> ReplyService:
    """Return the singleton ReplyService instance."""
    global _reply_service
    if _reply_service is None:
        _reply_service = ReplyService()
    return _reply_service


def get_email_service() -> EmailService:
    """Return the singleton EmailService instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


class ReplyResponse(BaseModel):
    """Response body for reply data."""
    id: str
    email_id: str
    content: str
    is_auto: bool
    is_approved: bool
    referenced_sources: List[str]
    created_at: str


class ReplyUpdate(BaseModel):
    """Request body for updating a reply."""
    content: str


class ChatRequest(BaseModel):
    """Request body for conversational (AI-assisted) reply editing."""
    message: str


class ReplyWithSources(BaseModel):
    """Response body for a reply with resolved knowledge source details."""
    id: str
    email_id: str
    content: str
    is_auto: bool
    is_approved: bool
    referenced_sources: List[dict]
    created_at: str


@router.get("/emails/{email_id}/reply", response_model=ReplyWithSources)
async def get_or_generate_reply(email_id: str):
    """Get existing reply for an email, or generate one if not found.

    Also resolves referenced knowledge source details for display.
    """
    reply_service = get_reply_service()
    email_service = get_email_service()

    # Fetch the target email
    email = await email_service.get_email(email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    # Get existing reply or auto-generate a new one
    reply = await reply_service.get_reply_by_email(email_id)
    if not reply:
        reply = await reply_service.generate_reply(email)

    # Resolve referenced knowledge source details for display
    referenced_sources = []
    if reply.referenced_sources:
        from ..services.knowledge_service import KnowledgeService
        knowledge_service = KnowledgeService()
        for source_id in reply.referenced_sources:
            source = await knowledge_service.get_source(source_id)
            if source:
                referenced_sources.append({
                    "id": source.id,
                    "title": source.title,
                })

    return ReplyWithSources(
        id=reply.id,
        email_id=reply.email_id,
        content=reply.content,
        is_auto=reply.is_auto,
        is_approved=reply.approved,
        referenced_sources=referenced_sources,
        created_at=reply.timestamp.isoformat(),
    )


@router.put("/replies/{reply_id}", response_model=ReplyResponse)
async def update_reply(reply_id: str, update: ReplyUpdate, current_user=Depends(get_current_user)):
    """Update the content of an existing reply."""
    reply_service = get_reply_service()

    reply = await reply_service.update_reply(reply_id, content=update.content)
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found")

    return ReplyResponse(
        id=reply.id,
        email_id=reply.email_id,
        content=reply.content,
        is_auto=reply.is_auto,
        is_approved=reply.approved,
        referenced_sources=reply.referenced_sources,
        created_at=reply.timestamp.isoformat(),
    )


@router.post("/replies/{reply_id}/approve")
async def approve_reply(reply_id: str, current_user=Depends(require_professor)):
    """Approve a reply via the Professor class.

    Demonstrates OOP Inheritance (Professor extends User) and
    Encapsulation (approve_reply encapsulates approval logic).
    """
    reply_service = get_reply_service()

    # Fetch the reply object
    reply = await reply_service.get_reply(reply_id)
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found")

    # Use Professor class for approval (OOP Encapsulation)
    professor = Professor(
        name=current_user.get("name", "Professor"),
        email=current_user.get("email", "professor@hkmu.edu.hk"),
    )
    professor.approve_reply(reply)

    # Persist the approval result to the database
    success = await reply_service.approve_reply(reply_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reply not found")

    return {"message": "Reply approved"}


@router.post("/replies/{reply_id}/reject")
async def reject_reply(reply_id: str, current_user=Depends(require_professor)):
    """Reject a reply via the Professor class.

    Demonstrates OOP Inheritance (Professor extends User) and
    Encapsulation (reject_reply encapsulates rejection logic).
    """
    reply_service = get_reply_service()

    # Fetch the reply object
    reply = await reply_service.get_reply(reply_id)
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found")

    # Use Professor class for rejection (OOP Encapsulation)
    professor = Professor(
        name=current_user.get("name", "Professor"),
        email=current_user.get("email", "professor@hkmu.edu.hk"),
    )
    professor.reject_reply(reply, reason="Professor manually rejected")

    # Persist the rejection result to the database
    success = await reply_service.reject_reply(reply_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reply not found")

    return {"message": "Reply rejected"}


@router.post("/emails/{email_id}/regenerate")
async def regenerate_reply(email_id: str, current_user=Depends(get_current_user)):
    """Delete old reply and generate a fresh one for the email."""
    reply_service = get_reply_service()
    email_service = get_email_service()

    # Fetch the target email
    email = await email_service.get_email(email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    # Get the old reply to be replaced
    old_reply = await reply_service.get_reply_by_email(email_id)
    if not old_reply:
        raise HTTPException(status_code=404, detail="No existing reply found")

    # Regenerate with fresh LLM call
    new_reply = await reply_service.regenerate_reply(email, old_reply.id)

    return {
        "id": new_reply.id,
        "content": new_reply.content,
        "message": "Reply regenerated",
    }


@router.post("/emails/{email_id}/generate")
async def generate_reply(email_id: str, current_user=Depends(get_current_user)):
    """Generate a reply on demand (user-triggered, not automatic)."""
    reply_service = get_reply_service()
    email_service = get_email_service()

    # Fetch the target email
    email = await email_service.get_email(email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    # Return existing reply if already generated
    existing_reply = await reply_service.get_reply_by_email(email_id)
    if existing_reply:
        return {
            "id": existing_reply.id,
            "content": existing_reply.content,
            "is_approved": existing_reply.approved,
            "message": "Reply already exists",
        }

    # Generate a new reply via the strategy pattern
    reply = await reply_service.generate_reply(email)

    # Resolve referenced knowledge sources for display
    referenced_sources = []
    if reply.referenced_sources:
        from ..services.knowledge_service import KnowledgeService
        knowledge_service = KnowledgeService()
        for source_id in reply.referenced_sources:
            source = await knowledge_service.get_source(source_id)
            if source:
                referenced_sources.append({
                    "id": source.id,
                    "title": source.title,
                })

    return {
        "id": reply.id,
        "content": reply.content,
        "is_auto": reply.is_auto,
        "is_approved": reply.approved,
        "referenced_sources": referenced_sources,
        "message": "Reply generated",
    }


@router.post("/replies/{reply_id}/chat")
async def chat_edit_reply(reply_id: str, request: ChatRequest, current_user=Depends(get_current_user)):
    """Edit a reply using conversational AI instructions.

    Accepts a natural language instruction (e.g. "reply in English")
    and uses the LLM to modify the reply accordingly.
    """
    reply_service = get_reply_service()

    # Fetch the current reply
    reply = await reply_service.get_reply(reply_id)
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found")

    # Use LLM to apply the user's edit instruction
    from ..llm.deepseek_client import get_llm_client
    llm = get_llm_client()

    new_content = await llm.chat_edit_reply(
        current_reply=reply.content,
        user_instruction=request.message,
    )

    # Persist the edited content
    updated_reply = await reply_service.update_reply(reply_id, content=new_content)
    if not updated_reply:
        raise HTTPException(status_code=500, detail="Failed to update reply")

    return {
        "id": updated_reply.id,
        "content": updated_reply.content,
        "message": "Reply updated",
    }


@router.post("/replies/{reply_id}/send")
async def send_reply(reply_id: str, current_user=Depends(require_professor)):
    """Send a reply (simulated). Auto-approves if not yet approved, then marks email as sent."""
    reply_service = get_reply_service()

    result = await reply_service.send_reply(reply_id)
    if not result:
        raise HTTPException(status_code=404, detail="Reply not found")

    return {
        "message": "Reply sent",
        "email_id": result["email_id"],
        "sent_at": result["sent_at"],
    }
