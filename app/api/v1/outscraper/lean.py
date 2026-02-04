"""Lean API endpoints for Clay integration"""
from fastapi import APIRouter, HTTPException, Query, Depends, Response
from typing import List
import asyncpg
import logging
from datetime import datetime

from app.models.business_lean import (
    EmailOnlyResponse,
    ContactInfoResponse,
    FullProfileResponse,
    LeanBusinessListResponse,
    ErrorResponse,
)
from app.api.middleware import verify_api_key
from app.db import get_pool
from app.utils.lean_queries import LeanQueryBuilder

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/business/domain", tags=["lean"])


async def get_db_connection():
    """Dependency to get database connection"""
    pool = await get_pool()
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)


@router.get("/emails-only")
async def get_emails_only_by_domain(
    domain: str = Query(..., description="Domain name to search for"),
    authenticated: bool = Depends(verify_api_key),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Get email-only data for businesses by domain.

    Returns only email fields that have values (excludes null/empty emails).
    Ideal for email validation and simple lookup use cases.

    **Data reduction:** 88% (13 vs 111 fields)
    **Dynamic response:** Only includes non-null email fields
    """
    try:
        businesses = await LeanQueryBuilder.by_domain_emails_only(conn, domain)

        # Filter to only include non-null email fields
        filtered_businesses = []
        for business in businesses:
            filtered = {
                "id": business["id"],
                "name": business["name"],
                "site": business["site"]
            }

            # Add email_1 fields if present
            if business.get("email_1"):
                filtered["email_1"] = business["email_1"]
                if business.get("email_1_full_name"):
                    filtered["email_1_full_name"] = business["email_1_full_name"]
                if business.get("email_1_title"):
                    filtered["email_1_title"] = business["email_1_title"]
                if business.get("email_1_phone"):
                    filtered["email_1_phone"] = business["email_1_phone"]

            # Add email_2 fields if present
            if business.get("email_2"):
                filtered["email_2"] = business["email_2"]
                if business.get("email_2_full_name"):
                    filtered["email_2_full_name"] = business["email_2_full_name"]
                if business.get("email_2_title"):
                    filtered["email_2_title"] = business["email_2_title"]
                if business.get("email_2_phone"):
                    filtered["email_2_phone"] = business["email_2_phone"]

            # Add email_3 fields if present
            if business.get("email_3"):
                filtered["email_3"] = business["email_3"]
                if business.get("email_3_full_name"):
                    filtered["email_3_full_name"] = business["email_3_full_name"]
                if business.get("email_3_title"):
                    filtered["email_3_title"] = business["email_3_title"]
                if business.get("email_3_phone"):
                    filtered["email_3_phone"] = business["email_3_phone"]

            filtered_businesses.append(filtered)

        return LeanBusinessListResponse(
            count=len(filtered_businesses),
            businesses=filtered_businesses,
            domain_query=domain,
            timestamp=datetime.utcnow()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying emails-only for domain {domain}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="internal_error",
                message="An internal error occurred",
                status=500
            ).dict()
        )


@router.get("/contact-info", response_model=LeanBusinessListResponse)
async def get_contact_info_by_domain(
    domain: str = Query(..., description="Domain name to search for"),
    authenticated: bool = Depends(verify_api_key),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Get essential contact info for businesses by domain.

    Returns ~25 fields: emails, phones, and basic location data.
    Ideal for basic outreach use cases.

    **Data reduction:** 77% (~25 vs 111 fields)
    """
    try:
        businesses = await LeanQueryBuilder.by_domain_contact_info(conn, domain)

        # Map to contact-info response model
        business_list = [ContactInfoResponse(**b) for b in businesses]

        return LeanBusinessListResponse(
            count=len(business_list),
            businesses=business_list,
            domain_query=domain,
            timestamp=datetime.utcnow()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying contact-info for domain {domain}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="internal_error",
                message="An internal error occurred",
                status=500
            ).dict()
        )


@router.get("/full-profile", response_model=LeanBusinessListResponse)
async def get_full_profile_by_domain(
    domain: str = Query(..., description="Domain name to search for"),
    authenticated: bool = Depends(verify_api_key),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Get complete outreach-ready data for businesses by domain.

    Returns ~40 fields: emails, phones, location, social media, and business details.
    Ideal for full outreach campaigns.

    **Data reduction:** 64% (~40 vs 111 fields)
    """
    try:
        businesses = await LeanQueryBuilder.by_domain_full_profile(conn, domain)

        # Map to full-profile response model
        business_list = [FullProfileResponse(**b) for b in businesses]

        return LeanBusinessListResponse(
            count=len(business_list),
            businesses=business_list,
            domain_query=domain,
            timestamp=datetime.utcnow()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying full-profile for domain {domain}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="internal_error",
                message="An internal error occurred",
                status=500
            ).dict()
        )
