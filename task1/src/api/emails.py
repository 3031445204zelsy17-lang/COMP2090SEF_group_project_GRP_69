"""Email API Routes

Provides RESTful endpoints for email management including creation,
listing, detail retrieval, classification, and category updates.
"""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, EmailStr

from ..services.email_service import EmailService
from ..models.email import EmailStatus
from .auth import get_current_user

router = APIRouter(prefix="/api/emails", tags=["Emails"])

# Singleton service instance to avoid re-creation on every request
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """Return the singleton EmailService instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service


class EmailCreate(BaseModel):
    """Request body for creating a new email."""
    subject: str
    body: str
    sender_email: EmailStr
    sender_name: Optional[str] = None


class EmailResponse(BaseModel):
    """Response body for email data."""
    id: str
    subject: str
    body: str
    sender_email: str
    sender_name: Optional[str]
    status: str
    category: Optional[dict]
    is_duplicate: bool
    created_at: str


class CategoryUpdate(BaseModel):
    """Request body for updating an email's category."""
    category_id: str


@router.get("", response_model=List[EmailResponse])
async def list_emails(
    status: Optional[str] = Query(None, description="Filter by status"),
    category_id: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """List emails with optional filtering by status and category.

    Supports pagination via limit/offset parameters.
    """
    service = get_email_service()
    emails = await service.get_emails(
        status=status,
        category_id=category_id,
        limit=limit,
        offset=offset,
    )

    return [
        EmailResponse(
            id=email.id,
            subject=email.subject,
            body=email.body,
            sender_email=email.sender_email,
            sender_name=email.sender_name,
            status=email.status.value,
            category=email.category.to_dict() if email.category else None,
            is_duplicate=email.is_duplicate,
            created_at=email.timestamp.isoformat(),
        )
        for email in emails
    ]


@router.post("", response_model=EmailResponse)
async def create_email(email: EmailCreate, current_user=Depends(get_current_user)):
    """Create a new email (simulates receiving an email).

    EmailService.create_email internally handles auto-classification
    and duplicate detection, so no additional service calls are needed.
    """
    service = get_email_service()

    # Create email (auto-classification and duplicate detection handled internally)
    new_email = await service.create_email(
        subject=email.subject,
        body=email.body,
        sender_email=email.sender_email,
        sender_name=email.sender_name,
    )

    return EmailResponse(
        id=new_email.id,
        subject=new_email.subject,
        body=new_email.body,
        sender_email=new_email.sender_email,
        sender_name=new_email.sender_name,
        status=new_email.status.value,
        category=new_email.category.to_dict() if new_email.category else None,
        is_duplicate=new_email.is_duplicate,
        created_at=new_email.timestamp.isoformat(),
    )


@router.get("/{email_id}", response_model=EmailResponse)
async def get_email(email_id: str):
    """Retrieve a single email by its ID."""
    service = get_email_service()
    email = await service.get_email(email_id)

    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    return EmailResponse(
        id=email.id,
        subject=email.subject,
        body=email.body,
        sender_email=email.sender_email,
        sender_name=email.sender_name,
        status=email.status.value,
        category=email.category.to_dict() if email.category else None,
        is_duplicate=email.is_duplicate,
        created_at=email.timestamp.isoformat(),
    )


@router.put("/{email_id}/category")
async def update_email_category(email_id: str, update: CategoryUpdate, current_user=Depends(get_current_user)):
    """Update the category assignment for a specific email."""
    service = get_email_service()
    success = await service.update_category(email_id, update.category_id)

    if not success:
        raise HTTPException(status_code=404, detail="Email or category not found")

    return {"message": "Category updated"}


@router.post("/{email_id}/classify")
async def classify_email(email_id: str, current_user=Depends(get_current_user)):
    """Manually trigger classification for a specific email."""
    service = get_email_service()

    email = await service.get_email(email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    # Perform classification
    from ..services.classification_service import ClassificationService
    classification_service = ClassificationService()
    category = await classification_service.auto_classify(email)

    return {
        "category": category.to_dict() if category else None,
        "message": "Classification complete",
    }
