"""Optimized query builders with prepared statements"""
import asyncpg
from typing import Optional, List, Dict, Any, Union
from app.utils.normalization import (
    normalize_domain,
    normalize_linkedin_url,
    normalize_email,
    normalize_place_id,
    normalize_google_id,
    extract_domain_from_email,
)


class QueryBuilder:
    """Query builder for Outscraper business lookups"""
    
    # Base SELECT clause with all 111 columns
    BASE_SELECT = """
        SELECT 
            id, query, name, name_for_emails, site, subtypes, category, type,
            phone, phone_1, phone_2, phone_3,
            full_address, borough, street, city, postal_code, state, us_state, country, country_code,
            latitude, longitude, h3, time_zone, plus_code, area_service,
            rating, reviews, reviews_link, reviews_tags, reviews_per_score,
            reviews_per_score_1, reviews_per_score_2, reviews_per_score_3, reviews_per_score_4, reviews_per_score_5, reviews_id,
            photos_count, photo, street_view, logo,
            located_in, working_hours, working_hours_csv_compatible, working_hours_old_format, other_hours, popular_times,
            business_status, about, range, prices, posts, description, typical_time_spent, verified,
            owner_id, owner_title, owner_link,
            reservation_links, booking_appointment_link, menu_link, order_links,
            location_link, location_reviews_link, place_id, google_id, cid, kgmid, located_google_id,
            email_1, email_1_full_name, email_1_first_name, email_1_last_name, email_1_title, email_1_phone,
            email_2, email_2_full_name, email_2_first_name, email_2_last_name, email_2_title, email_2_phone,
            email_3, email_3_full_name, email_3_first_name, email_3_last_name, email_3_title, email_3_phone,
            facebook, instagram, linkedin, tiktok, medium, reddit, skype, snapchat, telegram, whatsapp, twitter, vimeo, youtube, github, crunchbase,
            website_title, website_generator, website_description, website_keywords, website_has_fb_pixel, website_has_google_tag,
            source_file, import_date
        FROM businesses
    """
    
    @staticmethod
    async def prepare_statements(conn: asyncpg.Connection):
        """Prepare all statements for better performance"""
        statements = {}
        
        # By domain
        statements['by_domain'] = await conn.prepare(
            QueryBuilder.BASE_SELECT + " WHERE site ILIKE $1 OR site ILIKE $2 LIMIT 100"
        )
        
        # By LinkedIn
        statements['by_linkedin'] = await conn.prepare(
            QueryBuilder.BASE_SELECT + " WHERE linkedin ILIKE $1 LIMIT 100"
        )
        
        # By Place ID
        statements['by_place_id'] = await conn.prepare(
            QueryBuilder.BASE_SELECT + " WHERE place_id = $1 LIMIT 1"
        )
        
        # By email
        statements['by_email'] = await conn.prepare(
            QueryBuilder.BASE_SELECT + " WHERE email_1 = $1 OR email_2 = $1 OR email_3 = $1 LIMIT 100"
        )
        
        # By Google ID
        statements['by_google_id'] = await conn.prepare(
            QueryBuilder.BASE_SELECT + " WHERE google_id = $1 OR cid = $1 OR kgmid = $1 LIMIT 100"
        )
        
        # Batch by emails
        statements['batch_by_emails'] = await conn.prepare(
            QueryBuilder.BASE_SELECT + " WHERE email_1 = ANY($1::text[]) OR email_2 = ANY($1::text[]) OR email_3 = ANY($1::text[]) LIMIT 1000"
        )
        
        # Enriched contacts (with email and other contact info)
        statements['enriched_contacts'] = await conn.prepare(
            QueryBuilder.BASE_SELECT + " WHERE email_1 IS NOT NULL ORDER BY id LIMIT $1 OFFSET $2"
        )
        
        return statements
    
    @staticmethod
    async def by_domain(
        conn: asyncpg.Connection,
        domain: str,
        use_prepared: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """Query businesses by domain"""
        normalized_domain = normalize_domain(domain)
        if not normalized_domain:
            return []
        
        # Try exact match first, then pattern match
        domain_pattern = f"%{normalized_domain}%"
        domain_exact = f"%//{normalized_domain}%"
        
        if use_prepared:
            rows = await use_prepared.fetch(domain_exact, domain_pattern)
        else:
            query = QueryBuilder.BASE_SELECT + " WHERE site ILIKE $1 OR site ILIKE $2 LIMIT 100"
            rows = await conn.fetch(query, domain_exact, domain_pattern)
        
        return [dict(row) for row in rows] if rows else []
    
    @staticmethod
    async def by_linkedin(
        conn: asyncpg.Connection,
        linkedin: str,
        use_prepared: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """Query businesses by LinkedIn URL"""
        normalized_linkedin = normalize_linkedin_url(linkedin)
        if not normalized_linkedin:
            return []
        
        linkedin_pattern = f"%{normalized_linkedin}%"
        
        if use_prepared:
            rows = await use_prepared.fetch(linkedin_pattern)
        else:
            query = QueryBuilder.BASE_SELECT + " WHERE linkedin ILIKE $1 LIMIT 100"
            rows = await conn.fetch(query, linkedin_pattern)
        
        return [dict(row) for row in rows] if rows else []
    
    @staticmethod
    async def by_place_id(
        conn: asyncpg.Connection,
        place_id: str,
        use_prepared: Optional[Any] = None
    ) -> Optional[Dict[str, Any]]:
        """Query business by Place ID"""
        normalized_place_id = normalize_place_id(place_id)
        if not normalized_place_id:
            return None
        
        if use_prepared:
            row = await use_prepared.fetchrow(normalized_place_id)
        else:
            query = QueryBuilder.BASE_SELECT + " WHERE place_id = $1 LIMIT 1"
            row = await conn.fetchrow(query, normalized_place_id)
        
        return dict(row) if row else None
    
    @staticmethod
    async def by_email(
        conn: asyncpg.Connection,
        email: str,
        use_prepared: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """Query businesses by email"""
        normalized_email = normalize_email(email)
        if not normalized_email:
            return []
        
        if use_prepared:
            rows = await use_prepared.fetch(normalized_email)
        else:
            query = QueryBuilder.BASE_SELECT + " WHERE email_1 = $1 OR email_2 = $1 OR email_3 = $1 LIMIT 100"
            rows = await conn.fetch(query, normalized_email)
        
        return [dict(row) for row in rows] if rows else []
    
    @staticmethod
    async def by_google_id(
        conn: asyncpg.Connection,
        google_id: str,
        use_prepared: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """Query businesses by Google ID"""
        normalized_google_id = normalize_google_id(google_id)
        if not normalized_google_id:
            return []
        
        if use_prepared:
            rows = await use_prepared.fetch(normalized_google_id)
        else:
            query = QueryBuilder.BASE_SELECT + " WHERE google_id = $1 OR cid = $1 OR kgmid = $1 LIMIT 100"
            rows = await conn.fetch(query, normalized_google_id)
        
        return [dict(row) for row in rows] if rows else []
    
    @staticmethod
    async def batch_by_emails(
        conn: asyncpg.Connection,
        emails: List[str],
        use_prepared: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """Query businesses by multiple emails"""
        normalized_emails = [normalize_email(e) for e in emails if normalize_email(e)]
        if not normalized_emails:
            return []
        
        if use_prepared:
            rows = await use_prepared.fetch(normalized_emails)
        else:
            query = QueryBuilder.BASE_SELECT + " WHERE email_1 = ANY($1::text[]) OR email_2 = ANY($1::text[]) OR email_3 = ANY($1::text[]) LIMIT 1000"
            rows = await conn.fetch(query, normalized_emails)
        
        return [dict(row) for row in rows] if rows else []
    
    @staticmethod
    async def enriched_contacts(
        conn: asyncpg.Connection,
        limit: int = 100,
        offset: int = 0,
        use_prepared: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """Query businesses with enriched contact information"""
        if use_prepared:
            rows = await use_prepared.fetch(limit, offset)
        else:
            query = QueryBuilder.BASE_SELECT + " WHERE email_1 IS NOT NULL ORDER BY id LIMIT $1 OFFSET $2"
            rows = await conn.fetch(query, limit, offset)
        
        return [dict(row) for row in rows] if rows else []
