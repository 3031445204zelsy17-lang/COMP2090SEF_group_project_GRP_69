"""Abstract Base Classes

Defines the abstract base classes used throughout the system,
demonstrating OOP Abstraction and Inheritance concepts.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .email import Email
    from .reply import Reply


class AbstractPerson(ABC):
    """Abstract base class for all person types.

    Defines common attributes and behaviors for people in the system.
    Demonstrates OOP Abstraction concept.
    """

    def __init__(self, name: str, email: str):
        """Initialize a person.

        Args:
            name: Person's full name.
            email: Person's email address.
        """
        self.__name = name  # Private attribute (Encapsulation)
        self.__email = email
        self.__created_at = datetime.now()

    @property
    def name(self) -> str:
        """Get the person's name."""
        return self.__name

    @property
    def email(self) -> str:
        """Get the person's email address."""
        return self.__email

    @property
    def created_at(self) -> datetime:
        """Get the account creation timestamp."""
        return self.__created_at

    @abstractmethod
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Send an email to a recipient (abstract method).

        Args:
            recipient: Recipient's email address.
            subject: Email subject line.
            body: Email body content.

        Returns:
            True if the email was sent successfully.
        """
        pass

    @abstractmethod
    def receive_email(self) -> list:
        """Receive emails (abstract method).

        Returns:
            A list of received emails.
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.__name!r}, email={self.__email!r})"


class AbstractEmail(ABC):
    """Abstract base class for all email types.

    Defines common attributes for emails in the system.
    """

    def __init__(
        self,
        id: str,
        subject: str,
        body: str,
        sender_email: str,
        sender_name: Optional[str] = None,
    ):
        """Initialize an email.

        Args:
            id: Unique email identifier.
            subject: Email subject line.
            body: Email body content.
            sender_email: Sender's email address.
            sender_name: Sender's display name.
        """
        self.__id = id
        self.__subject = subject
        self.__body = body
        self.__sender_email = sender_email
        self.__sender_name = sender_name
        self.__timestamp = datetime.now()

    @property
    def id(self) -> str:
        """Get the email ID."""
        return self.__id

    @property
    def subject(self) -> str:
        """Get the email subject."""
        return self.__subject

    @property
    def body(self) -> str:
        """Get the email body."""
        return self.__body

    @property
    def sender_email(self) -> str:
        """Get the sender's email address."""
        return self.__sender_email

    @property
    def sender_name(self) -> Optional[str]:
        """Get the sender's display name."""
        return self.__sender_name

    @property
    def timestamp(self) -> datetime:
        """Get the email timestamp."""
        return self.__timestamp

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.__id!r}, subject={self.__subject!r})"


class ReplyStrategy(ABC):
    """Abstract base class for reply generation strategies.

    Uses the Strategy Pattern to define a common interface for different
    reply generation approaches. Demonstrates OOP Polymorphism concept.
    """

    @abstractmethod
    def generate(self, email: "Email") -> "Reply":
        """Generate a reply for the given email.

        Args:
            email: The email to reply to.

        Returns:
            A Reply object containing the generated response.
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of this strategy."""
        pass
