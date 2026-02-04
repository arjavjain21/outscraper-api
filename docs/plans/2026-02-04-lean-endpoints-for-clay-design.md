# Lean Endpoints for Clay Integration - Design Document

**Date:** 2026-02-04
**Author:** Claude Code
**Status:** Approved
**Purpose:** Create optimized API endpoints for Clay tool integration

---

## Executive Summary

Create 3 new lean API endpoints that return only essential contact data (emails, phones, social media) instead of all 111 database fields. This reduces response size by 64-88%, improves performance, and provides cleaner data for Clay workflows.

---

## Requirements

### Functional Requirements

1. **3 new endpoints** with different data granularity levels
2. **API authentication** via Bearer token
3. **Domain-based lookup** (same input as existing endpoint)
4. **Clay-optimized responses** (clean JSON, predictable structure)
5. **Backward compatibility** (existing endpoint unchanged)

### Non-Functional Requirements

1. **Performance:** 64-88% data reduction
2. **Security:** API key authentication
3. **Reliability:** Proper error handling for Clay workflows
4. **Maintainability:** Clean code, reusable components

---

## API Endpoints

### 1. Email-Only Endpoint

**URL:** `GET /api/v1/outscraper/business/domain/emails-only`

**Purpose:** Minimal response for email validation/lookup

**Request:**
```bash
GET /api/v1/outscraper/business/domain/emails-only?domain=example.com
Authorization: Bearer osk_YOUR_KEY
```

**Response Fields (13 total):**
- `id`, `name`, `site`
- `email_1`, `email_1_full_name`, `email_1_title`, `email_1_phone`
- `email_2`, `email_2_full_name`, `email_2_title`, `email_2_phone`
- `email_3`, `email_3_full_name`, `email_3_title`, `email_3_phone`

**Data Reduction:** 88% (13 vs 111 fields)

---

### 2. Contact Info Endpoint

**URL:** `GET /api/v1/outscraper/business/domain/contact-info`

**Purpose:** Essential contact data for basic outreach

**Response Fields (~25 total):**
- All email fields (13 fields)
- `phone`, `phone_1`, `phone_2`, `phone_3`
- `city`, `state`, `full_address`
- `category`

**Data Reduction:** 77% (~25 vs 111 fields)

---

### 3. Full Profile Endpoint

**URL:** `GET /api/v1/outscraper/business/domain/full-profile`

**Purpose:** Complete outreach-ready data including social media

**Response Fields (~40 total):**
- All contact fields (~25 fields)
- Social media: `linkedin`, `facebook`, `instagram`, `twitter`
- Business details: `description`, `rating`, `reviews`, `type`
- Full address: `postal_code`, plus basic fields

**Data Reduction:** 64% (~40 vs 111 fields)

---

## Response Format

All endpoints follow this consistent structure:

```json
{
  "count": 1,
  "businesses": [
    {
      "id": 108,
      "name": "The Moon Café",
      "site": "https://www.themoonnoho.com/",
      "email_1": "themoonnoho@gmail.com",
      "email_1_full_name": "John Doe",
      "email_1_title": "Manager",
      "...": "..."
    }
  ],
  "domain_query": "themoonnoho.com",
  "timestamp": "2026-02-04T05:30:00Z"
}
```

---

## Authentication

### Method

**Single Bearer Token** stored in environment variable

### API Key Format

- **Prefix:** `osk_` (Outscraper Service Key)
- **Length:** 64 characters (cryptographically secure)
- **Example:** `osk_kX9jM3nVpQ2rT8wY4hJ6fD5gA7sD9fZ2qW4eR6tY8uI0oP3lK5jH7gF9dS1zX3cV5b`

### Storage

```bash
# .env file
OUTSCRAPER_API_KEY=osk_<64-char-random>
OUTSCRAPER_API_ENABLED=true
```

### Usage

```bash
curl -X GET \
  "https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/emails-only?domain=example.com" \
  -H "Authorization: Bearer osk_YOUR_KEY"
```

---

## Technical Architecture

### Query Strategy

**Custom SELECT queries** for each endpoint (not filtering in Python)

**Rationale:**
- Only fetch needed columns from database
- 50-70% faster response times
- Lower bandwidth usage
- Better Clay performance

### File Structure

```
app/
├── api/
│   ├── middleware.py          # NEW: Authentication
│   └── v1/
│       └── outscraper/
│           ├── business.py    # EXISTING: Unchanged
│           └── lean.py        # NEW: Lean endpoints
├── models/
│   ├── business.py            # EXISTING: Full model (111 fields)
│   └── business_lean.py       # NEW: Lean models (13/25/40 fields)
├── utils/
│   ├── query_builders.py      # EXISTING: Full queries
│   └── lean_queries.py        # NEW: Optimized queries
└── config.py                  # MODIFY: Add API_KEY settings
```

---

## Error Handling

### Success Response (200 OK)

```json
{
  "count": 0,
  "businesses": [],
  "domain_query": "notfound.com",
  "timestamp": "2026-02-04T05:30:00Z"
}
```

### Authentication Errors

**Missing/Invalid API Key (401 Unauthorized):**
```json
{
  "error": "authentication_required",
  "message": "Invalid or missing API key",
  "status": 401
}
```

### Validation Errors

**Invalid Domain Format (400 Bad Request):**
```json
{
  "error": "invalid_domain",
  "message": "Domain 'invalid-input' is not a valid domain format",
  "status": 400
}
```

### Server Errors

**Database Connection Error (503 Service Unavailable):**
```json
{
  "error": "service_unavailable",
  "message": "Service temporarily unavailable",
  "status": 503
}
```

---

## Security Considerations

### Implemented Measures

