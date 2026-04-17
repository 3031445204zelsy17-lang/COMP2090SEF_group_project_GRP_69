"""Classification Service

Provides email classification and duplicate detection functionality.
"""

from typing import List, Optional, Tuple
from difflib import SequenceMatcher

from ..models.email import Email
from ..models.category import Category, CategoryType
from ..db.supabase_client import get_db


class ClassificationService:
    """Classification service.

    Responsible for automatic email classification and duplicate detection.
    """

    # Similarity threshold for duplicate detection (0-1, higher means stricter)
    SIMILARITY_THRESHOLD: float = 0.8
    # Minimum keyword match score to assign a category (below this -> "other")
    MIN_MATCH_SCORE: float = 0.1
    # Max number of recent emails to check for duplicates
    DUPLICATE_CHECK_LIMIT: int = 100

    # Category keyword mapping
    CATEGORY_KEYWORDS = {
        CategoryType.ACADEMIC: [
            "作业", "homework", "assignment",
            "考试", "exam", "test",
            "课程", "course", "class",
            "成绩", "grade", "score",
            "学分", "credit",
            "论文", "paper", "thesis",
            "项目", "project",
            "实验", "lab", "experiment",
            "讲座", "lecture",
            "辅导", "tutorial",
        ],
        CategoryType.ADMINISTRATIVE: [
            "请假", "leave", "absence",
            "证明", "certificate",
            "注册", "register", "enroll",
            "退课", "drop", "withdraw",
            "选课", "select course",
            "缴费", "payment", "fee",
            "办公室", "office",
            "截止", "deadline",
            "申请", "apply", "application",
        ],
        CategoryType.FAQ: [
            "时间", "time", "when",
            "地点", "location", "where", "room",
            "办公", "office hour",
            "咨询", "consult", "ask",
            "如何", "how to",
            "什么是", "what is",
            "为什么", "why",
        ],
    }

    def __init__(self):
        self._db = get_db()
        self._categories: Optional[List[Category]] = None

    async def get_categories(self) -> List[Category]:
        """Retrieve all categories.

        Returns:
            A list of Category objects.
        """
        if self._categories is None:
            data_list = await self._db.get_categories()
            self._categories = [
                Category(
                    id=data["id"],
                    name=data["name"],
                    priority=data.get("priority", 5),
                    keywords=data.get("keywords", []),
                )
                for data in data_list
            ]
        return self._categories

    async def classify_email(self, email: Email) -> Tuple[Category, float]:
        """Classify an email using keyword matching.

        Args:
            email: The email to classify.

        Returns:
            A tuple of (Category object, confidence score).
        """
        categories = await self.get_categories()

        # Combine subject and body for matching
        text = f"{email.subject} {email.body}".lower()

        # Calculate match score for each category
        best_category = None
        best_score = 0.0

        for category in categories:
            score = self._calculate_match_score(text, category.keywords)
            if score > best_score:
                best_score = score
                best_category = category

        # If no match, fall back to "other" category
        if best_category is None or best_score < self.MIN_MATCH_SCORE:
            for category in categories:
                if category.priority >= 5:  # Priority 5 typically means "other"
                    best_category = category
                    best_score = 0.0
                    break

        return best_category, best_score

    def _calculate_match_score(self, text: str, keywords: List[str]) -> float:
        """Calculate keyword match score.

        Algorithm: counts how many category keywords appear in the text,
        divided by the total number of keywords to get a match ratio.
        Example: 3 out of 8 keywords matched -> score = 3/8 = 0.375

        Args:
            text: The text content to match against.
            keywords: List of keywords for the category.

        Returns:
            Match score between 0.0 and 1.0.
        """
        if not keywords:
            return 0.0

        text_lower = text.lower()
        matched = sum(1 for kw in keywords if kw.lower() in text_lower)

        return matched / len(keywords)

    async def check_duplicate(
        self,
        email: Email,
        existing_emails: Optional[List[Email]] = None,
        threshold: float = SIMILARITY_THRESHOLD,
    ) -> Tuple[bool, Optional[Email]]:
        """Check whether an email is a duplicate of an existing one.

        Uses text similarity (SequenceMatcher) to detect duplicates.

        Args:
            email: The email to check.
            existing_emails: Optional list of existing emails to compare against.
                             If not provided, recent emails are fetched from the database.
            threshold: Similarity threshold (0-1).

        Returns:
            A tuple of (is_duplicate, similar_email).
        """
        if existing_emails is None:
            # Only check recent emails
            existing_emails = await self._db.get_emails(limit=self.DUPLICATE_CHECK_LIMIT)
            existing_emails = [
                Email(
                    id=e["id"],
                    subject=e["subject"],
                    body=e["body"],
                    sender_email=e["sender_email"],
                    sender_name=e.get("sender_name"),
                )
                for e in existing_emails
            ]

        email_text = f"{email.subject} {email.body}"

        for existing in existing_emails:
            if existing.id == email.id:
                continue

            existing_text = f"{existing.subject} {existing.body}"

            # Calculate similarity
            similarity = self._calculate_similarity(email_text, existing_text)

            if similarity >= threshold:
                return True, existing

        return False, None

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using SequenceMatcher.

        Args:
            text1: First text.
            text2: Second text.

        Returns:
            Similarity ratio between 0.0 and 1.0.
        """
        # Normalize text
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()

        return SequenceMatcher(None, text1, text2).ratio()

    async def auto_classify(self, email: Email) -> Category:
        """Classify an email and update the database.

        Args:
            email: The email to classify.

        Returns:
            The assigned Category.
        """
        category, confidence = await self.classify_email(email)

        # Update the database
        if category:
            await self._db.update_email(
                email.id,
                category_id=category.id,
                status="classified",
            )

        # Check for duplicates
        is_duplicate, similar_email = await self.check_duplicate(email)
        if is_duplicate:
            await self._db.update_email(email.id, is_duplicate=True)

        return category
