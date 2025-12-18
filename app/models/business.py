"""Business response model with all 111 columns"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BusinessResponse(BaseModel):
    """Complete business response model with all 111 columns"""
    
    # Primary key
    id: int
    
    # Basic information (8 columns)
    query: Optional[str] = None
    name: Optional[str] = None
    name_for_emails: Optional[str] = None
    site: Optional[str] = None
    subtypes: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    
    # Contact information (4 columns)
    phone: Optional[str] = None
    phone_1: Optional[str] = None
    phone_2: Optional[str] = None
    phone_3: Optional[str] = None
    
    # Address information (9 columns)
    full_address: Optional[str] = None
    borough: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None
    us_state: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    
    # Geolocation (6 columns)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    h3: Optional[str] = None
    time_zone: Optional[str] = None
    plus_code: Optional[str] = None
    area_service: Optional[str] = None
    
    # Reviews (11 columns)
    rating: Optional[float] = None
    reviews: Optional[int] = None
    reviews_link: Optional[str] = None
    reviews_tags: Optional[str] = None
    reviews_per_score: Optional[str] = None
    reviews_per_score_1: Optional[int] = None
    reviews_per_score_2: Optional[int] = None
    reviews_per_score_3: Optional[int] = None
    reviews_per_score_4: Optional[int] = None
    reviews_per_score_5: Optional[int] = None
    reviews_id: Optional[str] = None
    
    # Media (4 columns)
    photos_count: Optional[int] = None
    photo: Optional[str] = None
    street_view: Optional[str] = None
    logo: Optional[str] = None
    
    # Hours and location (6 columns)
    located_in: Optional[str] = None
    working_hours: Optional[str] = None
    working_hours_csv_compatible: Optional[str] = None
    working_hours_old_format: Optional[str] = None
    other_hours: Optional[str] = None
    popular_times: Optional[str] = None
    
    # Business details (8 columns)
    business_status: Optional[str] = None
    about: Optional[str] = None
    range: Optional[str] = None
    prices: Optional[str] = None
    posts: Optional[str] = None
    description: Optional[str] = None
    typical_time_spent: Optional[str] = None
    verified: Optional[bool] = None
    
    # Owner (3 columns)
    owner_id: Optional[str] = None
    owner_title: Optional[str] = None
    owner_link: Optional[str] = None
    
    # Booking (4 columns)
    reservation_links: Optional[str] = None
    booking_appointment_link: Optional[str] = None
    menu_link: Optional[str] = None
    order_links: Optional[str] = None
    
    # Google IDs (7 columns)
    location_link: Optional[str] = None
    location_reviews_link: Optional[str] = None
    place_id: Optional[str] = None
    google_id: Optional[str] = None
    cid: Optional[str] = None
    kgmid: Optional[str] = None
    located_google_id: Optional[str] = None
    
    # Emails - Email 1 (6 columns)
    email_1: Optional[str] = None
    email_1_full_name: Optional[str] = None
    email_1_first_name: Optional[str] = None
    email_1_last_name: Optional[str] = None
    email_1_title: Optional[str] = None
    email_1_phone: Optional[str] = None
    
    # Emails - Email 2 (6 columns)
    email_2: Optional[str] = None
    email_2_full_name: Optional[str] = None
    email_2_first_name: Optional[str] = None
    email_2_last_name: Optional[str] = None
    email_2_title: Optional[str] = None
    email_2_phone: Optional[str] = None
    
    # Emails - Email 3 (6 columns)
    email_3: Optional[str] = None
    email_3_full_name: Optional[str] = None
    email_3_first_name: Optional[str] = None
    email_3_last_name: Optional[str] = None
    email_3_title: Optional[str] = None
    email_3_phone: Optional[str] = None
    
    # Social media (15 columns)
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    tiktok: Optional[str] = None
    medium: Optional[str] = None
    reddit: Optional[str] = None
    skype: Optional[str] = None
    snapchat: Optional[str] = None
    telegram: Optional[str] = None
    whatsapp: Optional[str] = None
    twitter: Optional[str] = None
    vimeo: Optional[str] = None
    youtube: Optional[str] = None
    github: Optional[str] = None
    crunchbase: Optional[str] = None
    
    # Website metadata (6 columns)
    website_title: Optional[str] = None
    website_generator: Optional[str] = None
    website_description: Optional[str] = None
    website_keywords: Optional[str] = None
    website_has_fb_pixel: Optional[bool] = None
    website_has_google_tag: Optional[bool] = None
    
    # Metadata (2 columns)
    source_file: Optional[str] = None
    import_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BusinessListResponse(BaseModel):
    """Response model for list of businesses"""
    count: int
    businesses: list[BusinessResponse]


class BatchEmailRequest(BaseModel):
    """Request model for batch email lookup"""
    emails: list[str] = Field(..., min_length=1, max_length=100, description="List of email addresses to lookup")


class BatchEmailResponse(BaseModel):
    """Response model for batch email lookup"""
    count: int
    businesses: list[BusinessResponse]
