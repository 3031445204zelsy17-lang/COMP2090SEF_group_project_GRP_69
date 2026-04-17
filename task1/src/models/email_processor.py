"""Email Processor - Composition Pattern Demonstration

This module defines the EmailProcessor class, which explicitly demonstrates
OOP Composition. An EmailProcessor composes multiple independent service
objects to build a complete email processing pipeline.

Composition vs Inheritance:
- Inheritance ("is-a"): Professor IS-A User
- Composition ("has-a"): EmailProcessor HAS-A Classifier and HAS-A ReplyGenerator
"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .email import Email
    from .reply import Reply
    from .category import Category


class EmailProcessor:
    """Email processing pipeline that composes multiple services.

    Demonstrates OOP Composition: instead of inheriting behavior,
    this class combines independent objects (classifier + reply generator)
    to achieve complex functionality through delegation.

    This is the preferred pattern when classes represent components that
    can be swapped or reused independently.

    Example:
        processor = EmailProcessor(classifier=svc, reply_generator=svc)
        category, reply = await processor.process(email)
    """

    def __init__(self, classifier, reply_generator):
        """Initialize the processor with composed services.

        Args:
            classifier: A service that classifies emails (e.g. ClassificationService).
                        Demonstrates Composition: EmailProcessor "has-a" classifier.
            reply_generator: A service that generates replies (e.g. ReplyService).
                             Demonstrates Composition: EmailProcessor "has-a" reply_generator.
        """
        # Composition: combining independent objects to build complex behavior
        self._classifier = classifier
        self._reply_generator = reply_generator

    async def process(self, email: "Email") -> tuple:
        """Run the full email processing pipeline.

        Step 1: Classify the email into a category.
        Step 2: Generate a reply based on the classification.

        Args:
            email: The email to process.

        Returns:
            A tuple of (Category, Reply) representing the processing results.
        """
        # Step 1: Delegate classification to the composed classifier
        category = await self._classifier.auto_classify(email)

        # Step 2: Delegate reply generation to the composed reply generator
        reply = await self._reply_generator.generate_reply(email)

        return category, reply

    async def classify_only(self, email: "Email") -> "Category":
        """Classify an email without generating a reply.

        Args:
            email: The email to classify.

        Returns:
            The assigned Category.
        """
        return await self._classifier.auto_classify(email)

    async def generate_reply_only(self, email: "Email") -> "Reply":
        """Generate a reply for an already-classified email.

        Args:
            email: The email to reply to (should already be classified).

        Returns:
            The generated Reply.
        """
        return await self._reply_generator.generate_reply(email)

    def __repr__(self) -> str:
        return (
            f"EmailProcessor("
            f"classifier={self._classifier.__class__.__name__}, "
            f"reply_generator={self._reply_generator.__class__.__name__})"
        )
