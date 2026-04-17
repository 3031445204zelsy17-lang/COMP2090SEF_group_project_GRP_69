# OOP Model Classes
from .base import AbstractPerson, AbstractEmail, ReplyStrategy
from .user import User, Professor, Student
from .email import Email, StudentEmail, FAQEmail
from .category import Category
from .reply import Reply
from .knowledge_source import KnowledgeSource
from .strategies import AutoReplyStrategy, TemplateReplyStrategy, ManualReplyStrategy
from .email_processor import EmailProcessor
from .factory import EmailFactory

__all__ = [
    "AbstractPerson",
    "AbstractEmail",
    "ReplyStrategy",
    "User",
    "Professor",
    "Student",
    "Email",
    "StudentEmail",
    "FAQEmail",
    "Category",
    "Reply",
    "KnowledgeSource",
    "AutoReplyStrategy",
    "TemplateReplyStrategy",
    "ManualReplyStrategy",
    "EmailProcessor",
    "EmailFactory",
]
