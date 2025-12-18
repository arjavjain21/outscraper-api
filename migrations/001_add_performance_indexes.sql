-- Add performance indexes for Outscraper API lookups
-- These indexes optimize the query patterns used by the API endpoints

-- Enable pg_trgm extension for better text search (if not already enabled)
-- This enables trigram-based text search for domain matching
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Index for domain lookups (site column)
-- Used by: GET /api/v1/outscraper/business/by-domain
-- Note: Standard index first, trigram index created later
CREATE INDEX IF NOT EXISTS idx_businesses_site_lower 
ON businesses (LOWER(site)) WHERE site IS NOT NULL;

-- If pg_trgm extension is not available, use standard index
-- CREATE INDEX IF NOT EXISTS idx_businesses_site_lower 
-- ON businesses (LOWER(site));

-- Index for LinkedIn lookups
-- Used by: GET /api/v1/outscraper/business/by-linkedin
CREATE INDEX IF NOT EXISTS idx_businesses_linkedin 
ON businesses (linkedin) WHERE linkedin IS NOT NULL;

-- Index for email lookups (already exists as idx_email_1, but add for email_2 and email_3)
-- Used by: GET /api/v1/outscraper/business/by-email
-- Used by: POST /api/v1/outscraper/business/by-email/batch
CREATE INDEX IF NOT EXISTS idx_businesses_email_2 
ON businesses (email_2) WHERE email_2 IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_businesses_email_3 
ON businesses (email_3) WHERE email_3 IS NOT NULL;

-- Composite index for email lookups across all email fields
CREATE INDEX IF NOT EXISTS idx_businesses_emails_composite 
ON businesses (email_1, email_2, email_3) 
WHERE email_1 IS NOT NULL OR email_2 IS NOT NULL OR email_3 IS NOT NULL;

-- Index for Google ID lookups (cid and kgmid)
-- Used by: GET /api/v1/outscraper/business/by-google-id
CREATE INDEX IF NOT EXISTS idx_businesses_cid 
ON businesses (cid) WHERE cid IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_businesses_kgmid 
ON businesses (kgmid) WHERE kgmid IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_businesses_google_id 
ON businesses (google_id) WHERE google_id IS NOT NULL;

-- Index for enriched contacts endpoint
-- Used by: GET /api/v1/outscraper/business/contacts/enriched
-- This index already exists (idx_email_1), but we can add a composite for better performance
CREATE INDEX IF NOT EXISTS idx_businesses_enriched_contacts 
ON businesses (id, email_1) 
WHERE email_1 IS NOT NULL;

-- Add GIN index for site column using trigram (better for ILIKE queries)
-- This will significantly improve domain lookup performance
CREATE INDEX IF NOT EXISTS idx_businesses_site_trgm 
ON businesses USING gin (site gin_trgm_ops);

-- Analyze tables to update statistics
ANALYZE businesses;
