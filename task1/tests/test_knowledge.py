"""KnowledgeSource Model Unit Tests

Tests for KnowledgeSource class creation, keyword management, and relevance scoring.
"""

import pytest
from src.models.knowledge_source import KnowledgeSource


class TestKnowledgeSourceCreation:
    """Creation tests."""

    def test_create_source(self):
        """Test creating a knowledge source."""
        source = KnowledgeSource(
            title="Course Syllabus",
            content="This course covers data structures and algorithms",
            keywords=["data structures", "algorithms", "course"],
        )
        assert source.title == "Course Syllabus"
        assert source.content == "This course covers data structures and algorithms"
        assert len(source.keywords) == 3
        assert source.id is None
        assert source.category is None

    def test_create_with_all_fields(self):
        """Test creating a source with all fields populated."""
        source = KnowledgeSource(
            title="FAQ",
            content="Frequently asked questions and answers",
            keywords=["FAQ"],
            category="faq",
            source_id="src001",
            created_by="prof001",
        )
        assert source.id == "src001"
        assert source.category == "faq"
        assert source.created_by == "prof001"

    def test_default_empty_keywords(self):
        """Test that keywords default to empty list."""
        source = KnowledgeSource(title="test", content="test")
        assert source.keywords == []


class TestKnowledgeSourceKeywords:
    """Keyword management tests."""

    def test_add_keyword(self):
        """Test adding a keyword."""
        source = KnowledgeSource(title="test", content="test")
        source.add_keyword("Python")
        assert "python" in source.keywords  # Auto-lowercased

    def test_add_keyword_strips_whitespace(self):
        """Test that whitespace is stripped from keywords."""
        source = KnowledgeSource(title="test", content="test")
        source.add_keyword("  testing  ")
        assert "testing" in source.keywords

    def test_add_duplicate_keyword(self):
        """Test that adding a duplicate keyword does not create duplicates."""
        source = KnowledgeSource(title="test", content="test")
        source.add_keyword("test")
        source.add_keyword("TEST")  # Case-insensitive
        assert len(source.keywords) == 1

    def test_add_empty_keyword_ignored(self):
        """Test that empty keywords are ignored."""
        source = KnowledgeSource(title="test", content="test")
        source.add_keyword("")
        source.add_keyword("   ")
        assert len(source.keywords) == 0

    def test_remove_keyword(self):
        """Test removing a keyword (stored in lowercase)."""
        source = KnowledgeSource(title="test", content="test", keywords=["alpha", "beta"])
        assert source.remove_keyword("alpha") is True
        assert len(source.keywords) == 1

    def test_remove_keyword_case_insensitive(self):
        """Test that keyword removal is case-insensitive."""
        source = KnowledgeSource(title="test", content="test", keywords=["python"])
        assert source.remove_keyword("PYTHON") is True
        assert len(source.keywords) == 0

    def test_remove_nonexistent_keyword(self):
        """Test removing a non-existent keyword returns False."""
        source = KnowledgeSource(title="test", content="test", keywords=["A"])
        assert source.remove_keyword("Z") is False

    def test_set_keywords(self):
        """Test batch-setting keywords."""
        source = KnowledgeSource(title="test", content="test")
        source.set_keywords(["Python", "  R  ", "", "Java"])
        assert source.keywords == ["python", "r", "java"]

    def test_keywords_returns_copy(self):
        """Test that keywords returns a copy."""
        source = KnowledgeSource(title="test", content="test", keywords=["A"])
        kw = source.keywords
        kw.append("B")
        assert len(source.keywords) == 1


class TestRelevanceScore:
    """Relevance score calculation tests."""

    def test_empty_content(self):
        """Test with empty email content."""
        source = KnowledgeSource(title="test", content="test", keywords=["test"])
        assert source.calculate_relevance_score("") == 0.0

    def test_keyword_match_only(self):
        """Test keyword-only matching."""
        source = KnowledgeSource(
            title="Unrelated title",
            content="Unrelated content xyz",
            keywords=["homework", "exam"],
        )
        score = source.calculate_relevance_score("When is the homework due? What about the exam schedule?")
        # Keyword match 2/2 = 1.0, weight 0.5 -> at least 0.5
        assert score >= 0.5

    def test_no_match(self):
        """Test with no matching content."""
        source = KnowledgeSource(
            title="PE class",
            content="basketball, soccer, tennis",
            keywords=["sports", "exercise"],
        )
        score = source.calculate_relevance_score("When is the homework deadline?")
        assert score < 0.1

    def test_title_match(self):
        """Test title matching (using English for reliable word tokenization)."""
        source = KnowledgeSource(
            title="data structure course syllabus",
            content="course introduction",
            keywords=[],
        )
        score = source.calculate_relevance_score("data structure course schedule")
        assert score > 0

    def test_content_match(self):
        """Test content matching."""
        source = KnowledgeSource(
            title="FAQ",
            content="homework deadline is next friday, exam results in two weeks",
            keywords=[],
        )
        score = source.calculate_relevance_score("homework deadline and exam results?")
        assert score > 0

    def test_combined_score(self):
        """Test combined score (keywords + title + content)."""
        source = KnowledgeSource(
            title="Course Syllabus",
            content="This course covers data structures, algorithms, and Python programming",
            keywords=["course", "data structures", "algorithms"],
        )
        score = source.calculate_relevance_score("How to learn data structures and algorithms in this course?")
        # Keywords, title, and content all have matches — score should be high
        assert score > 0.3

    def test_score_max_is_one(self):
        """Test that score never exceeds 1.0."""
        source = KnowledgeSource(
            title="test test test",
            content="test test test",
            keywords=["test"],
        )
        score = source.calculate_relevance_score("test test test test")
        assert score <= 1.0


class TestPropertySetters:
    """Property setter tests."""

    def test_set_title_updates_timestamp(self):
        """Test that setting title updates updated_at."""
        source = KnowledgeSource(title="old", content="test")
        old_updated = source.updated_at
        source.title = "new"
        assert source.title == "new"
        assert source.updated_at >= old_updated

    def test_set_content_updates_timestamp(self):
        """Test that setting content updates updated_at."""
        source = KnowledgeSource(title="test", content="old")
        old_updated = source.updated_at
        source.content = "new"
        assert source.content == "new"
        assert source.updated_at >= old_updated

    def test_set_id(self):
        """Test setting the ID."""
        source = KnowledgeSource(title="test", content="test")
        assert source.id is None
        source.id = "src099"
        assert source.id == "src099"


class TestToDict:
    """to_dict tests."""

    def test_to_dict(self):
        """Test conversion to dictionary."""
        source = KnowledgeSource(
            title="Course Syllabus",
            content="Course content",
            keywords=["course"],
            category="academic",
            source_id="src001",
        )
        d = source.to_dict()
        assert d["id"] == "src001"
        assert d["title"] == "Course Syllabus"
        assert d["content"] == "Course content"
        assert d["keywords"] == ["course"]
        assert d["category"] == "academic"
        assert "created_at" in d
        assert "updated_at" in d

    def test_repr(self):
        """Test string representation."""
        source = KnowledgeSource(title="test", content="test", source_id="s1")
        assert "s1" in repr(source)
        assert "test" in repr(source)
