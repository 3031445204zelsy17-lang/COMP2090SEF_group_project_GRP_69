"""SQLite Database Client

Local file-based database client for offline demo mode.
Implements the same DatabaseClient interface as SupabaseClient,
demonstrating OOP Polymorphism — same interface, different backend.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any

import aiosqlite

from .base import DatabaseClient


class SqliteClient(DatabaseClient):
    """SQLite database client for offline demo mode.

    Implements all DatabaseClient methods using a local SQLite file.
    Generates UUIDs to match Supabase's auto-generated ID behavior.
    Stores list fields (keywords, referenced_sources) as JSON strings.
    """

    def __init__(self, db_path: str):
        """Initialize with the path to the SQLite database file.

        Args:
            db_path: Path to the .db file (created automatically on first use).
        """
        self._db_path = db_path

    async def init_db(self) -> None:
        """Create all required tables if they do not exist.

        Called once by run_demo.py before seeding data.
        """
        async with aiosqlite.connect(self._db_path) as db:
            await db.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    role TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now'))
                );

                CREATE TABLE IF NOT EXISTS categories (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    priority INTEGER DEFAULT 5,
                    keywords TEXT DEFAULT '[]'
                );

                CREATE TABLE IF NOT EXISTS knowledge_sources (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    keywords TEXT DEFAULT '[]',
                    category TEXT,
                    created_by TEXT,
                    created_at TEXT DEFAULT (datetime('now')),
                    updated_at TEXT DEFAULT (datetime('now'))
                );

                CREATE TABLE IF NOT EXISTS emails (
                    id TEXT PRIMARY KEY,
                    subject TEXT NOT NULL,
                    body TEXT NOT NULL,
                    sender_email TEXT NOT NULL,
                    sender_name TEXT,
                    category_id TEXT,
                    status TEXT DEFAULT 'pending',
                    is_duplicate INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now'))
                );

                CREATE TABLE IF NOT EXISTS replies (
                    id TEXT PRIMARY KEY,
                    email_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    is_auto INTEGER DEFAULT 1,
                    is_approved INTEGER DEFAULT 0,
                    referenced_sources TEXT DEFAULT '[]',
                    created_at TEXT DEFAULT (datetime('now'))
                );
            """)
            await db.commit()

    # ==================== User Operations ====================

    async def create_user(
        self,
        name: str,
        email: str,
        role: str,
        password_hash: str,
    ) -> Dict[str, Any]:
        user_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT INTO users (id, name, email, role, password_hash, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, name, email, role, password_hash, now),
            )
            await db.commit()
        return {
            "id": user_id,
            "name": name,
            "email": email,
            "role": role,
            "password_hash": password_hash,
            "created_at": now,
        }

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    # ==================== Category Operations ====================

    async def get_categories(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM categories ORDER BY priority")
            rows = await cursor.fetchall()
            return [self._parse_category(dict(r)) for r in rows]

    async def create_category(
        self,
        name: str,
        priority: int,
        keywords: List[str],
    ) -> Dict[str, Any]:
        cat_id = str(uuid.uuid4())
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT INTO categories (id, name, priority, keywords) VALUES (?, ?, ?, ?)",
                (cat_id, name, priority, json.dumps(keywords)),
            )
            await db.commit()
        return {
            "id": cat_id,
            "name": name,
            "priority": priority,
            "keywords": keywords,
        }

    # ==================== Knowledge Source Operations ====================

    async def get_knowledge_sources(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM knowledge_sources ORDER BY created_at DESC")
            rows = await cursor.fetchall()
            return [self._parse_knowledge_source(dict(r)) for r in rows]

    async def get_knowledge_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM knowledge_sources WHERE id = ?", (source_id,))
            row = await cursor.fetchone()
            return self._parse_knowledge_source(dict(row)) if row else None

    async def create_knowledge_source(
        self,
        title: str,
        content: str,
        keywords: List[str],
        category: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        source_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT INTO knowledge_sources (id, title, content, keywords, category, created_by, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (source_id, title, content, json.dumps(keywords), category, created_by, now, now),
            )
            await db.commit()
        return {
            "id": source_id,
            "title": title,
            "content": content,
            "keywords": keywords,
            "category": category,
            "created_by": created_by,
            "created_at": now,
            "updated_at": now,
        }

    async def update_knowledge_source(
        self,
        source_id: str,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        kwargs["updated_at"] = datetime.now().isoformat()
        if "keywords" in kwargs and isinstance(kwargs["keywords"], list):
            kwargs["keywords"] = json.dumps(kwargs["keywords"])

        set_clauses = [f"{k} = ?" for k in kwargs]
        values = list(kwargs.values()) + [source_id]

        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                f"UPDATE knowledge_sources SET {', '.join(set_clauses)} WHERE id = ?",
                values,
            )
            await db.commit()
        return await self.get_knowledge_source(source_id)

    async def delete_knowledge_source(self, source_id: str) -> bool:
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute("DELETE FROM knowledge_sources WHERE id = ?", (source_id,))
            await db.commit()
            return cursor.rowcount > 0

    # ==================== Email Operations ====================

    async def get_emails(
        self,
        status: Optional[str] = None,
        category_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        query = """
            SELECT e.id, e.subject, e.body, e.sender_email, e.sender_name,
                   e.category_id, e.status, e.is_duplicate, e.created_at,
                   c.id as cat_id, c.name as cat_name,
                   c.priority as cat_priority, c.keywords as cat_keywords
            FROM emails e
            LEFT JOIN categories c ON e.category_id = c.id
            WHERE 1=1
        """
        params: list = []

        if status:
            query += " AND e.status = ?"
            params.append(status)
        if category_id:
            query += " AND e.category_id = ?"
            params.append(category_id)

        query += " ORDER BY e.created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(query, params)
            rows = await cursor.fetchall()
            return [self._parse_email_with_category(dict(r)) for r in rows]

    async def get_email(self, email_id: str) -> Optional[Dict[str, Any]]:
        query = """
            SELECT e.id, e.subject, e.body, e.sender_email, e.sender_name,
                   e.category_id, e.status, e.is_duplicate, e.created_at,
                   c.id as cat_id, c.name as cat_name,
                   c.priority as cat_priority, c.keywords as cat_keywords
            FROM emails e
            LEFT JOIN categories c ON e.category_id = c.id
            WHERE e.id = ?
        """
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(query, (email_id,))
            row = await cursor.fetchone()
            return self._parse_email_with_category(dict(row)) if row else None

    async def create_email(
        self,
        subject: str,
        body: str,
        sender_email: str,
        sender_name: Optional[str] = None,
        category_id: Optional[str] = None,
        is_duplicate: bool = False,
    ) -> Dict[str, Any]:
        email_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT INTO emails (id, subject, body, sender_email, sender_name, category_id, status, is_duplicate, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (email_id, subject, body, sender_email, sender_name, category_id, "pending", int(is_duplicate), now),
            )
            await db.commit()

        # Return with joined category data if category_id is set
        if category_id:
            return await self.get_email(email_id)
        return {
            "id": email_id,
            "subject": subject,
            "body": body,
            "sender_email": sender_email,
            "sender_name": sender_name,
            "category_id": category_id,
            "status": "pending",
            "is_duplicate": is_duplicate,
            "created_at": now,
            "categories": None,
        }

    async def update_email(
        self,
        email_id: str,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        if "is_duplicate" in kwargs and isinstance(kwargs["is_duplicate"], bool):
            kwargs["is_duplicate"] = int(kwargs["is_duplicate"])

        set_clauses = [f"{k} = ?" for k in kwargs]
        values = list(kwargs.values()) + [email_id]

        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                f"UPDATE emails SET {', '.join(set_clauses)} WHERE id = ?",
                values,
            )
            await db.commit()
        return await self.get_email(email_id)

    async def count_emails(self, status: Optional[str] = None) -> int:
        query = "SELECT COUNT(*) FROM emails"
        params: list = []
        if status:
            query += " WHERE status = ?"
            params.append(status)

        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute(query, params)
            row = await cursor.fetchone()
            return row[0] if row else 0

    # ==================== Reply Operations ====================

    async def get_reply_by_id(self, reply_id: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM replies WHERE id = ?", (reply_id,))
            row = await cursor.fetchone()
            return self._parse_reply(dict(row)) if row else None

    async def get_reply_by_email(self, email_id: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM replies WHERE email_id = ?", (email_id,))
            row = await cursor.fetchone()
            return self._parse_reply(dict(row)) if row else None

    async def create_reply(
        self,
        email_id: str,
        content: str,
        is_auto: bool = True,
        referenced_sources: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        reply_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                "INSERT INTO replies (id, email_id, content, is_auto, is_approved, referenced_sources, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (reply_id, email_id, content, int(is_auto), 0, json.dumps(referenced_sources or []), now),
            )
            await db.commit()
        return {
            "id": reply_id,
            "email_id": email_id,
            "content": content,
            "is_auto": is_auto,
            "is_approved": False,
            "referenced_sources": referenced_sources or [],
            "created_at": now,
        }

    async def update_reply(
        self,
        reply_id: str,
        **kwargs,
    ) -> Optional[Dict[str, Any]]:
        if "is_auto" in kwargs and isinstance(kwargs["is_auto"], bool):
            kwargs["is_auto"] = int(kwargs["is_auto"])
        if "is_approved" in kwargs and isinstance(kwargs["is_approved"], bool):
            kwargs["is_approved"] = int(kwargs["is_approved"])
        if "referenced_sources" in kwargs and isinstance(kwargs["referenced_sources"], list):
            kwargs["referenced_sources"] = json.dumps(kwargs["referenced_sources"])

        set_clauses = [f"{k} = ?" for k in kwargs]
        values = list(kwargs.values()) + [reply_id]

        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                f"UPDATE replies SET {', '.join(set_clauses)} WHERE id = ?",
                values,
            )
            await db.commit()
        return await self.get_reply_by_id(reply_id)

    async def approve_reply(self, reply_id: str) -> bool:
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute(
                "UPDATE replies SET is_approved = 1 WHERE id = ?",
                (reply_id,),
            )
            await db.commit()
            return cursor.rowcount > 0

    async def delete_reply(self, reply_id: str) -> bool:
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute("DELETE FROM replies WHERE id = ?", (reply_id,))
            await db.commit()
            return cursor.rowcount > 0

    # ==================== Statistics Operations ====================

    async def get_stats(self) -> Dict[str, Any]:
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row

            # Email counts by status
            cursor = await db.execute("SELECT status FROM emails")
            email_rows = await cursor.fetchall()
            status_counts: Dict[str, int] = {}
            for row in email_rows:
                s = row["status"]
                status_counts[s] = status_counts.get(s, 0) + 1

            # Reply statistics
            cursor = await db.execute("SELECT is_auto, is_approved FROM replies")
            reply_rows = await cursor.fetchall()
            auto_replies = sum(1 for r in reply_rows if r["is_auto"])
            approved_replies = sum(1 for r in reply_rows if r["is_approved"])

            # Knowledge source count
            cursor = await db.execute("SELECT COUNT(*) FROM knowledge_sources")
            row = await cursor.fetchone()
            sources_count = row[0] if row else 0

            return {
                "total_emails": len(email_rows),
                "status_counts": status_counts,
                "auto_replies": auto_replies,
                "approved_replies": approved_replies,
                "knowledge_sources": sources_count,
            }

    # ==================== Private Helpers ====================

    @staticmethod
    def _parse_category(data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a category row, converting JSON keywords to list."""
        if isinstance(data.get("keywords"), str):
            data["keywords"] = json.loads(data["keywords"])
        return data

    @staticmethod
    def _parse_knowledge_source(data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a knowledge source row, converting JSON keywords to list."""
        if isinstance(data.get("keywords"), str):
            data["keywords"] = json.loads(data["keywords"])
        return data

    @staticmethod
    def _parse_email_with_category(data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse an email row with joined category data.

        Reconstructs the nested 'categories' dict to match Supabase's
        select('*, categories(*)') format expected by EmailFactory.from_dict().
        """
        # Extract category columns from the JOIN result
        cat_id = data.pop("cat_id", None)
        cat_name = data.pop("cat_name", None)
        cat_priority = data.pop("cat_priority", None)
        cat_keywords = data.pop("cat_keywords", None)

        # Build nested categories dict (matching Supabase join format)
        if cat_id:
            keywords = json.loads(cat_keywords) if cat_keywords else []
            data["categories"] = {
                "id": cat_id,
                "name": cat_name,
                "priority": cat_priority,
                "keywords": keywords,
            }
        else:
            data["categories"] = None

        # Convert boolean fields
        data["is_duplicate"] = bool(data.get("is_duplicate", 0))

        return data

    @staticmethod
    def _parse_reply(data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a reply row, converting SQLite integers to Python booleans."""
        data["is_auto"] = bool(data.get("is_auto", 0))
        data["is_approved"] = bool(data.get("is_approved", 0))
        if isinstance(data.get("referenced_sources"), str):
            data["referenced_sources"] = json.loads(data["referenced_sources"])
        return data
