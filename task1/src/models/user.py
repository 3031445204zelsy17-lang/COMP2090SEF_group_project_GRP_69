"""User Model

Defines user-related classes using inheritance to support different user roles.
Demonstrates OOP Inheritance concept.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from .base import AbstractPerson
from .email import Email

if TYPE_CHECKING:
    from .reply import Reply
    from .knowledge_source import KnowledgeSource


class User(AbstractPerson):
    """User base class.

    Inherits from AbstractPerson, providing common user implementation.
    """

    def __init__(
        self,
        name: str,
        email: str,
        role: str = "user",
        user_id: Optional[str] = None,
    ):
        """Initialize a user.

        Args:
            name: User's full name.
            email: User's email address.
            role: User's role (e.g., "professor", "student").
            user_id: Unique user identifier.
        """
        super().__init__(name, email)
        self.__role = role
        self.__user_id = user_id
        self.__inbox: List[Email] = []

    @property
    def role(self) -> str:
        """Get the user's role."""
        return self.__role

    @property
    def user_id(self) -> Optional[str]:
        """Get the user ID."""
        return self.__user_id

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Send an email.

        Args:
            recipient: Recipient's email address.
            subject: Email subject line.
            body: Email body content.

        Returns:
            True if the email was sent successfully.
        """
        print(f"[Email] {self.email} -> {recipient} | Subject: {subject}")
        return True

    def receive_email(self) -> List[Email]:
        """Receive emails.

        Returns:
            A list of emails in the inbox.
        """
        return self.__inbox

    def add_to_inbox(self, email: Email) -> None:
        """Add an email to the inbox.

        Args:
            email: The email to add.
        """
        self.__inbox.append(email)

    def __str__(self) -> str:
        """Return a human-readable summary of this user."""
        return f"{self.__class__.__name__}(name={self.name}, email={self.email}, role={self.__role})"


class Professor(User):
    """Professor class.

    Inherits from User, implementing professor-specific behavior.
    """

    def __init__(
        self,
        name: str,
        email: str,
        department: str = "",
        user_id: Optional[str] = None,
    ):
        """Initialize a professor.

        Args:
            name: Professor's full name.
            email: Professor's email address.
            department: Academic department.
            user_id: Unique user identifier.
        """
        super().__init__(name, email, role="professor", user_id=user_id)
        self.__department = department

    @property
    def department(self) -> str:
        """Get the department."""
        return self.__department

    def approve_reply(self, reply) -> bool:
        """Approve an auto-generated reply.

        Args:
            reply: The reply to approve.

        Returns:
            True if the approval was successful.
        """
        reply.approved = True
        print(f"[Approved] Professor '{self.name}' approved reply {reply.id} at {datetime.now():%Y-%m-%d %H:%M}")
        return True

    def reject_reply(self, reply, reason: str = "") -> bool:
        """Reject an auto-generated reply.

        Args:
            reply: The reply to reject.
            reason: Reason for rejection.

        Returns:
            True if the rejection was successful.
        """
        reply.approved = False
        if reason:
            reply.set_rejection_reason(reason)
        print(f"[Rejected] Professor '{self.name}' rejected reply {reply.id} at {datetime.now():%Y-%m-%d %H:%M} | Reason: {reason}")
        return True

    def review_summary(self) -> Dict[str, Any]:
        """Return a summary of the professor's profile for display purposes.

        Returns:
            A dictionary with professor profile information.
        """
        return {
            "name": self.name,
            "email": self.email,
            "department": self.__department,
            "role": self.role,
        }

    def __str__(self) -> str:
        """Return a human-readable summary of this professor."""
        return f"Professor(name={self.name}, email={self.email}, department={self.__department})"


class Student(User):
    """Student class.

    Inherits from User, implementing student-specific behavior.
    Students can compose emails, optionally using knowledge sources
    to reference relevant course materials.
    """

    def __init__(
        self,
        name: str,
        email: str,
        student_id: str = "",
        user_id: Optional[str] = None,
    ):
        """Initialize a student.

        Args:
            name: Student's full name.
            email: Student's email address.
            student_id: Student ID number.
            user_id: Unique user identifier.
        """
        super().__init__(name, email, role="student", user_id=user_id)
        self.__student_id = student_id

    @property
    def student_id(self) -> str:
        """Get the student ID."""
        return self.__student_id

    def compose_email(
        self,
        subject: str,
        body: str,
        knowledge_sources: Optional[List["KnowledgeSource"]] = None,
    ) -> "Email":
        """Compose a formatted student email.

        If knowledge sources are provided, appends referenced material
        titles to the email body so the professor knows which topics
        the student has already consulted.

        Demonstrates OOP Composition: Student uses KnowledgeSource
        objects to build a more informative email.

        Args:
            subject: Email subject line.
            body: Email body content (the student's question or request).
            knowledge_sources: Optional list of relevant knowledge sources
                               the student has consulted.

        Returns:
            A StudentEmail instance ready to be submitted.
        """
        from .email import StudentEmail

        # Append knowledge source references if available
        if knowledge_sources:
            ref_titles = [f"  - {src.title}" for src in knowledge_sources]
            body += "\n\n---\nReferenced course materials:\n" + "\n".join(ref_titles)

        email = StudentEmail(
            id="",  # Temporary ID; assigned after database save
            subject=subject,
            body=body,
            sender_email=self.email,
            sender_name=self.name,
            student_id=self.__student_id,
        )
        return email

    def __str__(self) -> str:
        """Return a human-readable summary of this student."""
        return f"Student(name={self.name}, email={self.email}, student_id={self.__student_id})"
