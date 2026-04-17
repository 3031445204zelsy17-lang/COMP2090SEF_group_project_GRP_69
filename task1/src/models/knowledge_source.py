"""Knowledge Source Model

Defines the knowledge source / knowledge base model.
Knowledge sources store reference materials uploaded by professors
to guide AI-generated replies.
"""

from datetime import datetime
from typing import List, Optional
import re


class KnowledgeSource:
    """Knowledge source / knowledge base class.

    Stores reference materials such as course syllabi, FAQs, and
    assignment guidelines uploaded by professors. Used to guide
    AI in generating accurate and relevant replies.
    """

    # Weights for relevance score calculation
    KEYWORD_WEIGHT: float = 0.5   # Keywords are the most precise indicator
    TITLE_WEIGHT: float = 0.2     # Title usually summarizes the topic
    CONTENT_WEIGHT: float = 0.3   # Content word overlap supplements keyword coverage

    def __init__(
        self,
        title: str,
        content: str,
        keywords: Optional[List[str]] = None,
        category: Optional[str] = None,
        source_id: Optional[str] = None,
        created_by: Optional[str] = None,
    ):
        """Initialize a knowledge source.

        Args:
            title: Title of the knowledge source.
            content: Body content of the knowledge source.
            keywords: List of keyword tags.
            category: Associated classification category.
            source_id: Unique source identifier.
            created_by: ID of the user who created this source.
        """
        self.__id = source_id
        self.__title = title
        self.__content = content
        self.__keywords = keywords or []
        self.__category = category
        self.__created_by = created_by
        self.__created_at = datetime.now()
        self.__updated_at = datetime.now()

    @property
    def id(self) -> Optional[str]:
        """Get the source ID."""
        return self.__id

    @id.setter
    def id(self, value: str) -> None:
        """Set the source ID."""
        self.__id = value

    @property
    def title(self) -> str:
        """Get the title."""
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """Set the title."""
        self.__title = value
        self.__updated_at = datetime.now()

    @property
    def content(self) -> str:
        """Get the content."""
        return self.__content

    @content.setter
    def content(self, value: str) -> None:
        """Set the content."""
        self.__content = value
        self.__updated_at = datetime.now()

    @property
    def keywords(self) -> List[str]:
        """Get a copy of the keyword list."""
        return self.__keywords.copy()

    @property
    def category(self) -> Optional[str]:
        """Get the associated category."""
        return self.__category

    @property
    def created_by(self) -> Optional[str]:
        """Get the creator's user ID."""
        return self.__created_by

    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp."""
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        """Get the last update timestamp."""
        return self.__updated_at

    def add_keyword(self, keyword: str) -> None:
        """Add a keyword tag.

        Args:
            keyword: The keyword to add (whitespace trimmed, stored lowercase).
        """
        keyword = keyword.strip().lower()
        if keyword and keyword not in self.__keywords:
            self.__keywords.append(keyword)
            self.__updated_at = datetime.now()

    def remove_keyword(self, keyword: str) -> bool:
        """Remove a keyword tag.

        Args:
            keyword: The keyword to remove.

        Returns:
            True if the keyword was removed, False if not found.
        """
        keyword = keyword.strip().lower()
        if keyword in self.__keywords:
            self.__keywords.remove(keyword)
            self.__updated_at = datetime.now()
            return True
        return False

    def set_keywords(self, keywords: List[str]) -> None:
        """Replace the keyword list with a new set.

        Args:
            keywords: The new list of keywords.
        """
        self.__keywords = [kw.strip().lower() for kw in keywords if kw.strip()]
        self.__updated_at = datetime.now()

    def calculate_relevance_score(self, email_content: str) -> float:
        """Calculate relevance score against an email's content.

        Uses weighted keyword matching and content overlap to estimate
        how relevant this knowledge source is to the given email.

        Args:
            email_content: The email content to compare against.

        Returns:
            A relevance score between 0.0 and 1.0.
        """
        if not email_content:
            return 0.0

        email_lower = email_content.lower()

        # 1. Keyword match score
        keyword_score = 0.0
        if self.__keywords:
            matched_keywords = sum(
                1 for kw in self.__keywords if kw in email_lower
            )
            keyword_score = matched_keywords / len(self.__keywords)

        # 2. Title word overlap score
        title_score = 0.0
        if self.__title:
            title_words = set(re.findall(r"\w+", self.__title.lower()))
            email_words = set(re.findall(r"\w+", email_lower))
            if title_words:
                title_score = len(title_words & email_words) / len(title_words)

        # 3. Content word overlap score (with stop-word filtering)
        content_score = 0.0
        content_words = set(re.findall(r"\w+", self.__content.lower()))
        email_words = set(re.findall(r"\w+", email_lower))
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "must", "shall",
            "can", "need", "dare", "ought", "used", "to", "of", "in",
            "for", "on", "with", "at", "by", "from", "as", "into",
            "through", "during", "before", "after", "above", "below",
            "between", "under", "again", "further", "then", "once",
            "的", "是", "在", "有", "和", "了", "不", "这", "我", "你",
            "他", "她", "它", "们", "着", "过", "会", "能", "要", "就",
        }
        content_words = content_words - stop_words
        email_words = email_words - stop_words

        if content_words:
            content_score = len(content_words & email_words) / min(
                len(content_words), 20
            )

        # Weighted average score
        total_score = (
            keyword_score * self.KEYWORD_WEIGHT
            + title_score * self.TITLE_WEIGHT
            + content_score * self.CONTENT_WEIGHT
        )

        return min(1.0, total_score)

    def __repr__(self) -> str:
        return f"KnowledgeSource(id={self.__id!r}, title={self.__title!r})"

    def to_dict(self) -> dict:
        """Convert the knowledge source to a dictionary.

        Returns:
            A dictionary containing all source fields.
        """
        return {
            "id": self.__id,
            "title": self.__title,
            "content": self.__content,
            "keywords": self.__keywords,
            "category": self.__category,
            "created_by": self.__created_by,
            "created_at": self.__created_at.isoformat(),
            "updated_at": self.__updated_at.isoformat(),
        }
