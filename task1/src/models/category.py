"""Category Model

Defines the email classification model used to categorize incoming emails.
"""

from typing import List, Optional
from enum import Enum


class CategoryType(str, Enum):
    """Category type enumeration."""

    ACADEMIC = "academic"            # Academic questions
    ADMINISTRATIVE = "administrative"  # Administrative affairs
    FAQ = "faq"                      # Frequently asked questions
    OTHER = "other"                  # Uncategorized


class Category:
    """Email category class.

    Represents a classification category for emails.
    """

    # Default category definitions
    DEFAULT_CATEGORIES = {
        CategoryType.ACADEMIC: {
            "name": "学术问题",
            "priority": 1,
            "keywords": ["作业", "考试", "课程", "成绩", "学分", "论文", "项目"],
        },
        CategoryType.ADMINISTRATIVE: {
            "name": "行政事务",
            "priority": 2,
            "keywords": ["请假", "证明", "注册", "退课", "选课", "缴费"],
        },
        CategoryType.FAQ: {
            "name": "常见问题",
            "priority": 3,
            "keywords": ["时间", "地点", "办公", "咨询"],
        },
        CategoryType.OTHER: {
            "name": "其他",
            "priority": 5,
            "keywords": [],
        },
    }

    def __init__(
        self,
        id: str,
        name: str,
        priority: int = 5,
        keywords: Optional[List[str]] = None,
        category_type: CategoryType = CategoryType.OTHER,
    ):
        """Initialize a category.

        Args:
            id: Unique category identifier.
            name: Display name of the category.
            priority: Priority level (1-10, 1 = highest).
            keywords: List of keywords associated with this category.
            category_type: Type of the category.
        """
        self.__id = id
        self.__name = name
        self.__priority = max(1, min(10, priority))  # Clamp to 1-10 range
        self.__keywords = keywords or []
        self.__type = category_type

    @property
    def id(self) -> str:
        """Get the category ID."""
        return self.__id

    @property
    def name(self) -> str:
        """Get the category name."""
        return self.__name

    @property
    def priority(self) -> int:
        """Get the priority level."""
        return self.__priority

    @property
    def keywords(self) -> List[str]:
        """Get a copy of the keyword list."""
        return self.__keywords.copy()

    @property
    def type(self) -> CategoryType:
        """Get the category type."""
        return self.__type

    def add_keyword(self, keyword: str) -> None:
        """Add a keyword to the category.

        Args:
            keyword: The keyword to add.
        """
        if keyword and keyword not in self.__keywords:
            self.__keywords.append(keyword)

    def remove_keyword(self, keyword: str) -> bool:
        """Remove a keyword from the category.

        Args:
            keyword: The keyword to remove.

        Returns:
            True if the keyword was removed, False if not found.
        """
        if keyword in self.__keywords:
            self.__keywords.remove(keyword)
            return True
        return False

    def matches(self, text: str) -> int:
        """Count how many keywords match the given text.

        Args:
            text: The text to check against.

        Returns:
            The number of matching keywords.
        """
        text_lower = text.lower()
        return sum(1 for kw in self.__keywords if kw.lower() in text_lower)

    def __lt__(self, other: "Category") -> bool:
        """Less-than operator overload (Polymorphism).

        Compares by priority for sorting.

        Args:
            other: Another category to compare with.

        Returns:
            True if this category has higher priority (lower number).
        """
        return self.__priority < other.__priority

    def __eq__(self, other: object) -> bool:
        """Equality operator overload."""
        if not isinstance(other, Category):
            return False
        return self.__id == other.__id

    def __hash__(self) -> int:
        """Hash function overload."""
        return hash(self.__id)

    def __repr__(self) -> str:
        return f"Category(id={self.__id!r}, name={self.__name!r}, priority={self.__priority})"

    def to_dict(self) -> dict:
        """Convert the category to a dictionary.

        Returns:
            A dictionary containing all category fields.
        """
        return {
            "id": self.__id,
            "name": self.__name,
            "priority": self.__priority,
            "keywords": self.__keywords,
            "type": self.__type.value,
        }
