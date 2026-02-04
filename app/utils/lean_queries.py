"""Optimized SQL queries for lean endpoints"""
import asyncpg
from typing import List, Dict, Any, Optional

from app.utils.normalization import normalize_domain


class LeanQueryBuilder:
    """
    Optimized query builder for Clay integration.
    Uses custom SELECT queries to fetch only needed columns.
    """

    # Email-only query (13 columns = 88% reduction)
    EMAILS_ONLY_QUERY = """
        SELECT
            id, name, site,
            email_1, email_1_full_name, email_1_title, email_1_phone,
            email_2, email_2_full_name, email_2_title, email_2_phone,
            email_3, email_3_full_name, email_3_title, email_3_phone
        FROM businesses
        WHERE (site ILIKE $1 OR site ILIKE $2)
          AND (email_1 IS NOT NULL AND email_1 <> ''
             OR email_2 IS NOT NULL AND email_2 <> ''
             OR email_3 IS NOT NULL AND email_3 <> '')
        LIMIT 100
    """

    # Contact info query (~25 columns = 77% reduction)
    CONTACT_INFO_QUERY = """
        SELECT
            id, name, site, category,
            phone, phone_1, phone_2, phone_3,
            city, state, full_address,
            email_1, email_1_full_name, email_1_title, email_1_phone,
            email_2, email_2_full_name, email_2_title, email_2_phone,
            email_3, email_3_full_name, email_3_title, email_3_phone
        FROM businesses
        WHERE site ILIKE $1 OR site ILIKE $2
        LIMIT 100
    """

    # Full profile query (~40 columns = 64% reduction)
    FULL_PROFILE_QUERY = """
        SELECT
            id, name, name_for_emails, site, category, type,
            phone, phone_1, phone_2, phone_3,
            full_address, city, state, postal_code,
            description, rating, reviews,
            linkedin, facebook, instagram, twitter,
            email_1, email_1_full_name, email_1_title, email_1_phone,
            email_2, email_2_full_name, email_2_title, email_2_phone,
            email_3, email_3_full_name, email_3_title, email_3_phone
        FROM businesses
        WHERE site ILIKE $1 OR site ILIKE $2
        LIMIT 100
    """

    @staticmethod
    async def by_domain_emails_only(
        conn: asyncpg.Connection,
        domain: str
    ) -> List[Dict[str, Any]]:
        """
        Query businesses by domain - email-only fields (13 columns).

        Args:
            conn: Database connection
            domain: Domain to search for

        Returns:
            List of business dictionaries with email fields only
        """
        normalized_domain = normalize_domain(domain)
        if not normalized_domain:
            return []

        # Try exact match first, then pattern match
        domain_pattern = f"%{normalized_domain}%"
        domain_exact = f"%//{normalized_domain}%"

        rows = await conn.fetch(
            LeanQueryBuilder.EMAILS_ONLY_QUERY,
            domain_exact,
            domain_pattern
        )

        return [dict(row) for row in rows] if rows else []

    @staticmethod
    async def by_domain_contact_info(
        conn: asyncpg.Connection,
        domain: str
    ) -> List[Dict[str, Any]]:
        """
        Query businesses by domain - contact info fields (~25 columns).

        Args:
            conn: Database connection
            domain: Domain to search for

        Returns:
            List of business dictionaries with contact info
        """
        normalized_domain = normalize_domain(domain)
        if not normalized_domain:
            return []

        domain_pattern = f"%{normalized_domain}%"
        domain_exact = f"%//{normalized_domain}%"

        rows = await conn.fetch(
            LeanQueryBuilder.CONTACT_INFO_QUERY,
            domain_exact,
            domain_pattern
        )

        return [dict(row) for row in rows] if rows else []

    @staticmethod
    async def by_domain_full_profile(
        conn: asyncpg.Connection,
        domain: str
    ) -> List[Dict[str, Any]]:
        """
        Query businesses by domain - full profile fields (~40 columns).

        Args:
            conn: Database connection
            domain: Domain to search for

        Returns:
            List of business dictionaries with full profile
        """
        normalized_domain = normalize_domain(domain)
        if not normalized_domain:
            return []

        domain_pattern = f"%{normalized_domain}%"
        domain_exact = f"%//{normalized_domain}%"

        rows = await conn.fetch(
            LeanQueryBuilder.FULL_PROFILE_QUERY,
            domain_exact,
            domain_pattern
        )

        return [dict(row) for row in rows] if rows else []
