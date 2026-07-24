# INTERSERVIM AI SALES AGENT — Roadmap

## Phase Overview

| Phase | Name | Estimated Effort | Status |
|-------|------|-----------------|--------|
| 0 | Architecture & Documentation | 1 day | ✅ Current |
| 1 | Monorepo & Configuration | 1 day | ⬜ |
| 2 | Database & Migrations | 2 days | ⬜ |
| 3 | Authentication | 2 days | ⬜ |
| 4 | Products API | 1 day | ⬜ |
| 5 | Customers & CRM | 1 day | ⬜ |
| 6 | Conversations | 1 day | ⬜ |
| 7 | AI Agent Engine | 3 days | ⬜ |
| 8 | WhatsApp Integration | 2 days | ⬜ |
| 9 | Quotes & PDF | 2 days | ⬜ |
| 10 | Knowledge Base | 2 days | ⬜ |
| 11 | Marketing AI Studio | 2 days | ⬜ |
| 12 | Flutter App Complete | 5 days | ⬜ |
| 13 | Automatic Follow-ups | 1 day | ⬜ |
| 14 | Analytics | 1 day | ⬜ |
| 15 | Complete Testing | 2 days | ⬜ |
| 16 | Security Hardening | 1 day | ⬜ |
| 17 | Docker & Production | 1 day | ⬜ |
| 18 | APK Generation | 1 day | ⬜ |

**Total estimated effort: ~30 days**

## Detailed Phase Breakdown

### FASE 0 — Architecture & Documentation
- Create project directory structure
- Write ARCHITECTURE.md, ROADMAP.md, DATABASE.md, API.md, SECURITY.md, AI_AGENT.md
- Define all entities, relationships, flows, APIs, modules
- Risk assessment

### FASE 1 — Monorepo & Configuration
- Initialize Git repository
- Create monorepo structure: apps/, packages/, infrastructure/, docs/, tests/
- Set up Flutter project in apps/mobile/flutter_app/
- Set up FastAPI project in apps/backend/api/
- Configure Docker + Docker Compose (PostgreSQL, Redis, API)
- Create .env.example, .gitignore, README.md
- Verify API starts, Flutter builds, DB connects

### FASE 2 — Database & Migrations
- Implement SQLAlchemy models for all entities
- Create Alembic migration scripts
- Set up indexes, foreign keys, constraints
- Create seed data script
- Verify migrations run cleanly

### FASE 3 — Authentication
- User registration endpoint
- Login with JWT access + refresh tokens
- Token refresh endpoint
- Current user endpoint
- RBAC middleware
- Password hashing (bcrypt)
- Auth tests

### FASE 4 — Products API
- Product CRUD endpoints
- Search, filter, pagination
- Category management
- Product image support
- Stock/availability management

### FASE 5 — Customers & CRM
- Customer CRUD endpoints
- Status management (NEW → CONTACTED → ... → WON/LOST)
- Notes and follow-up tracking
- Conversation history per customer
- Product interest tracking

### FASE 6 — Conversations
- Conversation CRUD
- Message CRUD
- Channel support (WhatsApp, manual, etc.)
- AI enable/disable per conversation
- Human handoff mechanism

### FASE 7 — AI Agent Engine
- AI provider abstraction layer
- OpenAI provider implementation
- Intent classifier
- Response generator with sales personality
- Context manager (summary + recent messages)
- Knowledge retrieval (RAG)
- Sales engine (stage detection, follow-up triggers)
- Safety guardrails (no inventing data)

### FASE 8 — WhatsApp Integration
- Webhook verification endpoint
- Incoming message handler
- Message parser (text, media, documents)
- WhatsApp client for sending messages
- Message status callbacks
- Full integration test with simulator

### FASE 9 — Quotes & PDF
- Quote CRUD endpoints
- Quote item management
- PDF generation with company branding
- Quote status workflow
- Email sending (optional)

### FASE 10 — Knowledge Base
- Document upload (PDF, DOCX, XLSX, TXT)
- Text extraction pipeline
- Chunking and embedding generation
- Vector storage (configurable provider)
- RAG search endpoint for AI context

### FASE 11 — Marketing AI Studio
- AI content generation endpoints
- Content types: WhatsApp status, ads, emails, posts
- Campaign management CRUD
- Template system
- Product-specific content generation

### FASE 12 — Flutter App Complete
- All screens (see ARCHITECTURE.md)
- Material 3 theming
- GoRouter navigation
- Riverpod state management
- Dio HTTP client with interceptors
- Auth token management
- Charts and analytics visualizations
- Loading, empty, error states

### FASE 13 — Automatic Follow-ups
- Follow-up scheduling (24h, 48h, 72h, custom)
- Celery/ARQ tasks for scheduled execution
- Smart follow-up (check for customer reply before sending)
- Follow-up templates

### FASE 14 — Analytics
- Overview metrics endpoint
- Conversation analytics
- Product analytics
- Sales funnel analytics
- Dashboard charts data

### FASE 15 — Complete Testing
- Backend unit tests (pytest)
- Backend integration tests
- API tests (httpx)
- Auth and security tests
- AI service tests (mocked)
- Webhook tests
- Flutter unit tests
- Flutter widget tests
- Flutter integration tests

### FASE 16 — Security Hardening
- Rate limiting
- Input sanitization
- SQL injection prevention
- XSS protection
- CORS hardening
- Security headers
- Dependency scanning
- Penetration test simulation

### FASE 17 — Docker & Production
- Production Dockerfile optimization
- Docker Compose production config
- Health checks
- Logging infrastructure
- Backup strategy
- Monitoring setup

### FASE 18 — APK Generation
- Flutter build configuration
- Android signing setup
- ProGuard rules
- APK generation script
- Version management
- Distribution preparation

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| LLM hallucination (inventing products) | Medium | Critical | Safety guardrails, RAG-only product data |
| WhatsApp API rate limits | Low | Medium | Queue system, retry logic |
| Webhook downtimes | Low | Medium | Retry mechanism, logging |
| Data model changes mid-project | Medium | Medium | Alembic migrations, modular design |
| API key exposure | Low | Critical | .env only, never in code, .gitignore |
| Flutter APK size | Medium | Low | ProGuard, asset optimization |
| AI latency | Medium | Medium | Streaming responses, caching |