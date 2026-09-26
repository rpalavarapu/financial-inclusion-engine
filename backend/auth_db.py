import json
import os
import hashlib
import uuid
from pathlib import Path
from typing import Dict, Any, Optional

# File path for JSON Database
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = ROOT_DIR / "data" / "users.json"

class UserJSONDatabase:
    """
    JSON File Database for managing user credentials with salted SHA-256 password hashing.
    """
    def __init__(self, db_path: Path = DB_FILE):
        self.db_path = db_path
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Ensures data directory and users.json file exist with default demo account."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._write_db({"users": {}})
            # Seed default demo account
            self.register_user("underwriter_demo", "ab@mail.com", "secure123")

    def _read_db(self) -> Dict[str, Any]:
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"users": {}}

    def _write_db(self, data: Dict[str, Any]):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        """Computes salted SHA-256 password hash."""
        salted = f"{salt}:{password}".encode("utf-8")
        return hashlib.sha256(salted).hexdigest()

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        db = self._read_db()
        return db["users"].get(username.lower())

    def register_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Registers a new user and saves salted password hash to JSON DB."""
        username_clean = username.strip().lower()
        db = self._read_db()

        if username_clean in db["users"]:
            raise ValueError(f"Username '{username}' is already registered.")

        # Check email uniqueness
        for user_rec in db["users"].values():
            if user_rec.get("email", "").lower() == email.strip().lower():
                raise ValueError(f"Email '{email}' is already registered.")

        salt = uuid.uuid4().hex
        password_hash = self._hash_password(password, salt)

        user_record = {
            "id": str(uuid.uuid4()),
            "username": username_clean,
            "email": email.strip().lower(),
            "salt": salt,
            "password_hash": password_hash,
            "created_at": str(Path(__file__).stat().st_mtime)
        }

        db["users"][username_clean] = user_record
        self._write_db(db)

        return {
            "id": user_record["id"],
            "username": user_record["username"],
            "email": user_record["email"]
        }

    def verify_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Verifies username and password against JSON database."""
        user_record = self.get_user(username)
        if not user_record:
            return None

        salt = user_record["salt"]
        expected_hash = user_record["password_hash"]
        computed_hash = self._hash_password(password, salt)

        if computed_hash == expected_hash:
            return {
                "id": user_record["id"],
                "username": user_record["username"],
                "email": user_record["email"]
            }

        return None

# Singleton DB instance
user_db = UserJSONDatabase()
