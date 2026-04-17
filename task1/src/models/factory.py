"""Email Factory

Implements the Factory Pattern to create appropriate Email subclass instances
based on data characteristics. Demonstrates OOP Factory Pattern and Polymorphism:
the same interface (from_dict) produces different subclass objects depending on
the input data.
"""

from typing import Dict, Any

from .email import Email, StudentEmail, FAQEmail, EmailStatus
from .category import Category


class EmailFactory:
    """Factory class for creating Email subclass instances.

    Selects the appropriate Email subclass (StudentEmail, FAQEmail, or Email)
    based on data characteristics, centralising the creation logic so that
    EmailService, ReplyService and other consumers share a single conversion
    path.

    Demonstrates:
        - Factory Pattern: one interface, multiple concrete products.
        - Polymorphism: callers work with the abstract Email type without
          knowing which subclass they received.
    """

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Email:
        """Convert a database dictionary to an Email subclass instance.

        Selection logic:
        - If ``is_duplicate`` is True, creates a FAQEmail (repeat question).
        - Otherwise, creates a StudentEmail (default for incoming student email).

        Args:
            data: Dictionary returned from the database.

        Returns:
            An Email or its subclass instance.
        """
        status = EmailStatus(data.get("status", "pending"))

        # If the email is marked as duplicate, create a FAQEmail subclass
        if data.get("is_duplicate", False):
            email: Email = FAQEmail(
                id=data["id"],
                subject=data["subject"],
                body=data["body"],
                sender_email=data["sender_email"],
                sender_name=data.get("sender_name"),
                faq_id=data.get("faq_id"),
            )
        else:
            # Default: create a StudentEmail subclass (preserves student_id)
            email = StudentEmail(
                id=data["id"],
                subject=data["subject"],
                body=data["body"],
                sender_email=data["sender_email"],
                sender_name=data.get("sender_name"),
                student_id=data.get("student_id"),
            )

        email.status = status
        email.is_duplicate = data.get("is_duplicate", False)

        # Set the category if available
        if data.get("categories"):
            cat_data = data["categories"]
            email.category = Category(
                id=cat_data["id"],
                name=cat_data["name"],
                priority=cat_data.get("priority", 5),
                keywords=cat_data.get("keywords", []),
            )

        return email
