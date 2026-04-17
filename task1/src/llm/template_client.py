"""Template-based LLM Client

Drop-in replacement for DeepSeekClient that generates replies using
pre-defined templates instead of calling an external API.
Used in offline demo mode.
"""

from typing import List, Optional, Tuple

from ..models.knowledge_source import KnowledgeSource


class TemplateLLMClient:
    """Template-based LLM client for offline demo mode.

    Implements the same method signatures as DeepSeekClient (duck typing),
    so it can be injected via set_llm_backend() without changing any
    service or route code.
    """

    # Templates for reply generation
    REPLY_TEMPLATES = {
        "学术问题": (
            "Dear Student,\n\n"
            "Thank you for your inquiry about {subject}. "
            "Based on the course materials and lecture notes, "
            "please refer to the relevant chapters and assignment guidelines for detailed information. "
            "If you need further clarification, feel free to visit during office hours.\n\n"
            "Best regards"
        ),
        "行政事务": (
            "Dear Student,\n\n"
            "Thank you for your request regarding {subject}. "
            "Please visit the university administration office or check the student portal "
            "for the relevant forms and procedures. "
            "Make sure to submit all required documents before the deadline.\n\n"
            "Best regards"
        ),
        "常见问题": (
            "Dear Student,\n\n"
            "Your question about {subject} is a frequently asked question. "
            "You may find the answer in the course FAQ section or the student handbook. "
            "If you still need help, please do not hesitate to ask during the next class.\n\n"
            "Best regards"
        ),
        "default": (
            "Dear Student,\n\n"
            "Thank you for your email about {subject}. "
            "We have received your message and will get back to you as soon as possible. "
            "Please don't hesitate to contact us if you have any further questions.\n\n"
            "Best regards"
        ),
    }

    async def generate_reply(
        self,
        email_subject: str,
        email_body: str,
        category_name: str,
        knowledge_sources: Optional[List[KnowledgeSource]] = None,
    ) -> Tuple[str, List[str]]:
        """Generate a reply using templates.

        Args:
            email_subject: Email subject line.
            email_body: Email body content.
            category_name: Classification category name.
            knowledge_sources: Ignored in template mode.

        Returns:
            A tuple of (reply content, list of referenced source IDs).
        """
        template = self.REPLY_TEMPLATES.get(
            category_name,
            self.REPLY_TEMPLATES["default"],
        )
        content = template.format(subject=email_subject)
        referenced_ids = [s.id for s in (knowledge_sources or [])]
        return content, referenced_ids

    async def classify_email(
        self,
        email_subject: str,
        email_body: str,
        categories: List[str],
    ) -> str:
        """Classify an email using simple keyword matching.

        Note: ClassificationService already uses keyword-based classification
        without calling the LLM. This method exists as a fallback.

        Args:
            email_subject: Email subject line.
            email_body: Email body text.
            categories: List of available category names.

        Returns:
            The predicted category name.
        """
        text = f"{email_subject} {email_body}"

        # Simple keyword matching
        keyword_map = {
            "学术问题": ["作业", "考试", "课程", "成绩", "学分", "论文", "项目", "实验"],
            "行政事务": ["请假", "证明", "注册", "退课", "选课", "缴费", "申请"],
            "常见问题": ["时间", "地点", "办公", "咨询", "截止"],
        }

        best_category = None
        best_score = 0

        for cat_name, keywords in keyword_map.items():
            if cat_name not in categories:
                continue
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_category = cat_name

        return best_category or (categories[0] if categories else "其他")

    async def test_connection(self) -> bool:
        """Test connection (always succeeds in template mode)."""
        return True

    async def chat_edit_reply(
        self,
        current_reply: str,
        user_instruction: str,
    ) -> str:
        """Edit a reply based on simple rule matching.

        Args:
            current_reply: The current reply content.
            user_instruction: User instruction for editing.

        Returns:
            The modified reply content.
        """
        instruction_lower = user_instruction.lower()

        if "english" in instruction_lower or "英文" in instruction_lower:
            return (
                "Dear Student,\n\n"
                "Thank you for your email. We have received your message "
                "and will process your request as soon as possible. "
                "Please feel free to reach out if you have any further questions.\n\n"
                "Best regards"
            )
        elif "short" in instruction_lower or "简短" in instruction_lower:
            lines = current_reply.strip().split("\n")
            # Keep greeting + first substantive line + closing
            if len(lines) > 4:
                return "\n".join(lines[:2] + lines[-2:])
            return current_reply
        elif "formal" in instruction_lower or "正式" in instruction_lower:
            return (
                "Dear Student,\n\n"
                "Thank you for your correspondence. "
                "Your inquiry has been noted and will be addressed accordingly. "
                "Should you require any further assistance, "
                "please do not hesitate to contact this office.\n\n"
                "Yours sincerely,\nProfessor"
            )
        else:
            return current_reply
