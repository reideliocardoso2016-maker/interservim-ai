# INTERSERVIM AI SALES AGENT — Database Design

## Entity Relationship Diagram (Conceptual)

```
User ──< Conversation >── Customer
 │                          │
 │                          ├──< Quote >──< QuoteItem >── Product
 │                          │                 │
 │                          ├──< FollowUp     │
 │                          │                 ├──< ProductImage
 │                          │                 │
 │                          └──< Message      ├──< Category
 │                                             │
 │                          MarketingCampaign ─┴──< MarketingContent
 │
 │                          KnowledgeDocument
```

## Entity Definitions

### User
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| name | VARCHAR(255) | NOT NULL | |
| email | VARCHAR(255) | UNIQUE, NOT NULL | |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hash |
| role | ENUM | NOT NULL | ADMIN, MANAGER, SALES_AGENT, VIEWER |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | NOT NULL | |
| updated_at | TIMESTAMP | NOT NULL | |

### Customer
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| name | VARCHAR(255) | NOT NULL | |
| phone | VARCHAR(50) | UNIQUE, NOT NULL | WhatsApp number |
| email | VARCHAR(255) | NULLABLE | |
| country | VARCHAR(100) | NULLABLE | |
| company | VARCHAR(255) | NULLABLE | |
| customer_type | ENUM | NULLABLE | IMPORTER, DISTRIBUTOR, RETAILER, OTHER |
| status | ENUM | NOT NULL, DEFAULT 'NEW' | NEW, CONTACTED, INTERESTED, QUOTE_SENT, NEGOTIATING, WON, LOST, FOLLOW_UP |
| notes | TEXT | NULLABLE | |
| last_contacted_at | TIMESTAMP | NULLABLE | |
| created_at | TIMESTAMP | NOT NULL | |
| updated_at | TIMESTAMP | NOT NULL | |
| deleted_at | TIMESTAMP | NULLABLE | Soft delete |

### Product
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| name | VARCHAR(255) | NOT NULL | |
| sku | VARCHAR(100) | UNIQUE | |
| category_id | UUID | FK → ProductCategory.id | |
| description | TEXT | NULLABLE | |
| brand | VARCHAR(255) | NULLABLE | |
| origin_country | VARCHAR(100) | NULLABLE | |
| unit_price | DECIMAL(12,2) | NOT NULL | |
| currency | VARCHAR(3) | DEFAULT 'USD' | |
| minimum_order_quantity | INTEGER | DEFAULT 1 | |
| packaging | VARCHAR(255) | NULLABLE | |
| availability_status | ENUM | DEFAULT 'AVAILABLE' | AVAILABLE, LOW_STOCK, OUT_OF_STOCK, DISCONTINUED |
| container_capacity | VARCHAR(100) | NULLABLE | |
| technical_information | JSONB | NULLABLE | Flexible specs |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | NOT NULL | |
| updated_at | TIMESTAMP | NOT NULL | |

### ProductCategory
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| name | VARCHAR(255) | NOT NULL, UNIQUE | |
| description | TEXT | NULLABLE | |
| parent_id | UUID | FK → self | Hierarchical |
| created_at | TIMESTAMP | NOT NULL | |

### ProductImage
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| product_id | UUID | FK → Product, NOT NULL | |
| url | VARCHAR(500) | NOT NULL | |
| type | ENUM | DEFAULT 'PRIMARY' | PRIMARY, GALLERY, DOCUMENT |
| created_at | TIMESTAMP | NOT NULL | |

### Conversation
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| customer_id | UUID | FK → Customer, NOT NULL | |
| channel | ENUM | NOT NULL | WHATSAPP, MANUAL, WEB |
| status | ENUM | NOT NULL, DEFAULT 'ACTIVE' | ACTIVE, PAUSED, CLOSED, HUMAN_HANDOFF |
| assigned_user_id | UUID | FK → User, NULLABLE | |
| ai_enabled | BOOLEAN | DEFAULT TRUE | |
| sales_stage | ENUM | DEFAULT 'LEAD' | LEAD, QUALIFIED, PRODUCT_INTEREST, QUOTE_REQUESTED, QUOTE_SENT, NEGOTIATION, CLOSED_WON, CLOSED_LOST |
| ai_context_summary | TEXT | NULLABLE | Compressed conversation summary |
| created_at | TIMESTAMP | NOT NULL | |
| updated_at | TIMESTAMP | NOT NULL | |

### Message
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| conversation_id | UUID | FK → Conversation, NOT NULL | |
| sender_type | ENUM | NOT NULL | CUSTOMER, AI_AGENT, HUMAN_AGENT |
| content | TEXT | NOT NULL | |
| message_type | ENUM | DEFAULT 'TEXT' | TEXT, IMAGE, DOCUMENT, VIDEO, AUDIO |
| intent | VARCHAR(50) | NULLABLE | Classified intent |
| external_message_id | VARCHAR(255) | NULLABLE | WhatsApp message ID |
| metadata | JSONB | NULLABLE | Additional data |
| created_at | TIMESTAMP | NOT NULL | |

