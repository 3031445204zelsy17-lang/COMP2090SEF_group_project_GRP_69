"""Reply Model Unit Tests

Tests for Reply class creation, approval state changes, and referenced source management.
"""

import pytest
from src.models.reply import Reply


class TestReply:
    """Reply class tests."""

    def test_create_auto_reply(self):
        """Test creating an auto-generated reply."""
        reply = Reply(content="This is an auto reply", is_auto=True, email_id="e001")
        assert reply.content == "This is an auto reply"
        assert reply.is_auto is True
        assert reply.approved is False
        assert reply.email_id == "e001"
        assert reply.id is None  # None before database save

    def test_create_manual_reply(self):
        """Test creating a manual reply."""
        reply = Reply(content="Manual reply", is_auto=False)
        assert reply.is_auto is False

    def test_default_auto(self):
        """Test that default is_auto is True."""
        reply = Reply(content="test")
        assert reply.is_auto is True

    def test_default_not_approved(self):
        """Test that default approval status is False."""
        reply = Reply(content="test")
        assert reply.approved is False

    def test_set_id(self):
        """Test setting a reply ID."""
        reply = Reply(content="test")
        assert reply.id is None
        reply.id = "r001"
        assert reply.id == "r001"

    def test_approve_reply(self):
        """Test approving a reply."""
        reply = Reply(content="test")
        assert reply.approved is False
        reply.approved = True
        assert reply.approved is True

    def test_reject_reply(self):
        """Test rejecting a reply (approve then reject)."""
        reply = Reply(content="test")
        reply.approved = True
        reply.approved = False
        assert reply.approved is False

    def test_update_content(self):
        """Test updating reply content."""
        reply = Reply(content="Original content")
        reply.content = "Updated content"
        assert reply.content == "Updated content"


class TestReferencedSources:
    """Referenced knowledge source tests."""

    def test_default_empty_sources(self):
        """Test that referenced_sources defaults to empty."""
        reply = Reply(content="test")
        assert reply.referenced_sources == []

    def test_create_with_sources(self):
        """Test creating a reply with referenced sources."""
        reply = Reply(content="test", referenced_sources=["src001", "src002"])
        assert len(reply.referenced_sources) == 2
        assert "src001" in reply.referenced_sources

    def test_add_source(self):
        """Test adding a referenced source."""
        reply = Reply(content="test")
        reply.add_referenced_source("src001")
        assert "src001" in reply.referenced_sources

    def test_add_duplicate_source(self):
        """Test that adding a duplicate source does not create duplicates."""
        reply = Reply(content="test")
        reply.add_referenced_source("src001")
        reply.add_referenced_source("src001")
        assert len(reply.referenced_sources) == 1

    def test_sources_is_copy(self):
        """Test that referenced_sources returns a copy."""
        reply = Reply(content="test", referenced_sources=["src001"])
        sources = reply.referenced_sources
        sources.append("src002")
        assert len(reply.referenced_sources) == 1  # Original data unaffected


class TestReplyTimestamp:
    """Timestamp tests."""

    def test_has_timestamp(self):
        """Test that a reply has a timestamp."""
        reply = Reply(content="test")
        assert reply.timestamp is not None

    def test_timestamp_is_datetime(self):
        """Test that the timestamp is a datetime object."""
        from datetime import datetime
        reply = Reply(content="test")
        assert isinstance(reply.timestamp, datetime)


class TestReplyToDict:
    """to_dict tests."""

    def test_to_dict(self):
        """Test conversion to dictionary."""
        reply = Reply(
            content="Reply content",
            is_auto=True,
            email_id="e001",
            referenced_sources=["src001"],
        )
        reply.id = "r001"
        d = reply.to_dict()
        assert d["id"] == "r001"
        assert d["content"] == "Reply content"
        assert d["is_auto"] is True
        assert d["approved"] is False
        assert d["email_id"] == "e001"
        assert d["referenced_sources"] == ["src001"]
        assert "timestamp" in d

    def test_to_dict_with_none_id(self):
        """Test to_dict for an unsaved reply."""
        reply = Reply(content="test")
        d = reply.to_dict()
        assert d["id"] is None


class TestReplyRepr:
    """__repr__ tests."""

    def test_repr(self):
        """Test string representation."""
        reply = Reply(content="test")
        reply.id = "r001"
        r = repr(reply)
        assert "r001" in r
        assert "auto=True" in r
