"""ClassificationService Unit Tests

Tests for keyword matching, text similarity, and duplicate detection.
Uses Mock objects to replace database calls so tests do not depend on external services.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.models.email import Email
from src.models.category import Category, CategoryType
from src.services.classification_service import ClassificationService


class TestCalculateMatchScore:
    """Keyword match score calculation tests."""

    def setup_method(self):
        """Create a ClassificationService instance with a mocked database."""
        self.service = ClassificationService.__new__(ClassificationService)
        self.service._db = MagicMock()
        self.service._categories = None

    def test_empty_keywords(self):
        """Empty keywords should return 0."""
        score = self.service._calculate_match_score("test text", [])
        assert score == 0.0

    def test_no_match(self):
        """No matching keywords should return 0."""
        score = self.service._calculate_match_score("Where is the cafeteria?", ["homework", "exam", "grade"])
        assert score == 0.0

    def test_partial_match(self):
        """Partial keyword match."""
        score = self.service._calculate_match_score(
            "When is the homework due?",
            ["homework", "exam", "grade", "course"],
        )
        assert score == 0.25  # 1/4

    def test_full_match(self):
        """All keywords match."""
        score = self.service._calculate_match_score(
            "homework exam grade course",
            ["homework", "exam", "grade", "course"],
        )
        assert score == 1.0

    def test_case_insensitive(self):
        """Case-insensitive matching."""
        score = self.service._calculate_match_score(
            "I have HOMEWORK and exam",
            ["homework", "exam"],
        )
        assert score == 1.0

    def test_bilingual_keywords(self):
        """Mixed Chinese-English keywords."""
        score = self.service._calculate_match_score(
            "About homework issue",
            ["homework", "assignment", "deadline"],
        )
        assert score == pytest.approx(1 / 3, abs=0.01)


class TestCalculateSimilarity:
    """Text similarity calculation tests."""

    def setup_method(self):
        self.service = ClassificationService.__new__(ClassificationService)
        self.service._db = MagicMock()
        self.service._categories = None

    def test_identical_text(self):
        """Identical text should have similarity 1."""
        score = self.service._calculate_similarity("hello world", "hello world")
        assert score == 1.0

    def test_completely_different(self):
        """Completely different text should have low similarity."""
        score = self.service._calculate_similarity("hello world", "ABCDEFGH")
        assert score < 0.3

    def test_similar_text(self):
        """Similar text should have high similarity."""
        score = self.service._calculate_similarity(
            "When is the homework due?",
            "When is the homework deadline?",
        )
        assert score > 0.8

    def test_case_insensitive(self):
        """Case-insensitive comparison."""
        score = self.service._calculate_similarity("Hello World", "hello world")
        assert score == 1.0

    def test_whitespace_stripped(self):
        """Leading/trailing whitespace is ignored."""
        score = self.service._calculate_similarity("  test  ", "test")
        assert score == 1.0


class TestCheckDuplicate:
    """Duplicate email detection tests."""

    def setup_method(self):
        self.service = ClassificationService.__new__(ClassificationService)
        self.service._db = MagicMock()
        self.service._categories = None

    @pytest.mark.asyncio
    async def test_duplicate_detected(self):
        """Duplicate email should be detected."""
        email1 = Email(
            id="e001",
            subject="Homework deadline",
            body="Hello Professor, when is the homework deadline?",
            sender_email="s1@hkmu.edu.hk",
        )
        email2 = Email(
            id="e002",
            subject="Homework deadline",
            body="Hello Professor, when is the homework deadline?",
            sender_email="s2@hkmu.edu.hk",
        )

        is_dup, similar = await self.service.check_duplicate(
            email2, existing_emails=[email1], threshold=0.8
        )
        assert is_dup is True
        assert similar.id == "e001"

    @pytest.mark.asyncio
    async def test_not_duplicate(self):
        """Non-duplicate emails should not be flagged."""
        email1 = Email(
            id="e001",
            subject="Exam schedule",
            body="When and where is the final exam?",
            sender_email="s1@hkmu.edu.hk",
        )
        email2 = Email(
            id="e002",
            subject="Leave request",
            body="Hello Professor, I need to take leave next Wednesday.",
            sender_email="s2@hkmu.edu.hk",
        )

        is_dup, similar = await self.service.check_duplicate(
            email2, existing_emails=[email1], threshold=0.8
        )
        assert is_dup is False
        assert similar is None

    @pytest.mark.asyncio
    async def test_skip_self(self):
        """Should skip itself during duplicate check."""
        email = Email(
            id="e001",
            subject="test",
            body="test content",
            sender_email="a@b.com",
        )

        is_dup, similar = await self.service.check_duplicate(
            email, existing_emails=[email], threshold=0.8
        )
        assert is_dup is False

    @pytest.mark.asyncio
    async def test_custom_threshold(self):
        """Custom similarity threshold."""
        email1 = Email(
            id="e001",
            subject="Homework question",
            body="How do I solve the homework?",
            sender_email="a@b.com",
        )
        email2 = Email(
            id="e002",
            subject="Exam question",
            body="How should I prepare for the exam?",
            sender_email="a@b.com",
        )

        # High threshold (0.9) → not a duplicate
        is_dup, _ = await self.service.check_duplicate(
            email2, existing_emails=[email1], threshold=0.9
        )
        assert is_dup is False

        # Low threshold (0.3) → may be flagged (depends on SequenceMatcher)
        is_dup, _ = await self.service.check_duplicate(
            email2, existing_emails=[email1], threshold=0.3
        )
        # Result depends on actual similarity; just verify no error
        assert isinstance(is_dup, bool)


class TestClassifyEmail:
    """Email classification tests."""

    @pytest.mark.asyncio
    async def test_academic_classification(self):
        """Test that academic emails are correctly classified."""
        service = ClassificationService.__new__(ClassificationService)
        service._db = MagicMock()
        service._categories = None

        # Mock get_categories to return a list of categories
        service._db.get_categories = AsyncMock(return_value=[
            {"id": "c1", "name": "Academic", "priority": 1, "keywords": ["homework", "exam", "grade", "course"]},
            {"id": "c2", "name": "Administrative", "priority": 2, "keywords": ["leave", "registration", "payment"]},
            {"id": "c3", "name": "Other", "priority": 5, "keywords": []},
        ])

        email = Email(
            id="e001",
            subject="About final exam",
            body="Hello Professor, what is the schedule for the final exam?",
            sender_email="s@hkmu.edu.hk",
        )

        category, confidence = await service.classify_email(email)
        assert category.name == "Academic"
        assert confidence > 0

    @pytest.mark.asyncio
    async def test_administrative_classification(self):
        """Test that administrative emails are correctly classified."""
        service = ClassificationService.__new__(ClassificationService)
        service._db = MagicMock()
        service._categories = None

        service._db.get_categories = AsyncMock(return_value=[
            {"id": "c1", "name": "Academic", "priority": 1, "keywords": ["homework", "exam"]},
            {"id": "c2", "name": "Administrative", "priority": 2, "keywords": ["leave", "registration", "payment"]},
            {"id": "c3", "name": "Other", "priority": 5, "keywords": []},
        ])

        email = Email(
            id="e002",
            subject="Leave request",
            body="Hello Professor, I need leave next week for course registration.",
            sender_email="s@hkmu.edu.hk",
        )

        category, confidence = await service.classify_email(email)
        assert category.name == "Administrative"

    @pytest.mark.asyncio
    async def test_fallback_to_other(self):
        """Test that unmatched emails fall back to the 'Other' category."""
        service = ClassificationService.__new__(ClassificationService)
        service._db = MagicMock()
        service._categories = None

        service._db.get_categories = AsyncMock(return_value=[
            {"id": "c1", "name": "Academic", "priority": 1, "keywords": ["homework", "exam"]},
            {"id": "c2", "name": "Administrative", "priority": 2, "keywords": ["leave", "registration"]},
            {"id": "c3", "name": "Other", "priority": 5, "keywords": []},
        ])

        email = Email(
            id="e003",
            subject="Hello",
            body="Hello",
            sender_email="s@hkmu.edu.hk",
        )

        category, confidence = await service.classify_email(email)
        assert category.name == "Other"