### Quote
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| customer_id | UUID | FK → Customer, NOT NULL | |
| quote_number | VARCHAR(50) | UNIQUE, NOT NULL | Auto-generated |
| status | ENUM | NOT NULL, DEFAULT 'DRAFT' | DRAFT, SENT, ACCEPTED, REJECTED, EXPIRED |
| currency | VARCHAR(3) | DEFAULT 'USD' | |
| total | DECIMAL(14,2) | NOT NULL | |
| destination_country | VARCHAR(100) | NULLABLE | |
| destination_port | VARCHAR(100) | NULLABLE | |
| payment_terms | VARCHAR(255) | NULLABLE | |
| delivery_terms | VARCHAR(255) | NULLABLE | |
| valid_until | DATE | NULLABLE | |
| notes | TEXT | NULLABLE | |
| pdf_url | VARCHAR(500) | NULLABLE | Generated PDF |
| created_by | UUID | FK → User | |
| created_at | TIMESTAMP | NOT NULL | |
| updated_at | TIMESTAMP | NOT NULL | |

### QuoteItem
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| quote_id | UUID | FK → Quote, NOT NULL | |
| product_id | UUID | FK → Product, NOT NULL | |
| product_name | VARCHAR(255) | NOT NULL | Snapshot at quote time |
| sku | VARCHAR(100) | NULLABLE | |
| quantity | INTEGER | NOT NULL | |
| unit_price | DECIMAL(12,2) | NOT NULL | |
| subtotal | DECIMAL(14,2) | NOT NULL | |
| created_at | TIMESTAMP | NOT NULL | |

### FollowUp
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| customer_id | UUID | FK → Customer, NOT NULL | |
| conversation_id | UUID | FK → Conversation, NULLABLE | |
| type | ENUM | DEFAULT 'AUTOMATIC' | AUTOMATIC, MANUAL |
| scheduled_at | TIMESTAMP | NOT NULL | |
| status | ENUM | DEFAULT 'PENDING' | PENDING, SENT, CANCELLED |
| message | TEXT | NOT NULL | |
| executed_at | TIMESTAMP | NULLABLE | |
| created_at | TIMESTAMP | NOT NULL | |

### MarketingCampaign
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| name | VARCHAR(255) | NOT NULL | |
| objective | ENUM | NOT NULL | GENERATE_LEADS, PROMOTE_PRODUCT, GENERATE_SALES, PROMOTE_IMPORTATION, CREATE_URGENCY, REACTIVATE_CUSTOMERS |
| target_audience | VARCHAR(500) | NULLABLE | |
| status | ENUM | DEFAULT 'DRAFT' | DRAFT, ACTIVE, PAUSED, COMPLETED |
| created_by | UUID | FK → User | |
| created_at | TIMESTAMP | NOT NULL | |
| updated_at | TIMESTAMP | NOT NULL | |

### MarketingContent
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| campaign_id | UUID | FK → MarketingCampaign, NOT NULL | |
| content_type | ENUM | NOT NULL | WHATSAPP_STATUS, WHATSAPP_MESSAGE, INSTAGRAM_CAPTION, FACEBOOK_POST, COMMERCIAL_EMAIL, PRODUCT_ADVERTISEMENT, IMPORTATION_CAMPAIGN |
| language | VARCHAR(10) | DEFAULT 'ES' | |
| title | VARCHAR(500) | NULLABLE | |
| body | TEXT | NOT NULL | |
| call_to_action | VARCHAR(255) | NULLABLE | |
| media_url | VARCHAR(500) | NULLABLE | |
| tone | ENUM | DEFAULT 'PROFESSIONAL' | PROFESSIONAL, URGENT, COMMERCIAL |
| ai_generated | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMP | NOT NULL | |

### KnowledgeDocument
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| name | VARCHAR(255) | NOT NULL | |
| file_url | VARCHAR(500) | NOT NULL | |
| document_type | ENUM | NOT NULL | PDF, DOCX, XLSX, TXT |
| status | ENUM | DEFAULT 'PROCESSING' | PROCESSING, READY, ERROR |
| chunk_count | INTEGER | DEFAULT 0 | |
| created_at | TIMESTAMP | NOT NULL | |

### KnowledgeChunk
| Column | Type | Constraints | Notes |
|--------|------|------------|-------|
| id | UUID | PK | |
| document_id | UUID | FK → KnowledgeDocument, NOT NULL | |
| content | TEXT | NOT NULL | |
| chunk_index | INTEGER | NOT NULL | |
| embedding | VECTOR(1536) | NULLABLE | pgvector |
| created_at | TIMESTAMP | NOT NULL | |

## Indexes

| Table | Index | Columns | Type |
|-------|-------|---------|------|
| customer | idx_customer_phone | phone | UNIQUE |
| customer | idx_customer_status | status | BTREE |
| product | idx_product_sku | sku | UNIQUE |
| product | idx_product_category | category_id | BTREE |
| product | idx_product_availability | availability_status | BTREE |
| product | idx_product_price | unit_price | BTREE |
| conversation | idx_conv_customer | customer_id | BTREE |
| conversation | idx_conv_status | status | BTREE |
| conversation | idx_conv_assigned | assigned_user_id | BTREE |
| message | idx_msg_conversation | conversation_id | BTREE |
| message | idx_msg_created | created_at | BTREE |
| quote | idx_quote_customer | customer_id | BTREE |
| quote | idx_quote_status | status | BTREE |
| followup | idx_followup_scheduled | scheduled_at | BTREE |
| followup | idx_followup_status | status | BTREE |

## Conventions

- All tables use UUID primary keys
- All tables have `created_at` and `updated_at` timestamps
- Soft-delete via `deleted_at` timestamp where applicable
- `is_active` boolean for logical deactivation
- JSONB for flexible/future fields
- ENUMs for constrained string values
- All relationships use foreign keys with CASCADE or SET NULL as appropriate