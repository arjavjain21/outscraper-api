"""Unit tests for normalization utilities"""
import pytest
from app.utils.normalization import (
    normalize_domain,
    normalize_linkedin_url,
    normalize_email,
    normalize_place_id,
    normalize_google_id,
    extract_domain_from_email,
)


class TestNormalizeDomain:
    """Tests for domain normalization"""
    
    def test_full_url(self):
        assert normalize_domain("https://www.example.com/path") == "example.com"
    
    def test_url_with_port(self):
        assert normalize_domain("https://example.com:8080/path") == "example.com"
    
    def test_www_prefix(self):
        assert normalize_domain("www.example.com") == "example.com"
    
    def test_simple_domain(self):
        assert normalize_domain("example.com") == "example.com"
    
    def test_subdomain(self):
        assert normalize_domain("subdomain.example.com") == "subdomain.example.com"
    
    def test_http_url(self):
        assert normalize_domain("http://example.com") == "example.com"
    
    def test_domain_with_path(self):
        assert normalize_domain("example.com/path/to/page") == "example.com"
    
    def test_invalid_domain(self):
        assert normalize_domain("not-a-domain") is None
    
    def test_empty_string(self):
        assert normalize_domain("") is None
    
    def test_none(self):
        assert normalize_domain(None) is None
    
    def test_whitespace(self):
        assert normalize_domain("  example.com  ") == "example.com"
    
    def test_uppercase(self):
        assert normalize_domain("EXAMPLE.COM") == "example.com"


class TestNormalizeLinkedIn:
    """Tests for LinkedIn URL normalization"""
    
    def test_full_url(self):
        assert normalize_linkedin_url("https://www.linkedin.com/company/example") == "linkedin.com/company/example"
    
    def test_without_protocol(self):
        assert normalize_linkedin_url("linkedin.com/in/john-doe") == "linkedin.com/in/john-doe"
    
    def test_www_prefix(self):
        assert normalize_linkedin_url("www.linkedin.com/company/example") == "linkedin.com/company/example"
    
    def test_trailing_slash(self):
        assert normalize_linkedin_url("linkedin.com/company/example/") == "linkedin.com/company/example"
    
    def test_invalid_url(self):
        assert normalize_linkedin_url("not-linkedin.com/page") is None
    
    def test_empty_string(self):
        assert normalize_linkedin_url("") is None
    
    def test_none(self):
        assert normalize_linkedin_url(None) is None


class TestNormalizeEmail:
    """Tests for email normalization"""
    
    def test_simple_email(self):
        assert normalize_email("test@example.com") == "test@example.com"
    
    def test_uppercase(self):
        assert normalize_email("TEST@EXAMPLE.COM") == "test@example.com"
    
    def test_with_whitespace(self):
        assert normalize_email("  test@example.com  ") == "test@example.com"
    
    def test_invalid_email(self):
        assert normalize_email("not-an-email") is None
    
    def test_empty_string(self):
        assert normalize_email("") is None
    
    def test_none(self):
        assert normalize_email(None) is None


class TestNormalizePlaceId:
    """Tests for Place ID normalization"""
    
    def test_valid_place_id(self):
        assert normalize_place_id("ChIJN1t_tDeuEmsRUsoyG83frY4") == "ChIJN1t_tDeuEmsRUsoyG83frY4"
    
    def test_with_whitespace(self):
        assert normalize_place_id("  ChIJN1t_tDeuEmsRUsoyG83frY4  ") == "ChIJN1t_tDeuEmsRUsoyG83frY4"
    
    def test_empty_string(self):
        assert normalize_place_id("") is None
    
    def test_none(self):
        assert normalize_place_id(None) is None


class TestNormalizeGoogleId:
    """Tests for Google ID normalization"""
    
    def test_valid_google_id(self):
        assert normalize_google_id("0x1234567890abcdef") == "0x1234567890abcdef"
    
    def test_with_whitespace(self):
        assert normalize_google_id("  0x1234567890abcdef  ") == "0x1234567890abcdef"
    
    def test_empty_string(self):
        assert normalize_google_id("") is None
    
    def test_none(self):
        assert normalize_google_id(None) is None


class TestExtractDomainFromEmail:
    """Tests for domain extraction from email"""
    
    def test_simple_email(self):
        assert extract_domain_from_email("test@example.com") == "example.com"
    
    def test_subdomain(self):
        assert extract_domain_from_email("user@mail.example.com") == "mail.example.com"
    
    def test_invalid_email(self):
        assert extract_domain_from_email("not-an-email") is None
    
    def test_empty_string(self):
        assert extract_domain_from_email("") is None
    
    def test_none(self):
        assert extract_domain_from_email(None) is None
