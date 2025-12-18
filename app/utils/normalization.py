"""Normalization utilities for domain, LinkedIn, and email parsing"""
import re
from typing import Optional
from urllib.parse import urlparse, urlunparse
import logging

logger = logging.getLogger(__name__)


def normalize_domain(domain: str) -> Optional[str]:
    """
    Normalize a domain string to a clean domain format.
    
    Examples:
        "https://www.example.com/path" -> "example.com"
        "www.example.com" -> "example.com"
        "example.com" -> "example.com"
        "subdomain.example.com" -> "subdomain.example.com"
    
    Args:
        domain: Domain string that may include protocol, path, etc.
    
    Returns:
        Normalized domain string or None if invalid
    """
    if not domain or not isinstance(domain, str):
        return None
    
    domain = domain.strip()
    if not domain:
        return None
    
    # Remove protocol if present
    if "://" in domain:
        try:
            parsed = urlparse(domain)
            domain = parsed.netloc or parsed.path
        except Exception as e:
            logger.warning(f"Failed to parse URL {domain}: {e}")
            return None
    
    # Remove port if present
    if ":" in domain:
        domain = domain.split(":")[0]
    
    # Remove path if present
    if "/" in domain:
        domain = domain.split("/")[0]
    
    # Remove www. prefix (optional, but common)
    domain = re.sub(r'^www\.', '', domain, flags=re.IGNORECASE)
    
    # Remove trailing dots
    domain = domain.rstrip('.')
    
    # Basic validation - should contain at least one dot
    if '.' not in domain:
        return None
    
    # Remove spaces and convert to lowercase
    domain = domain.lower().strip()
    
    # Validate domain format (basic check)
    if not re.match(r'^[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?)*$', domain):
        return None
    
    return domain


def extract_domain_from_url(url: str) -> Optional[str]:
    """
    Extract domain from a full URL.
    
    Args:
        url: Full URL string
    
    Returns:
        Normalized domain or None
    """
    return normalize_domain(url)


def normalize_linkedin_url(linkedin: str) -> Optional[str]:
    """
    Normalize a LinkedIn URL to a standard format.
    
    Examples:
        "https://www.linkedin.com/company/example" -> "linkedin.com/company/example"
        "linkedin.com/in/john-doe" -> "linkedin.com/in/john-doe"
        "www.linkedin.com/company/example/" -> "linkedin.com/company/example"
    
    Args:
        linkedin: LinkedIn URL string
    
    Returns:
        Normalized LinkedIn URL path or None if invalid
    """
    if not linkedin or not isinstance(linkedin, str):
        return None
    
    linkedin = linkedin.strip()
    if not linkedin:
        return None
    
    # Remove protocol
    if "://" in linkedin:
        try:
            parsed = urlparse(linkedin)
            linkedin = parsed.netloc + parsed.path
        except Exception:
            return None
    
    # Remove www. prefix
    linkedin = re.sub(r'^www\.', '', linkedin, flags=re.IGNORECASE)
    
    # Ensure it starts with linkedin.com
    if not linkedin.lower().startswith('linkedin.com'):
        return None
    
    # Remove trailing slashes
    linkedin = linkedin.rstrip('/')
    
    # Convert to lowercase
    linkedin = linkedin.lower()
    
    return linkedin


def normalize_email(email: str) -> Optional[str]:
    """
    Normalize an email address.
    
    Examples:
        "John.Doe@Example.COM" -> "john.doe@example.com"
        " john@example.com " -> "john@example.com"
    
    Args:
        email: Email address string
    
    Returns:
        Normalized email address or None if invalid
    """
    if not email or not isinstance(email, str):
        return None
    
    email = email.strip()
    if not email:
        return None
    
    # Convert to lowercase
    email = email.lower()
    
    # Basic email validation
    email_pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    if not re.match(email_pattern, email):
        return None
    
    return email


def normalize_place_id(place_id: str) -> Optional[str]:
    """
    Normalize a Google Place ID.
    
    Args:
        place_id: Google Place ID string
    
    Returns:
        Normalized Place ID or None if invalid
    """
    if not place_id or not isinstance(place_id, str):
        return None
    
    place_id = place_id.strip()
    if not place_id:
        return None
    
    return place_id


def normalize_google_id(google_id: str) -> Optional[str]:
    """
    Normalize a Google ID.
    
    Args:
        google_id: Google ID string
    
    Returns:
        Normalized Google ID or None if invalid
    """
    if not google_id or not isinstance(google_id, str):
        return None
    
    google_id = google_id.strip()
    if not google_id:
        return None
    
    return google_id


def extract_domain_from_email(email: str) -> Optional[str]:
    """
    Extract domain from an email address.
    
    Args:
        email: Email address
    
    Returns:
        Domain string or None
    """
    normalized_email = normalize_email(email)
    if not normalized_email:
        return None
    
    return normalized_email.split('@')[1]