1. ✅ API key stored in environment variable (.env)
2. ✅ .env file in .gitignore (never committed)
3. ✅ HTTPS only (already configured via Nginx)
4. ✅ Input validation (domain normalization)
5. ✅ SQL injection prevention (prepared statements)
6. ✅ No sensitive data in error messages
7. ✅ API key sanitized from logs (only prefix logged)

### CORS Configuration

Current: `allow_origins=["*"]` (open)

**Future enhancement:** Restrict to Clay domains if needed:
```python
allow_origins=["https://app.clay.com", "https://www.clay.com"]
```

---

## Performance Optimizations

### Data Reduction

| Endpoint | Fields | Reduction |
|----------|--------|-----------|
| Email-only | 13 | 88% |
| Contact info | ~25 | 77% |
| Full profile | ~40 | 64% |

### Query Optimization

- Custom SELECT queries fetch only needed columns
- Reuse existing database connection pool
- Prepared statements for caching
- Domain normalization (ILIKE indexes)

### Expected Performance

- **Current endpoint:** ~200-300ms (111 fields)
- **Email-only:** ~50-100ms (88% less data)
- **Contact info:** ~80-150ms (77% less data)
- **Full profile:** ~100-180ms (64% less data)

---

## Testing Strategy

### Unit Tests

**File:** `tests/test_lean_endpoints.py`

Test cases:
1. ✅ Email-only endpoint returns correct fields
2. ✅ Contact-info endpoint includes phones + location
3. ✅ Full-profile endpoint includes social media
4. ✅ Missing API key returns 401
5. ✅ Invalid API key returns 401
6. ✅ Invalid domain returns 400
7. ✅ Domain not found returns empty array (not error)
8. ✅ Response format matches Clay requirements

### Integration Tests

Test with real domains:
```bash
curl -X GET \
  "https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/emails-only?domain=themoonnoho.com" \
  -H "Authorization: Bearer osk_YOUR_KEY"
```

### Clay Testing Checklist

1. Test field mapping in Clay UI
2. Verify response structure consistency
3. Test empty results handling
4. Test error responses in Clay workflows
5. Performance testing (< 200ms target)

---

## Implementation Plan

### Phase 1: Setup & Configuration
1. Backup current `.env` file
2. Generate and save API key in `.env`
3. Update `app/config.py` with API settings

### Phase 2: Core Components
4. Create authentication middleware (`app/api/middleware.py`)
5. Create lean response models (`app/models/business_lean.py`)
6. Create optimized SQL queries (`app/utils/lean_queries.py`)

### Phase 3: API Endpoints
7. Create new lean endpoints (`app/api/v1/outscraper/lean.py`)
8. Register router in `app/main.py`

### Phase 4: Testing & Deployment
9. Create unit tests
10. Test endpoints manually with curl
11. Restart outscraper-api service
12. Final verification

---

## Rollout Plan

### Step 1: Deploy to Production
- Deploy without Clay integration (testing mode)
- Verify all endpoints work with API key
- Document API key for Clay team

### Step 2: Clay Integration
- Share API documentation with Clay team
- Provide test endpoint (domain with known data)
- Gather feedback

### Step 3: Monitor & Optimize
- Monitor response times
- Track Clay usage patterns
- Optimize queries based on real usage

---

## API Key Management

### Key Storage

**Location:** `/home/ubuntu/outscraper-api/.env`
**Format:** `OUTSCRAPER_API_KEY=osk_<64-char-random>`
**Backup:** `/home/ubuntu/outscraper-api/.env.backup-YYYYMMDD`

### Key Rotation Process

1. Generate new key
2. Update .env file
3. Restart service
4. Share new key with Clay team
5. Monitor for failed requests (old key usage)

---

## Future Enhancements

### Potential Additions

1. **Batch endpoint:** Accept multiple domains in single request
   ```
   POST /api/v1/outscraper/business/domain/batch
   {"domains": ["example.com", "test.com"]}
   ```

2. **Response caching:** Cache frequently queried domains
   - Redis cache with 5-minute TTL
   - Reduce database load

3. **Usage analytics:** Track Clay usage patterns
   - Request counts per endpoint
   - Most queried domains
   - Response time metrics

4. **Webhook notifications:** Notify Clay of data updates
   - New email discovered
   - Data refresh complete

---

## Clay Integration Guide

### Quick Start

1. **Get API Key:** Contact system administrator
2. **Make Request:**
   ```bash
   curl -X GET \
     "https://data.eagleinfoservice.com/api/v1/outscraper/business/domain/emails-only?domain=example.com" \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

3. **Map Fields in Clay:**
   - Import response to Clay table
   - Map `businesses[0].email_1` to email field
   - Map `businesses[0].name` to company field

### Clay Workflow Example

```
1. Input: Company domain
2. API Call: /domain/emails-only
3. Condition: If count > 0
4. Action: Import email_1, email_2, email_3
5. Else: Log "No emails found"
```

---

## Success Criteria

1. ✅ All 3 endpoints functional and tested
2. ✅ API authentication working
3. ✅ 64-88% data reduction achieved
4. ✅ Clay team can integrate successfully
5. ✅ Response time < 200ms (p95)
6. ✅ Error handling covers all edge cases
7. ✅ Documentation complete

---

## Appendix: Database Schema Reference

### Relevant Tables

**Table:** `businesses`
**Total Columns:** 111
**Indexed Columns:**
- `site` (gin_trgm for ILIKE searches)
- `email_1`, `email_2`, `email_3`
- `phone`, `phone_1`, `phone_2`, `phone_3`
- `linkedin`, `facebook`, `instagram`, `twitter`

**Query Performance:**
- Index lookup: ~1-5ms
- Full query: ~50-200ms (depending on fields)

---

**Document Version:** 1.0
**Last Updated:** 2026-02-04
**Status:** Ready for Implementation
