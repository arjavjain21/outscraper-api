"""Authentication middleware for API endpoints"""
from fastapi import HTTPException, status, Header
import logging

from app.config import settings

logger = logging.getLogger(__name__)


async def verify_api_key(
    authorization: str = Header(None, convert_underscores=False)
) -> bool:
    """
    Verify Bearer token for API requests.

    Args:
        authorization: Authorization header value

    Returns:
        bool: True if authenticated

    Raises:
        HTTPException: If authentication fails (401 Unauthorized)
    """
    # If auth is disabled (for development/testing), allow all requests
    if not settings.OUTSCRAPER_API_ENABLED:
        logger.debug("API authentication is disabled")
        return True

    # Check if authorization header is present
    if not authorization:
        logger.warning("Missing Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "authentication_required",
                "message": "Invalid or missing API key",
                "status": 401
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract Bearer token
    if not authorization.startswith("Bearer "):
        logger.warning("Invalid Authorization header format (missing 'Bearer')")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "authentication_required",
                "message": "Invalid authorization header format",
                "status": 401
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]  # Remove "Bearer " prefix

    # Verify API key
    if token != settings.OUTSCRAPER_API_KEY:
        # Log only prefix for security (don't log full key)
        key_preview = token[:10] if token else "None"
        logger.warning(f"Failed authentication attempt with key: {key_preview}...")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "authentication_required",
                "message": "Invalid or missing API key",
                "status": 401
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Log successful authentication (only prefix)
    key_preview = token[:10]
    logger.info(f"Successful authentication with key: {key_preview}...")
    return True
