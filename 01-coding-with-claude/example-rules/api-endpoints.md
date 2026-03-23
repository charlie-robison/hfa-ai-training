---
paths:
  - "src/api/**/*.py"
---

# API Endpoint Conventions

These rules apply only when working with files in `src/api/`.

## Route Naming
- Use kebab-case: `/api/v1/market-analysis` not `/api/v1/marketAnalysis`
- Always include the API version: `/api/v1/...`
- Use plural nouns for collections: `/api/v1/listings` not `/api/v1/listing`

## Request/Response
- All request bodies use Pydantic models for validation
- All responses use a standard envelope: `{"data": ..., "meta": {...}}`
- Error responses use: `{"error": {"code": "...", "message": "..."}}`
- Return appropriate HTTP status codes (201 for create, 204 for delete)

## Authentication
- All endpoints require Bearer token auth except `/api/v1/health`
- Use the `@require_auth` decorator from `src/api/middleware.py`
- Never log or return auth tokens in response bodies

## Performance
- Paginate all list endpoints (default 20, max 100)
- Include `X-Request-Id` header for tracing
- Log request duration for all endpoints over 500ms
