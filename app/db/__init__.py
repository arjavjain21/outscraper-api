"""Database connection and pool management"""
import asyncpg
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_pool() -> asyncpg.Pool:
    """Get or create database connection pool"""
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            host=settings.DATABASE_HOST,
            port=settings.DATABASE_PORT,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            database=settings.DATABASE_NAME,
            min_size=settings.DB_POOL_MIN_SIZE,
            max_size=settings.DB_POOL_MAX_SIZE,
            max_queries=settings.DB_POOL_MAX_QUERIES,
            max_inactive_connection_lifetime=settings.DB_POOL_MAX_INACTIVE_TIME,
            command_timeout=60,
        )
        logger.info(f"Database connection pool created: {settings.DB_POOL_MIN_SIZE}-{settings.DB_POOL_MAX_SIZE} connections")
    return _pool


async def close_pool():
    """Close database connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


async def get_connection():
    """Get a connection from the pool"""
    pool = await get_pool()
    return await pool.acquire()


async def release_connection(conn):
    """Release a connection back to the pool"""
    pool = await get_pool()
    await pool.release(conn)
