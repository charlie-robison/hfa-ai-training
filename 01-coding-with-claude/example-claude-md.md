# Example CLAUDE.md

# Project: Hawaii Real Estate Analytics Platform

## Overview
Python-based analytics platform that processes MLS data for Hawaii residential
real estate. Provides pricing analysis, market trend reports, and lead scoring.

## Tech Stack
- **Language:** Python 3.12+
- **Framework:** FastAPI for the REST API
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Task Queue:** Celery with Redis
- **AI/ML:** OpenAI GPT-4o API for analysis, scikit-learn for lead scoring
- **Vector DB:** Pinecone for semantic search
- **Testing:** pytest with pytest-asyncio
- **Deployment:** Docker containers on AWS ECS

## Project Structure
```
src/
  api/           # FastAPI route handlers
  models/        # SQLAlchemy database models
  services/      # Business logic layer
  agents/        # AI agent definitions and prompts
  pipelines/     # Multi-step agent pipelines
  utils/         # Shared utilities
tests/
  unit/          # Unit tests (no external dependencies)
  integration/   # Integration tests (may hit DB or APIs)
  fixtures/      # Shared test fixtures and sample data
scripts/         # One-off scripts and data migrations
```

## Common Commands
```bash
# Dev server
uvicorn src.api.main:app --reload --port 8000

# Tests
pytest                                    # All tests
pytest tests/unit/test_pricing.py -v      # Specific file
pytest --cov=src --cov-report=html        # With coverage

# Type checking and linting
mypy src/
ruff check src/ tests/

# Database
alembic upgrade head                      # Run migrations
alembic revision --autogenerate -m "msg"  # New migration
```

## Coding Conventions
- Type hints on all function signatures
- Pydantic models for structured data (never plain dicts for domain objects)
- Functions under 30 lines — extract helpers for clarity
- Google-style docstrings on all public functions
- Files: `snake_case.py` | Classes: `PascalCase` | Constants: `UPPER_SNAKE_CASE`

## Things to AVOID
- Do NOT modify files in `src/legacy/` — deprecated, being removed in v3.0
- Do NOT use `print()` for logging — use `src/utils/logging.py`
- Do NOT store secrets in code — all secrets come from environment variables
- Do NOT write raw SQL — use SQLAlchemy ORM
- Do NOT use `datetime.now()` — use `datetime.now(timezone.utc)`

## Domain Knowledge
- Properties are identified by TMK (Tax Map Key), not by address
- Price per square foot is the primary valuation metric
- "Comparable sales" (comps) must be within 90 days and 20% sqft range
- Lead scores: Hot (80+), Warm (50-79), Cold (0-49)
- All prices in USD. Hawaii has no state property tax exemption for investors.

## API Rate Limits
- OpenAI API: 500 requests/minute on our current plan
- MLS API: 100 requests/minute, data refreshes every 15 minutes
- Always implement retry with exponential backoff

## Additional Context
- @README.md
- @docs/architecture.md
