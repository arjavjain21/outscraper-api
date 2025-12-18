# Outscraper Business API

High-performance FastAPI service for querying the Outscraper business database (1.18M+ businesses).

## Features

- **7 API Endpoints** for business lookups
- **Async/await** with asyncpg for maximum performance
- **Connection pooling** (10-50 connections)
- **Prepared statements** for optimized queries
- **Comprehensive response models** (all 111 columns)
- **Health check endpoint** for monitoring
- **Full test coverage** (unit + integration tests)

## API Endpoints

All endpoints are prefixed with `/api/v1/outscraper`

### Business Lookups

1. **GET** `/business/by-domain?domain=example.com`
   - Lookup businesses by domain name
   - Supports partial matching

2. **GET** `/business/by-linkedin?linkedin=linkedin.com/company/example`
   - Lookup businesses by LinkedIn URL

3. **GET** `/business/by-place-id?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4`
   - Lookup business by Google Place ID
   - Returns single result

4. **GET** `/business/by-email?email=test@example.com`
   - Lookup businesses by email address
   - Searches across email_1, email_2, email_3

5. **GET** `/business/by-google-id?google_id=0x1234567890abcdef`
   - Lookup businesses by Google ID, CID, or KGMID

6. **POST** `/business/by-email/batch`
   - Batch lookup by multiple emails (up to 100)
   - Request body: `{"emails": ["email1@example.com", "email2@example.com"]}`

7. **GET** `/business/contacts/enriched?limit=100&offset=0`
   - Get businesses with enriched contact information
   - Supports pagination

### Utility Endpoints

- **GET** `/health` - Health check endpoint
- **GET** `/` - API information
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative API documentation

## Installation

### 1. Clone and Setup

```bash
cd /home/ubuntu/outscraper-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Run Database Migrations

```bash
sudo -u postgres psql outscraper < migrations/001_add_performance_indexes.sql
```

### 4. Run Tests

```bash
source venv/bin/activate
pytest
```

### 5. Start Development Server

```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Production Deployment

### Systemd Service

1. Copy service file:
```bash
sudo cp outscraper-api.service /etc/systemd/system/
```

2. Reload systemd and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable outscraper-api
sudo systemctl start outscraper-api
```

3. Check status:
```bash
sudo systemctl status outscraper-api
sudo journalctl -u outscraper-api -f
```

### Nginx Configuration

Add to your nginx configuration:

```nginx
location /api/v1/outscraper/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## Performance Optimizations

- **Connection Pooling**: 10-50 connections (configurable)
- **Prepared Statements**: All queries use prepared statements
- **Database Indexes**: Optimized indexes on lookup columns
- **Async Operations**: Full async/await for non-blocking I/O
- **Direct Database Queries**: No ORM overhead

## Database Schema

The API queries the `businesses` table with 111 columns including:
- Basic information (name, category, type)
- Contact details (phone, email, address)
- Geolocation (latitude, longitude)
- Reviews and ratings
- Social media profiles
- Google IDs (Place ID, CID, KGMID)
- Website metadata

See `DOCUMENTATION/technical/outscraper_database_info.json` for full schema details.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_normalization.py
```

## Monitoring

- Health check: `GET /health`
- Logs: `/var/log/outscraper-api.log`
- Systemd logs: `journalctl -u outscraper-api`

## License

Internal tool - for Hyperke use only.
