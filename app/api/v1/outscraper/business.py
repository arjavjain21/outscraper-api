"""Business lookup API endpoints"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
import asyncpg
import logging

from app.models.business import (
    BusinessResponse,
    BusinessListResponse,
    BatchEmailRequest,
    BatchEmailResponse,
)
from app.db import get_pool
from app.utils.query_builders import QueryBuilder

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/business", tags=["business"])


async def get_db_connection():
    """Dependency to get database connection"""
    pool = await get_pool()
    conn = await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)


@router.get("/by-domain", response_model=BusinessListResponse)
async def get_business_by_domain(
    domain: str = Query(..., description="Domain name to search for"),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Lookup businesses by domain name.
    
    Supports partial domain matching (e.g., "example.com" will match "www.example.com").
    """
    try:
        businesses = await QueryBuilder.by_domain(conn, domain)
        return BusinessListResponse(
            count=len(businesses),
            businesses=[BusinessResponse(**b) for b in businesses]
        )
    except Exception as e:
        logger.error(f"Error querying by domain {domain}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/by-linkedin", response_model=BusinessListResponse)
async def get_business_by_linkedin(
    linkedin: str = Query(..., description="LinkedIn URL to search for"),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Lookup businesses by LinkedIn URL.
    
    Supports partial LinkedIn URL matching.
    """
    try:
        businesses = await QueryBuilder.by_linkedin(conn, linkedin)
        return BusinessListResponse(
            count=len(businesses),
            businesses=[BusinessResponse(**b) for b in businesses]
        )
    except Exception as e:
        logger.error(f"Error querying by LinkedIn {linkedin}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/by-place-id", response_model=BusinessResponse)
async def get_business_by_place_id(
    place_id: str = Query(..., description="Google Place ID"),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Lookup business by Google Place ID.
    
    Returns a single business record if found.
    """
    try:
        business = await QueryBuilder.by_place_id(conn, place_id)
        if not business:
            raise HTTPException(status_code=404, detail=f"Business with place_id '{place_id}' not found")
        return BusinessResponse(**business)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying by place_id {place_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/by-email", response_model=BusinessListResponse)
async def get_business_by_email(
    email: str = Query(..., description="Email address to search for"),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Lookup businesses by email address.
    
    Searches across email_1, email_2, and email_3 fields.
    """
    try:
        businesses = await QueryBuilder.by_email(conn, email)
        return BusinessListResponse(
            count=len(businesses),
            businesses=[BusinessResponse(**b) for b in businesses]
        )
    except Exception as e:
        logger.error(f"Error querying by email {email}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/by-google-id", response_model=BusinessListResponse)
async def get_business_by_google_id(
    google_id: str = Query(..., description="Google ID, CID, or KGMID"),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Lookup businesses by Google ID.
    
    Searches across google_id, cid, and kgmid fields.
    """
    try:
        businesses = await QueryBuilder.by_google_id(conn, google_id)
        return BusinessListResponse(
            count=len(businesses),
            businesses=[BusinessResponse(**b) for b in businesses]
        )
    except Exception as e:
        logger.error(f"Error querying by google_id {google_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/by-email/batch", response_model=BatchEmailResponse)
async def get_businesses_by_email_batch(
    request: BatchEmailRequest,
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Batch lookup businesses by multiple email addresses.
    
    Accepts up to 100 email addresses per request.
    Searches across email_1, email_2, and email_3 fields.
    """
    try:
        businesses = await QueryBuilder.batch_by_emails(conn, request.emails)
        return BatchEmailResponse(
            count=len(businesses),
            businesses=[BusinessResponse(**b) for b in businesses]
        )
    except Exception as e:
        logger.error(f"Error in batch email query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/contacts/enriched", response_model=BusinessListResponse)
async def get_enriched_contacts(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    """
    Get businesses with enriched contact information.
    
    Returns businesses that have email addresses, ordered by ID.
    Supports pagination via limit and offset parameters.
    """
    try:
        businesses = await QueryBuilder.enriched_contacts(conn, limit=limit, offset=offset)
        return BusinessListResponse(
            count=len(businesses),
            businesses=[BusinessResponse(**b) for b in businesses]
        )
    except Exception as e:
        logger.error(f"Error querying enriched contacts: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
