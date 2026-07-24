# INTERSERVIM AI SALES AGENT — API Reference

## Base URL

- Development: `http://localhost:8000/api/v1`
- Production: Configurable via `API_BASE_URL` env var

## Authentication

All protected endpoints require:
```
Authorization: Bearer <access_token>
```

### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description"
  }
}
```

### Success Response Format
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

---

## Auth Endpoints

### POST /auth/register
Register a new user (ADMIN only).

**Request:**
```json
{
  "name": "string",
  "email": "string",
  "password": "string",
  "role": "SALES_AGENT"
}
```

### POST /auth/login
Obtain access and refresh tokens.

**Request:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### POST /auth/refresh
Get a new access token using refresh token.

**Request:**
```json
{
  "refresh_token": "string"
}
```

### GET /auth/me
Get current user profile.

---

## Product Endpoints

### GET /products
List products with filters and pagination.

**Query Parameters:**
- `search` — text search in name/description/sku
- `category_id` — filter by category
- `availability` — AVAILABLE, LOW_STOCK, OUT_OF_STOCK
- `min_price` / `max_price` — price range
- `currency` — filter by currency
- `page` (default: 1)
- `per_page` (default: 20)

### POST /products
Create a new product (MANAGER, ADMIN).

### GET /products/{id}
Get product details with images and category.

### PUT /products/{id}
Update product (MANAGER, ADMIN).

### DELETE /products/{id}
Soft-delete product (ADMIN only).

---

## Customer Endpoints

### GET /customers
List customers with filters.

**Query Parameters:**
- `search` — text search in name/phone/email/company
- `status` — filter by status
- `customer_type` — filter by type
- `country` — filter by country
- `page`, `per_page`

### POST /customers
Create a new customer.

### GET /customers/{id}
Get customer with conversations, quotes, follow-ups.

### PUT /customers/{id}
Update customer.

### DELETE /customers/{id}
Soft-delete customer (ADMIN).

---

## Conversation Endpoints

### GET /conversations
List conversations.

**Query Parameters:**
- `status` — ACTIVE, PAUSED, CLOSED, HUMAN_HANDOFF
- `customer_id`
- `assigned_user_id`
- `ai_enabled`
- `sales_stage`
- `page`, `per_page`

### POST /conversations
Create a conversation.

### GET /conversations/{id}
Get conversation with messages.

### PATCH /conversations/{id}/ai
Toggle AI on/off (MANAGER, ADMIN).

### PATCH /conversations/{id}/assign
Assign to human agent (MANAGER, ADMIN).

### PATCH /conversations/{id}/handoff
Request human handoff.

---

## Message Endpoints

### GET /conversations/{id}/messages
Get paginated messages for a conversation.

### POST /conversations/{id}/messages
Send a message (manual entry by human agent).

---

## Quote Endpoints

### GET /quotes
List quotes with filters.

**Query Parameters:**
- `customer_id`
- `status` — DRAFT, SENT, ACCEPTED, REJECTED, EXPIRED
- `page`, `per_page`

### POST /quotes
Create a new quote with items.

### GET /quotes/{id}
Get quote with items and customer.

### PUT /quotes/{id}
Update quote.

### DELETE /quotes/{id}
Delete quote.

### GET /quotes/{id}/pdf
Download quote as PDF.

---

## Webhook Endpoints (WhatsApp)

### GET /webhooks/whatsapp
WhatsApp webhook verification.

**Query Parameters:**
- `hub.mode`
- `hub.verify_token`
- `hub.challenge`

### POST /webhooks/whatsapp
Receive WhatsApp messages.

**Request:** Standard WhatsApp Cloud API payload.

---

## AI Endpoints

### POST /ai/classify
Classify message intent.

### POST /ai/generate
Generate AI response for a conversation.

### POST /ai/marketing
Generate marketing content.

**Request:**
```json
{
  "product_id": "uuid",
  "content_type": "WHATSAPP_STATUS",
  "objective": "PROMOTE_PRODUCT",
  "tone": "PROFESSIONAL",
  "language": "ES",
  "audience": "importers in Central America"
}
```

---

## Knowledge Base Endpoints

### POST /knowledge/upload
Upload a document (PDF, DOCX, XLSX, TXT).

**Request:** Multipart form-data with file.

### GET /knowledge/documents
List uploaded documents.

### DELETE /knowledge/documents/{id}
Delete document.

### GET /knowledge/search
Search knowledge base using RAG.

**Query Parameters:**
- `query` — search text
- `limit` — max results

---

## Marketing Campaign Endpoints

### GET /marketing/campaigns
List campaigns.

### POST /marketing/campaigns
Create campaign.

### GET /marketing/campaigns/{id}
Get campaign with contents.

### PUT /marketing/campaigns/{id}
Update campaign.

### POST /marketing/campaigns/{id}/generate
Generate AI content for campaign.

---

## Follow-Up Endpoints

### GET /followups
List follow-ups (filterable by status, date range).

### POST /followups
Schedule a follow-up.

### PATCH /followups/{id}
Update follow-up status.

---

## Analytics Endpoints

### GET /analytics/overview
Dashboard overview metrics.

### GET /analytics/conversations
Conversation statistics over time.

### GET /analytics/products
Most queried products.

### GET /analytics/sales
Sales funnel data.

---

## Endpoint Summary

| Method | Path | Auth | Roles |
|--------|------|------|-------|
| POST | /auth/register | JWT | ADMIN |
| POST | /auth/login | None | All |
| POST | /auth/refresh | None | All |
| GET | /auth/me | JWT | All authenticated |
| GET | /products | JWT | All authenticated |
| POST | /products | JWT | MANAGER, ADMIN |
| GET | /products/{id} | JWT | All authenticated |
| PUT | /products/{id} | JWT | MANAGER, ADMIN |
| DELETE | /products/{id} | JWT | ADMIN |
| GET | /customers | JWT | All authenticated |
| POST | /customers | JWT | All authenticated |
| GET | /customers/{id} | JWT | All authenticated |
| PUT | /customers/{id} | JWT | All authenticated |
| DELETE | /customers/{id} | JWT | ADMIN |
| GET | /conversations | JWT | All authenticated |
| POST | /conversations | JWT | All authenticated |
| GET | /conversations/{id} | JWT | All authenticated |
| PATCH | /conversations/{id}/ai | JWT | MANAGER, ADMIN |
| PATCH | /conversations/{id}/assign | JWT | MANAGER, ADMIN |
| PATCH | /conversations/{id}/handoff | JWT | SALES_AGENT, MANAGER, ADMIN |
| GET | /conversations/{id}/messages | JWT | All authenticated |
| POST | /conversations/{id}/messages | JWT | All authenticated |
| GET | /quotes | JWT | All authenticated |
| POST | /quotes | JWT | SALES_AGENT, MANAGER, ADMIN |
| GET | /quotes/{id} | JWT | All authenticated |
| PUT | /quotes/{id} | JWT | SALES_AGENT, MANAGER, ADMIN |
| DELETE | /quotes/{id} | JWT | ADMIN |
| GET | /quotes/{id}/pdf | JWT | All authenticated |
| GET | /webhooks/whatsapp | None | Public |
| POST | /webhooks/whatsapp | None | Public |
| POST | /ai/classify | JWT | All authenticated |
| POST | /ai/generate | JWT | All authenticated |
| POST | /ai/marketing | JWT | All authenticated |
| POST | /knowledge/upload | JWT | MANAGER, ADMIN |
| GET | /knowledge/documents | JWT | All authenticated |
| DELETE | /knowledge/documents/{id} | JWT | ADMIN |
| GET | /knowledge/search | JWT | All authenticated |
| GET | /marketing/campaigns | JWT | All authenticated |
| POST | /marketing/campaigns | JWT | MANAGER, ADMIN |
| GET | /marketing/campaigns/{id} | JWT | All authenticated |
| PUT | /marketing/campaigns/{id} | JWT | MANAGER, ADMIN |
| POST | /marketing/campaigns/{id}/generate | JWT | MANAGER, ADMIN |
| GET | /followups | JWT | All authenticated |
| POST | /followups | JWT | All authenticated |
| PATCH | /followups/{id} | JWT | All authenticated |
| GET | /analytics/overview | JWT | MANAGER, ADMIN |
| GET | /analytics/conversations | JWT | MANAGER, ADMIN |
| GET | /analytics/products | JWT | MANAGER, ADMIN |
| GET | /analytics/sales | JWT | MANAGER, ADMIN |