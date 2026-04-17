"""Email Model Unit Tests

Tests for Email, StudentEmail, FAQEmail class creation, attribute access, and status management.
"""

import pytest
from src.models.email import Email, StudentEmail, FAQEmail, EmailStatus


class TestEmail:
    """Email base class tests."""

    def test_create_email(self):
        """Test creating an Email object."""
        email = Email(
            id="e001",
            subject="About homework",
            body="Hello Professor, when is the homework deadline?",
            sender_email="student@hkmu.edu.hk",
            sender_name="Zhang",
        )
        assert email.id == "e001"
        assert email.subject == "About homework"
        assert email.body == "Hello Professor, when is the homework deadline?"
        assert email.sender_email == "student@hkmu.edu.hk"
        assert email.sender_name == "Zhang"
        assert email.status == EmailStatus.PENDING
        assert email.is_duplicate is False

    def test_email_default_status(self):
        """Test that the default status is pending."""
        email = Email(id="e002", subject="test", body="test", sender_email="a@b.com")
        assert email.status == EmailStatus.PENDING

    def test_email_status_change(self):
        """Test email status transitions."""
        email = Email(id="e003", subject="test", body="test", sender_email="a@b.com")

        # pending → classified
        email.status = EmailStatus.CLASSIFIED
        assert email.status == EmailStatus.CLASSIFIED

        # classified → replied
        email.status = EmailStatus.REPLIED
        assert email.status == EmailStatus.REPLIED

        # replied → approved
        email.status = EmailStatus.APPROVED
        assert email.status == EmailStatus.APPROVED

        # approved → sent
        email.status = EmailStatus.SENT
        assert email.status == EmailStatus.SENT

    def test_email_duplicate_flag(self):
        """Test the duplicate flag."""
        email = Email(id="e004", subject="test", body="test", sender_email="a@b.com")
        assert email.is_duplicate is False

        email.is_duplicate = True
        assert email.is_duplicate is True

    def test_email_category(self):
        """Test setting a category on an email."""
        email = Email(id="e005", subject="test", body="test", sender_email="a@b.com")
        assert email.category is None

        from src.models.category import Category, CategoryType
        cat = Category(id="c001", name="Academic", priority=1, category_type=CategoryType.ACADEMIC)
        email.category = cat
        assert email.category.name == "Academic"

    def test_email_to_dict(self):
        """Test the to_dict method."""
        email = Email(
            id="e006",
            subject="test subject",
            body="test body",
            sender_email="a@b.com",
            sender_name="Test User",
        )
        d = email.to_dict()
        assert d["id"] == "e006"
        assert d["subject"] == "test subject"
        assert d["body"] == "test body"
        assert d["sender_email"] == "a@b.com"
        assert d["sender_name"] == "Test User"
        assert d["status"] == "pending"
        assert d["is_duplicate"] is False

    def test_email_repr(self):
        """Test __repr__ output."""
        email = Email(id="e007", subject="test", body="test", sender_email="a@b.com")
        assert "e007" in repr(email)
        assert "test" in repr(email)


class TestStudentEmail:
    """StudentEmail subclass tests."""

    def test_create_student_email(self):
        """Test creating a StudentEmail."""
        email = StudentEmail(
            id="se001",
            subject="Leave request",
            body="Hello Professor, I would like to request leave",
            sender_email="student@hkmu.edu.hk",
            sender_name="Li",
            student_id="S12345678",
        )
        # Inherited from Email
        assert email.id == "se001"
        assert email.subject == "Leave request"
        assert email.status == EmailStatus.PENDING

        # StudentEmail-specific attribute
        assert email.student_id == "S12345678"

    def test_student_email_without_student_id(self):
        """Test creating a StudentEmail without student_id."""
        email = StudentEmail(
            id="se002",
            subject="test",
            body="test",
            sender_email="a@b.com",
        )
        assert email.student_id is None

    def test_student_email_is_instance_of_email(self):
        """Test that StudentEmail is a subclass of Email."""
        email = StudentEmail(id="se003", subject="test", body="test", sender_email="a@b.com")
        assert isinstance(email, Email)


class TestFAQEmail:
    """FAQEmail subclass tests."""

    def test_create_faq_email(self):
        """Test creating a FAQEmail."""
        email = FAQEmail(
            id="fe001",
            subject="Class schedule",
            body="When does the course meet?",
            sender_email="student@hkmu.edu.hk",
            sender_name="Wang",
            faq_id="faq001",
        )
        # FAQEmail-specific attribute
        assert email.faq_id == "faq001"
        # Inherited from Email
        assert isinstance(email, Email)

    def test_faq_email_is_duplicate_setter(self):
        """Test that FAQEmail can set the duplicate flag."""
        email = FAQEmail(
            id="fe002",
            subject="test",
            body="test",
            sender_email="a@b.com",
        )
        email.is_duplicate = True
        assert email.is_duplicate is True

    def test_faq_email_set_faq_id(self):
        """Test setting faq_id."""
        email = FAQEmail(
            id="fe003",
            subject="test",
            body="test",
            sender_email="a@b.com",
        )
        assert email.faq_id is None
        email.faq_id = "faq099"
        assert email.faq_id == "faq099"

    def test_faq_email_is_instance_of_email(self):
        """Test that FAQEmail is a subclass of Email."""
        email = FAQEmail(id="fe004", subject="test", body="test", sender_email="a@b.com")
        assert isinstance(email, Email)


class TestEmailStatus:
    """EmailStatus enum tests."""

    def test_status_values(self):
        """Test enum values."""
        assert EmailStatus.PENDING == "pending"
        assert EmailStatus.CLASSIFIED == "classified"
        assert EmailStatus.REPLIED == "replied"
        assert EmailStatus.APPROVED == "approved"
        assert EmailStatus.SENT == "sent"

    def test_status_from_string(self):
        """Test creating enum from string."""
        assert EmailStatus("pending") == EmailStatus.PENDING
        assert EmailStatus("classified") == EmailStatus.CLASSIFIED
