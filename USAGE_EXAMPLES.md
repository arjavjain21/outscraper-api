# Outscraper API Usage Examples

## Authentication

**No authentication required** - This is an internal API with no authentication configured.

## Base URL

```
https://data.eagleinfoservice.com/api/v1/outscraper
```

## Endpoint Examples

### 1. Health Check

```bash
curl https://data.eagleinfoservice.com/api/v1/outscraper/health
```

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "pool_size": {
    "min": 10,
    "max": 50
  }
}
```

### 2. Lookup Business by Domain

```bash
curl "https://data.eagleinfoservice.com/api/v1/outscraper/business/by-domain?domain=example.com"
```

Or with a real domain:
```bash
curl "https://data.eagleinfoservice.com/api/v1/outscraper/business/by-domain?domain=google.com"
```

### 3. Lookup Business by Email

```bash
curl "https://data.eagleinfoservice.com/api/v1/outscraper/business/by-email?email=contact@example.com"
```

### 4. Lookup Business by LinkedIn URL

```bash
curl "https://data.eagleinfoservice.com/api/v1/outscraper/business/by-linkedin?linkedin=linkedin.com/company/example"
```

### 5. Lookup Business by Google Place ID

```bash
curl "https://data.eagleinfoservice.com/api/v1/outscraper/business/by-place-id?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4"
```

### 6. Lookup Business by Google ID

```bash
curl "https://data.eagleinfoservice.com/api/v1/outscraper/business/by-google-id?google_id=0x1234567890abcdef"
```

### 7. Batch Email Lookup (POST)

```bash
curl -X POST "https://data.eagleinfoservice.com/api/v1/outscraper/business/by-email/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      "email1@example.com",
      "email2@example.com",
      "email3@example.com"
    ]
  }'
```

**Note:** Maximum 100 emails per request.

### 8. Get Enriched Contacts (Paginated)

```bash
# First 100 results
curl "https://data.eagleinfoservice.com/api/v1/outscraper/business/contacts/enriched?limit=100&offset=0"

# Next 100 results
curl "https://data.eagleinfoservice.com/api/v1/outscraper/business/contacts/enriched?limit=100&offset=100"
```

## Python Examples

### Using requests library

```python
import requests

base_url = "https://data.eagleinfoservice.com/api/v1/outscraper"

# Health check
response = requests.get(f"{base_url}/health")
print(response.json())

# Search by domain
response = requests.get(f"{base_url}/business/by-domain", params={"domain": "example.com"})
data = response.json()
print(f"Found {data['count']} businesses")
for business in data['businesses']:
    print(f"- {business['name']}: {business['email_1']}")

# Batch email lookup
response = requests.post(
    f"{base_url}/business/by-email/batch",
    json={"emails": ["email1@example.com", "email2@example.com"]}
)
data = response.json()
print(f"Found {data['count']} businesses")
```

### Using httpx (async)

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Search by domain
        response = await client.get(
            "https://data.eagleinfoservice.com/api/v1/outscraper/business/by-domain",
            params={"domain": "example.com"}
        )
        data = response.json()
        print(f"Found {data['count']} businesses")

asyncio.run(main())
```

## JavaScript/Node.js Examples

### Using fetch

```javascript
const baseUrl = 'https://data.eagleinfoservice.com/api/v1/outscraper';

// Health check
fetch(`${baseUrl}/health`)
  .then(res => res.json())
  .then(data => console.log(data));

// Search by domain
fetch(`${baseUrl}/business/by-domain?domain=example.com`)
  .then(res => res.json())
  .then(data => {
    console.log(`Found ${data.count} businesses`);
    data.businesses.forEach(business => {
      console.log(`${business.name}: ${business.email_1}`);
    });
  });

// Batch email lookup
fetch(`${baseUrl}/business/by-email/batch`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    emails: ['email1@example.com', 'email2@example.com']
  })
})
  .then(res => res.json())
  .then(data => console.log(`Found ${data.count} businesses`));
```

## Response Format

All endpoints return JSON with the following structure:

### Single Business (by-place-id)
```json
{
  "id": 12345,
  "name": "Business Name",
  "email_1": "contact@example.com",
  "phone": "+1234567890",
  "site": "https://example.com",
  ...
}
```

### Multiple Businesses (all other endpoints)
```json
{
  "count": 2,
  "businesses": [
    {
      "id": 12345,
      "name": "Business 1",
      ...
    },
    {
      "id": 12346,
      "name": "Business 2",
      ...
    }
  ]
}
```

## Error Responses

### 404 Not Found
```json
{
  "detail": "Business with place_id 'xxx' not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["query", "domain"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error: ..."
}
```

## Rate Limiting

**No rate limiting configured** - Use responsibly for internal tools.

## Documentation

- **Swagger UI**: https://data.eagleinfoservice.com/api/v1/outscraper/docs
- **ReDoc**: https://data.eagleinfoservice.com/api/v1/outscraper/redoc
- **OpenAPI JSON**: https://data.eagleinfoservice.com/api/v1/outscraper/openapi.json
