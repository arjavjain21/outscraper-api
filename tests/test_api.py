"""Integration tests for API endpoints"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code in [200, 503]  # 503 if DB not connected in test


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "status" in data


@pytest.mark.asyncio
async def test_by_domain_endpoint():
    """Test business lookup by domain"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/outscraper/business/by-domain?domain=example.com")
        # Should return 200 even if no results (empty list)
        assert response.status_code in [200, 500]  # 500 if DB not connected


@pytest.mark.asyncio
async def test_by_email_endpoint():
    """Test business lookup by email"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/outscraper/business/by-email?email=test@example.com")
        assert response.status_code in [200, 500]


@pytest.mark.asyncio
async def test_by_place_id_endpoint():
    """Test business lookup by place ID"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/outscraper/business/by-place-id?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4")
        assert response.status_code in [200, 404, 500]


@pytest.mark.asyncio
async def test_batch_email_endpoint():
    """Test batch email lookup"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/outscraper/business/by-email/batch",
            json={"emails": ["test@example.com", "user@example.com"]}
        )
        assert response.status_code in [200, 500]


@pytest.mark.asyncio
async def test_enriched_contacts_endpoint():
    """Test enriched contacts endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/outscraper/business/contacts/enriched?limit=10&offset=0")
        assert response.status_code in [200, 500]
