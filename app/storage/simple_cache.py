from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import threading
from app.log_utils import Logger
import json


class SimpleCacheManager:
    """Simple in-memory cache manager using dictionary storage."""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()  # Thread safety
        self._default_ttl = 3600  # 1 hour default TTL

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from cache if not expired."""
        with self._lock:
            if key not in self._cache:
                return None

            cache_entry = self._cache[key]
            expires_at = cache_entry.get("expires_at")

            # Check if expired
            if expires_at and datetime.utcnow() > expires_at:
                del self._cache[key]
                Logger.log_session(
                    session_id=key,
                    message=f"Cache entry expired for key: {key}",
                    level="DEBUG",
                )
                return None
            Logger.log_session(
                session_id=key,
                message=f"Cache hit for key: {key}, data: {json.dumps(cache_entry, default=str)}",
                level="DEBUG",
            )

            return cache_entry.get("data")

    def set(self, key: str, data: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """Set value in cache with TTL."""
        try:
            ttl = ttl or self._default_ttl
            expires_at = datetime.utcnow() + timedelta(seconds=ttl)

            with self._lock:
                self._cache[key] = {
                    "data": data,
                    "expires_at": expires_at,
                    "created_at": datetime.utcnow(),
                    "last_accessed": datetime.utcnow(),
                }
            Logger.log_session(
                session_id=key,
                message=f"Cache set for key: {key} success, data: {json.dumps(data, default=str)}, expires_at: {expires_at}",
                level="DEBUG",
            )

            return True

        except Exception as e:
            Logger.log_session(
                session_id=key,
                message=f"Cache set for key: {key} failed, error: {str(e)}",
                level="ERROR",
            )
            return False

    def update(self, key: str, updates: Dict[str, Any]) -> bool:
        """Update specific fields in cached data."""
        current_data = self.get(key) or {}
        current_data.update(updates)
        Logger.log_session(
            session_id=key,
            message=f"Updating cache for key: {key}, updates: {json.dumps(updates, default=str)}",
            level="DEBUG",
        )
        return self.set(key, current_data)

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            with self._lock:
                if key in self._cache:
                    del self._cache[key]
                    Logger.log_session(
                        session_id=key,
                        message=f"Cache entry deleted for key: {key}",
                        level="DEBUG",
                    )
                    return True
                return False

        except Exception as e:
            Logger.log_session(
                session_id=key,
                message=f"Cache delete for key: {key} failed, error: {str(e)}",
                level="ERROR",
            )
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists and is not expired."""
        return self.get(key) is not None

    def get_all_keys(self) -> list:
        """Get all non-expired keys."""
        with self._lock:
            valid_keys = []
            for key in list(self._cache.keys()):
                if self.exists(key):
                    valid_keys.append(key)
            return valid_keys

    def clear_expired(self) -> int:
        """Clear expired entries and return count of cleared items."""
        cleared_count = 0
        with self._lock:
            for key in list(self._cache.keys()):
                if not self.exists(key):
                    cleared_count += 1
        return cleared_count

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_entries = len(self._cache)
            valid_entries = len([k for k in self._cache.keys() if self.exists(k)])

            return {
                "total_entries": total_entries,
                "valid_entries": valid_entries,
                "expired_entries": total_entries - valid_entries,
                "cache_size": len(self._cache),
            }
