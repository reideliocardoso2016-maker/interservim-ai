# INTERSERVIM AI SALES AGENT — Architecture

## 1. System Overview

Interservim AI Sales Agent is a modular sales platform powered by artificial intelligence, designed to manage WhatsApp-based commercial conversations, product catalogs, customer relationships, quotes, and marketing campaigns for import/export businesses.

The system is composed of three main layers:

- **Mobile App** (Flutter/Dart) — Android APK, future iOS/Web
- **Backend API** (Python/FastAPI) — RESTful services, AI engine, WhatsApp integration
- **Infrastructure** (Docker/PostgreSQL/Redis) — Data persistence, caching, async tasks

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   WhatsApp Cloud API                     │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Webhooks
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Backend API (FastAPI / Python)               │
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │ Auth     │ │ Products │ │ CRM      │ │ Quotes     │ │
│  │ Module   │ │ Module   │ │ Module   │ │ Module     │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │ AI Agent │ │ WhatsApp │ │ Marketing│ │ Knowledge  │ │
│  │ Engine   │ │ Gateway  │ │ Studio   │ │ Base       │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP REST
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Flutter Mobile App (Android APK)            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │ Dashboard│ │ Chats    │ │ CRM      │ │ Products   │ │
│  │ Screen   │ │ Screen   │ │ Screen   │ │ Screen     │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │ Quotes   │ │Marketing │ │ Analytics│ │ Settings   │ │
│  │ Screen   │ │ Studio   │ │ Screen   │ │ Screen     │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘ │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│              Infrastructure Layer                        │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────┐  │
│  │ PostgreSQL │  │   Redis    │  │   Celery Worker  │  │
│  └────────────┘  └────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 3. Component Breakdown

### 3.1 Backend API (`apps/backend/api/`)

| Module | Path | Responsibility |
|--------|------|---------------|
| Auth | `app/auth/` | JWT, register, login, refresh, roles |
| Products | `app/products/` | CRUD, search, filters, categories |
| CRM | `app/customers/` | Customers, conversations, messages |
| Quotes | `app/quotes/` | Quote CRUD, PDF generation |
| AI Agent | `app/ai/` | LLM provider, intent classification, response generation, sales engine |
| WhatsApp | `app/integrations/whatsapp/` | Webhooks, message sending, status callbacks |
| Marketing | `app/marketing/` | AI content generation for campaigns |
| Knowledge | `app/knowledge/` | Document upload, text extraction, RAG |
| Analytics | `app/analytics/` | Metrics, charts, KPIs |
| FollowUps | `app/followups/` | Scheduled tasks, automatic follow-ups |

### 3.2 Mobile App (`apps/mobile/flutter_app/`)

| Screen | Route | Purpose |
|--------|-------|---------|
| Splash | `/` | App initialization |
| Login | `/login` | JWT authentication |
| Dashboard | `/dashboard` | KPIs, recent activity |
| Conversations | `/conversations` | Chat list |
| ConversationDetail | `/conversations/:id` | Chat view |
| Customers | `/customers` | Customer list |
| CustomerDetail | `/customers/:id` | Customer profile |
| Products | `/products` | Product catalog |
| ProductDetail | `/products/:id` | Product details |
| Quotes | `/quotes` | Quote list |
| QuoteDetail | `/quotes/:id` | Quote PDF view |
| MarketingStudio | `/marketing` | AI content generation |
| WhatsAppStatus | `/marketing/status` | WhatsApp status creator |
| KnowledgeBase | `/knowledge` | Document management |
| Analytics | `/analytics` | Charts and metrics |
| Settings | `/settings` | Profile, config |

### 3.3 Shared Packages (`packages/`)

| Package | Content |
|---------|---------|
| `shared_models` | Pydantic/DTO models shared between backend and mobile |
| `shared_constants` | Enums, roles, states, error codes |
| `shared_utils` | Validation helpers, date utils, formatting |

## 4. Data Flow — WhatsApp Message Cycle

```
1. Customer sends message via WhatsApp
2. WhatsApp Cloud API sends POST to /webhooks/whatsapp
3. Webhook verifies signature, parses message
4. Customer is identified or created in DB
5. Message is saved in conversations table
6. Intent is classified using AI (or rule-based fallback)
7. Conversation context is retrieved (last N messages, customer profile, sales stage)
8. If product-related: product catalog is queried via vector or keyword search
9. AI generates response using:
   - Conversation context
   - Product data
   - Knowledge base (RAG)
   - Sales stage
   - Guardrails
10. AI response is saved in messages table
11. Response is sent via WhatsApp API
12. Sales stage is updated if applicable
13. Follow-up task is scheduled if needed
```

## 5. Security Architecture

- JWT with access + refresh tokens
- Password hashing via bcrypt
- Role-based access control (RBAC): ADMIN, MANAGER, SALES_AGENT, VIEWER
- WhatsApp webhook signature verification
- API rate limiting
- CORS configuration
- Input validation via Pydantic
- No secrets in code; all via environment variables
- Structured logging without sensitive data

## 6. AI Architecture

```
┌───────────────────────────────────────────────┐
│                AIProvider Interface             │
│  + generate_response(context, messages)        │
│  + classify_intent(message)                     │
│  + generate_marketing_content(params)           │
└──────────────────┬────────────────────────────┘
                   │ implements
         ┌─────────┴──────────┐
         ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│  OpenAIProvider  │  │  AnthropicProvider│
│  (GPT-4o, etc)  │  │  (Claude, etc)  │
└─────────────────┘  └─────────────────┘
         │                    │
         └─────────┬──────────┘
                   ▼
┌───────────────────────────────────────────────┐
│           Response Pipeline                    │
│                                                │
│  Intent → Context → Products → RAG → Prompt   │
│  → LLM Call → Guardrails → Response           │
└───────────────────────────────────────────────┘
```

## 7. Technology Stack

| Component | Technology |
|-----------|-----------|
| Mobile Framework | Flutter 3.x + Dart |
| Mobile State | Riverpod |
| Mobile Routing | GoRouter |
| Mobile HTTP | Dio |
| Mobile Models | Freezed + JSON Serializable |
| Backend Framework | Python 3.12+ / FastAPI |
| Backend Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Database | PostgreSQL 15+ |
| Cache / Queue | Redis 7+ |
| Async Tasks | Celery / ARQ |
| Auth | JWT (python-jose / PyJWT) |
| AI Providers | OpenAI / Anthropic / configurable |
| WhatsApp | WhatsApp Cloud API (official) |
| Containers | Docker + Docker Compose |
| Testing | pytest (backend) / flutter_test (mobile) |

## 8. Deployment Strategy

- Docker Compose for development
- Docker stack / Kubernetes for production
- Environment-specific configuration via .env files
- CI/CD pipeline for automated testing and building
- APK generation via Flutter build commands