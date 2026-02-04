"""Lean response models for Clay integration"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class EmailOnlyResponse(BaseModel):
    """
    Email-focused response model (13 fields).
    For minimal email validation/lookup use cases.
    """
    # Basic identification
    id: int
    name: Optional[str] = None
    site: Optional[str] = None

    # Email 1
    email_1: Optional[str] = None
    email_1_full_name: Optional[str] = None
    email_1_title: Optional[str] = None
    email_1_phone: Optional[str] = None

    # Email 2
    email_2: Optional[str] = None
    email_2_full_name: Optional[str] = None
    email_2_title: Optional[str] = None
    email_2_phone: Optional[str] = None

    # Email 3
    email_3: Optional[str] = None
    email_3_full_name: Optional[str] = None
    email_3_title: Optional[str] = None
    email_3_phone: Optional[str] = None

    class Config:
        from_attributes = True


class ContactInfoResponse(BaseModel):
    """
    Essential contact info response model (~25 fields).
    For basic outreach use cases.
    Includes all emails + phones + basic location.
    """
    # Basic identification
    id: int
    name: Optional[str] = None
    site: Optional[str] = None
    category: Optional[str] = None

    # Phone numbers
    phone: Optional[str] = None
    phone_1: Optional[str] = None
    phone_2: Optional[str] = None
    phone_3: Optional[str] = None

    # Location
    city: Optional[str] = None
    state: Optional[str] = None
    full_address: Optional[str] = None

    # Email 1
    email_1: Optional[str] = None
    email_1_full_name: Optional[str] = None
    email_1_title: Optional[str] = None
    email_1_phone: Optional[str] = None

    # Email 2
    email_2: Optional[str] = None
    email_2_full_name: Optional[str] = None
    email_2_title: Optional[str] = None
    email_2_phone: Optional[str] = None

    # Email 3
    email_3: Optional[str] = None
    email_3_full_name: Optional[str] = None
    email_3_title: Optional[str] = None
    email_3_phone: Optional[str] = None

    class Config:
        from_attributes = True


class FullProfileResponse(BaseModel):
    """
    Complete outreach-ready response model (~40 fields).
    For full outreach campaigns with social media.
    """
    # Basic identification
    id: int
    name: Optional[str] = None
    name_for_emails: Optional[str] = None
    site: Optional[str] = None
    category: Optional[str] = None
    type_: Optional[str] = Field(None, alias="type")

    # Phone numbers
    phone: Optional[str] = None
    phone_1: Optional[str] = None
    phone_2: Optional[str] = None
    phone_3: Optional[str] = None

    # Full address
    full_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None

    # Business details
    description: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None

    # Social media
    linkedin: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None

    # Email 1
    email_1: Optional[str] = None
    email_1_full_name: Optional[str] = None
    email_1_title: Optional[str] = None
    email_1_phone: Optional[str] = None

    # Email 2
    email_2: Optional[str] = None
    email_2_full_name: Optional[str] = None
    email_2_title: Optional[str] = None
    email_2_phone: Optional[str] = None

    # Email 3
    email_3: Optional[str] = None
    email_3_full_name: Optional[str] = None
    email_3_title: Optional[str] = None
    email_3_phone: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class LeanBusinessListResponse(BaseModel):
    """
    Standard response wrapper for all lean endpoints.
    Provides consistent structure for Clay integration.
    """
    count: int = Field(..., description="Number of businesses returned")
    businesses: List = Field(..., description="List of businesses (varies by endpoint)")
    domain_query: str = Field(..., description="The domain that was searched")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str = Field(..., description="Error type/code")
    message: str = Field(..., description="Human-readable error message")
    status: int = Field(..., description="HTTP status code")
