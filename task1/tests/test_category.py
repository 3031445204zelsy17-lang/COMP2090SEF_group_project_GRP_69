"""Category Model Unit Tests

Tests for Category class creation, keyword matching, priority comparison, and operator overloading.
"""

import pytest
from src.models.category import Category, CategoryType


class TestCategory:
    """Category class tests."""

    def test_create_category(self):
        """Test creating a category."""
        cat = Category(id="c001", name="Academic", priority=1)
        assert cat.id == "c001"
        assert cat.name == "Academic"
        assert cat.priority == 1
        assert cat.keywords == []

    def test_create_category_with_keywords(self):
        """Test creating a category with keywords."""
        cat = Category(
            id="c002",
            name="Administrative",
            priority=2,
            keywords=["leave", "registration", "payment"],
        )
        assert len(cat.keywords) == 3
        assert "leave" in cat.keywords

    def test_priority_range_limit(self):
        """Test that priority is clamped to the 1-10 range."""
        # Priority too high should be clamped to 10
        cat_high = Category(id="c003", name="test", priority=999)
        assert cat_high.priority == 10

        # Priority too low should be clamped to 1
        cat_low = Category(id="c004", name="test", priority=-5)
        assert cat_low.priority == 1

        # Boundary value passes through unchanged
        cat_normal = Category(id="c005", name="test", priority=5)
        assert cat_normal.priority == 5

    def test_add_keyword(self):
        """Test adding a keyword."""
        cat = Category(id="c006", name="test", priority=5)
        cat.add_keyword("homework")
        assert "homework" in cat.keywords
        assert len(cat.keywords) == 1

    def test_add_duplicate_keyword(self):
        """Test that adding a duplicate keyword does not create duplicates."""
        cat = Category(id="c007", name="test", priority=5)
        cat.add_keyword("exam")
        cat.add_keyword("exam")
        assert len(cat.keywords) == 1

    def test_add_empty_keyword(self):
        """Test that empty keywords are ignored."""
        cat = Category(id="c008", name="test", priority=5)
        cat.add_keyword("")
        assert len(cat.keywords) == 0

    def test_remove_keyword(self):
        """Test removing a keyword."""
        cat = Category(id="c009", name="test", priority=5, keywords=["A", "B"])
        assert cat.remove_keyword("A") is True
        assert len(cat.keywords) == 1
        assert "B" in cat.keywords

    def test_remove_nonexistent_keyword(self):
        """Test removing a non-existent keyword returns False."""
        cat = Category(id="c010", name="test", priority=5, keywords=["A"])
        assert cat.remove_keyword("Z") is False
        assert len(cat.keywords) == 1

    def test_matches(self):
        """Test matches method — counts how many keywords appear in the text."""
        cat = Category(
            id="c011",
            name="Academic",
            priority=1,
            keywords=["homework", "exam", "grade", "course"],
        )
        # "homework" and "exam" are direct matches; "grade" appears inside "exam grade"
        matches = cat.matches("When is the homework due? How to check exam grade?")
        assert matches >= 2  # At least "homework" and "exam"

    def test_matches_case_insensitive(self):
        """Test that matches is case-insensitive."""
        cat = Category(
            id="c012",
            name="test",
            priority=5,
            keywords=["homework"],
        )
        assert cat.matches("I have a HOMEWORK question") == 1

    def test_keywords_copy(self):
        """Test that keywords property returns a copy, not a reference."""
        cat = Category(id="c013", name="test", priority=5, keywords=["A", "B"])
        kw = cat.keywords
        kw.append("C")
        assert len(cat.keywords) == 2  # Original data unaffected


class TestCategoryComparison:
    """Category operator overloading tests."""

    def test_lt_operator(self):
        """Test < operator (priority comparison)."""
        high = Category(id="c020", name="High priority", priority=1)
        low = Category(id="c021", name="Low priority", priority=5)
        assert high < low  # Lower priority number = higher importance
        assert not (low < high)

    def test_eq_operator(self):
        """Test == operator (based on id comparison)."""
        cat1 = Category(id="same", name="A", priority=1)
        cat2 = Category(id="same", name="B", priority=5)  # Different name/priority but same id
        assert cat1 == cat2

    def test_eq_different_id(self):
        """Test that different ids are not equal."""
        cat1 = Category(id="c100", name="A", priority=1)
        cat2 = Category(id="c200", name="A", priority=1)
        assert cat1 != cat2

    def test_eq_not_category(self):
        """Test comparison with non-Category objects."""
        cat = Category(id="c030", name="test", priority=1)
        assert cat != "not a category"
        assert cat != 42

    def test_hash(self):
        """Test hash value (based on id)."""
        cat1 = Category(id="same", name="A", priority=1)
        cat2 = Category(id="same", name="B", priority=5)
        assert hash(cat1) == hash(cat2)

    def test_sorting(self):
        """Test sorting by priority."""
        cats = [
            Category(id="c1", name="Other", priority=5),
            Category(id="c2", name="Academic", priority=1),
            Category(id="c3", name="Admin", priority=3),
        ]
        sorted_cats = sorted(cats)
        assert sorted_cats[0].name == "Academic"   # priority 1
        assert sorted_cats[1].name == "Admin"       # priority 3
        assert sorted_cats[2].name == "Other"       # priority 5


class TestCategoryType:
    """CategoryType enum tests."""

    def test_type_values(self):
        """Test enum values."""
        assert CategoryType.ACADEMIC == "academic"
        assert CategoryType.ADMINISTRATIVE == "administrative"
        assert CategoryType.FAQ == "faq"
        assert CategoryType.OTHER == "other"

    def test_category_type_property(self):
        """Test the category type property."""
        cat = Category(
            id="c040",
            name="Academic",
            priority=1,
            category_type=CategoryType.ACADEMIC,
        )
        assert cat.type == CategoryType.ACADEMIC

    def test_default_category_type(self):
        """Test that the default category type is OTHER."""
        cat = Category(id="c041", name="test", priority=5)
        assert cat.type == CategoryType.OTHER


class TestCategoryToDict:
    """Category to_dict tests."""

    def test_to_dict(self):
        """Test conversion to dictionary."""
        cat = Category(
            id="c050",
            name="Academic",
            priority=1,
            keywords=["homework", "exam"],
            category_type=CategoryType.ACADEMIC,
        )
        d = cat.to_dict()
        assert d["id"] == "c050"
        assert d["name"] == "Academic"
        assert d["priority"] == 1
        assert d["keywords"] == ["homework", "exam"]
        assert d["type"] == "academic"
