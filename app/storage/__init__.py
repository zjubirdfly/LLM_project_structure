from .simple_cache import SimpleCacheManager

# Export the current cache manager as the default
cache_manager = SimpleCacheManager()

# Future storage backends can be added here
# from .redis_cache import RedisCacheManager
# from .database_manager import DatabaseManager

__all__ = [
    "cache_manager",
]
