# Security Audit Report (Public Repository Readiness)

**Repository:** outscraper-api  
**Date:** 2026-04-25  
**Auditor:** GPT-5.3-Codex

## Executive Summary

This repository is **not currently safe to expose publicly** without changes.

Top risks identified:

1. **Hardcoded/default database credentials in code and tracked env files**.
2. **An API key appears in documentation** (must be treated as compromised).
3. **Most business endpoints are unauthenticated** and can return large amounts of sensitive contact/business data.
4. **No rate-limiting or abuse controls**, enabling scraping and potential database load/DoS risk.
5. **Overly permissive CORS configuration** (`*` + credentials), creating unnecessary cross-origin risk.

## Scope Reviewed

- FastAPI app configuration and middleware
- Database connectivity and query layer
- API routes and auth behavior
- Repository files for secrets exposure
- Deployment and docs for insecure defaults

## Key Findings

### 1) Hardcoded/insecure defaults for DB credentials (High)

- `app/config.py` includes defaults for `DATABASE_URL` and `DATABASE_PASSWORD` with `temp12345`.
- `.env` is committed and contains DB connection details.
- `.env.example` also contains weak placeholder secrets.

**Risk:**
- If reused in any live environment, this can allow unauthorized DB access.
- Even placeholder values normalize insecure operational behavior.

**Fix:**
- Remove all credential defaults from application code.
- Fail fast on startup if required env vars are missing.
- Rotate DB password and create new least-privilege DB user.
- Keep `.env` out of git history and repository tracking.

### 2) API key disclosed in documentation (Critical if still valid)

- `LEAN_ENDPOINTS_GUIDE.md` contains a full `OUTSCRAPER_API_KEY` value and example Bearer token usage.

**Risk:**
- Key should be assumed compromised immediately.
- Attackers can query protected endpoints if key remains valid.

**Fix:**
- Revoke and rotate the key now.
- Purge key from current files and git history.
- Use secret manager (or environment injection) for runtime only.

### 3) Unauthenticated data extraction endpoints (Critical)

- Business router endpoints (`/business/*`) do not require API key auth.
- These endpoints return rich dataset fields including emails and personal/contact details.

**Risk:**
- Public users can enumerate/exfiltrate records.
- Possible privacy, compliance, and contractual risk.

**Fix:**
- Require authentication on **all** data endpoints.
- Add authorization tiers/scopes per endpoint.
- Introduce field-level filtering by consumer role.

### 4) No rate limiting / abuse protections (High)

- No app-level throttling, quotas, or anti-abuse controls were found.
- Endpoint patterns and pagination can be used to scrape at scale.

**Risk:**
- DB pressure and cost spikes.
- Service degradation or outage.
- Accelerated data exfiltration.

**Fix:**
- Add per-key and per-IP rate limits and burst limits.
- Add WAF / reverse-proxy protections and request timeouts.
- Add query complexity constraints and global concurrency limits.

### 5) CORS too permissive (Medium)

- CORS is configured with `allow_origins=["*"]` and `allow_credentials=True`.

**Risk:**
- Broadens cross-origin attack surface and can break browser expectations.

**Fix:**
- Restrict origins to trusted frontend domains.
- Disable credentials unless strictly required.

### 6) Error details may leak internals (Medium)

- Some endpoints include `str(e)` in HTTP 500 responses and health check outputs.

**Risk:**
- Internal DB/network details can leak to attackers.

**Fix:**
- Return generic messages to clients.
- Log detailed exceptions server-side only.

### 7) Logging strategy may expose sensitive context (Medium)

- Auth middleware logs API key prefixes.

**Risk:**
- Partial secret disclosure in logs can aid credential stuffing/correlation.

**Fix:**
- Avoid logging token material entirely.
- Use request IDs and structured event logs.

### 8) Transport security not enforced at app layer (Medium)

- Service listens on `0.0.0.0`; TLS assumptions are delegated to reverse proxy.

**Risk:**
- Misconfiguration could expose plaintext traffic internally.

**Fix:**
- Enforce HTTPS at edge and internal network segmentation.
- Add `TrustedHostMiddleware` and proxy header hardening.

## Database Threat Assessment

### Direct DB takeover risk
- Depends on whether committed credentials are active and DB network exposure.
- If DB allows remote connections with these credentials, risk is severe.

### Data exfiltration risk
- High due to unauthenticated query endpoints and broad response payloads.

### DoS / performance risk
- Medium-to-High due to absent throttling and potentially expensive repeated queries.

## Public Repo Readiness Verdict

**Current state:** ❌ **Not safe for public release**.

## Immediate Remediation Plan (Priority Order)

1. **Rotate all secrets now** (DB passwords, API keys, any tokens).
2. **Remove `.env` from git tracking** and purge historical secrets from git history.
3. **Delete/replace exposed key values in docs**.
4. **Enforce auth on all data endpoints**, not only lean routes.
5. **Add rate limiting and abuse controls** at app + reverse proxy.
6. **Restrict CORS** to known origins.
7. **Sanitize all error responses** to avoid internal detail leaks.
8. **Implement least-privilege DB account** (read-only if applicable) and network ACL restrictions.
9. **Add automated secret scanning and dependency scanning in CI**.
10. **Create SECURITY.md + incident response process**.

## Suggested Ongoing Security Controls

- Pre-commit: `gitleaks` or `trufflehog` secret scan.
- CI: secret scanning + dependency CVE scanning + SAST.
- Runtime: API gateway keys, quotas, monitoring alerts, anomaly detection.
- Ops: regular key rotation and access review.

