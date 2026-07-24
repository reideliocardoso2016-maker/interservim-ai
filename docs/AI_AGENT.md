# INTERSERVIM AI SALES AGENT — AI Agent Specification

## 1. Agent Persona

The AI agent is the virtual commercial agent of InterServim-SL. It must embody the following characteristics:

**Identity:**
- Name: InterServim AI Sales Agent
- Company: InterServim-SL
- Role: Virtual commercial agent specializing in import/export products

**Personality Traits:**
- Professional but warm
- Clear and direct
- Commercially oriented
- Proactive but not pushy
- Honest and transparent
- Patient with customer questions

**Communication Style:**
- Natural, conversational Spanish (or configured language)
- Avoids robotic or overly formal language
- Uses appropriate business terminology
- Matches the customer's communication tone

**Core Rules:**
1. NEVER invent product information, prices, availability, or certifications
2. ONLY use information from the product database or knowledge base
3. If unsure, state clearly and offer to connect with a human agent
4. Always steer the conversation toward a commercial action
5. Do not bombard the customer with too many questions at once

## 2. Intent Classification

### 2.1 Intent Categories

| Intent | Trigger Examples | Priority |
|--------|-----------------|----------|
| GREETING | "Hola", "Buenos días", "Hi" | Low |
| PRODUCT_INQUIRY | "¿Tienen...?", "What products...", "Busco..." | High |
| PRICE_REQUEST | "¿Cuánto cuesta?", "Price of...", "Precio" | High |
| QUOTE_REQUEST | "Cotización", "Quotation", "Quote please" | High |
| AVAILABILITY_REQUEST | "¿Tienen stock?", "Available?", "Disponibilidad" | High |
| IMPORTATION_REQUEST | "Quiero importar", "Import to..." | High |
| LOGISTICS_QUESTION | "Shipping", "Transporte", "¿Cómo envían?" | Medium |
| PAYMENT_QUESTION | "Payment terms", "Formas de pago" | Medium |
| QUALITY_QUESTION | "Quality", "Calidad", "Certificaciones" | Medium |
| CERTIFICATE_QUESTION | "Certificados", "Certifications" | Medium |
| NEGOTIATION | "Descuento", "Better price", "Negocio" | High |
| FOLLOW_UP | "¿Me recuerdas?", "Following up" | Medium |
| COMPLAINT | "Problema", "Queja", "Complaint" | Critical |
| HUMAN_AGENT_REQUEST | "Agente humano", "Persona real", "Hablar con alguien" | Critical |
| OTHER | Unclear or out-of-scope | Low |

### 2.2 Classification Method
- Primary: AI-powered classification via LLM
- Fallback: Keyword-based regex classification
- Storage: Each message's classified intent is saved in the `intent` column

## 3. Conversation Memory

### 3.1 Context Structure
```python
{
    "conversation_id": "uuid",
    "customer": {
        "name": "string",
        "country": "string",
        "company": "string",
        "status": "string",
        "customer_type": "string"
    },
    "recent_messages": [  # Last 10 messages
        {"role": "customer|agent", "content": "string"}
    ],
    "summary": "string",  # AI-generated conversation summary
    "mentioned_products": ["product_id", ...],
    "sales_stage": "LEAD|QUALIFIED|...",
    "pending_info": {  # Information being collected
        "product": None,
        "quantity": None,
        "destination_country": None,
        "destination_port": None
    }
}
```

### 3.2 Memory Limits
- Recent messages: Last 10 (configurable)
- Summary: Regenerated every 20 messages
- Context window: Maximum ~4000 tokens for AI calls
- Old messages: Summarized and stored in `ai_context_summary`

## 4. Sales Funnel

### 4.1 Stages

```
LEAD → QUALIFIED → PRODUCT_INTEREST → QUOTE_REQUESTED
→ QUOTE_SENT → NEGOTIATION → CLOSED_WON
                                  → CLOSED_LOST
```

### 4.2 Stage Detection Triggers

| Stage | Trigger |
|-------|---------|
| LEAD | First message received |
| QUALIFIED | Customer provides company/country/needs |
| PRODUCT_INTEREST | Customer asks about specific products |
| QUOTE_REQUESTED | Customer asks for a quote |
| QUOTE_SENT | Quote is generated and sent |
| NEGOTIATION | Customer discusses price/terms |
| CLOSED_WON | Customer confirms purchase |
| CLOSED_LOST | Customer declines or goes silent |

### 4.3 Stage Transition Rules
- Automatic: AI detects and updates stage based on conversation
- Manual: Sales agent can override stage
- Rollback: Allowed (e.g., NEGOTIATION → QUOTE_REQUESTED)

## 5. Response Generation Pipeline

```
1. Receive message
2. Classify intent
3. Retrieve conversation context
4. If product-related: query product database
5. If knowledge needed: search knowledge base (RAG)
6. Determine current sales stage
7. Build system prompt with persona + context + rules
8. Call AI provider
9. Apply guardrails (hallucination check, data verification)
10. Save response
11. Update sales stage if applicable
12. Send response via WhatsApp
13. Schedule follow-up if appropriate
```

## 6. RAG (Retrieval-Augmented Generation)

### 6.1 Knowledge Sources
- Product catalog (database)
- Knowledge documents (uploaded PDFs, DOCX, etc.)
- Company information (configured in prompts)

### 6.2 Retrieval Process
1. User query is embedded (if using vector search) or keyword-processed
2. Relevant chunks are retrieved from vector store
3. Retrieved context is injected into the AI prompt
4. AI generates response using retrieved context only

### 6.3 Vector Store Interface
```python
class VectorStore:
    async def search(self, query: str, limit: int = 5) -> list[Chunk]:
        ...
    async def add_document(self, chunks: list[Chunk]):
        ...
    async def delete_document(self, document_id: str):
        ...
```

Configurable backends: pgvector (PostgreSQL), ChromaDB, Pinecone, etc.

## 7. Safety Guardrails

### 7.1 What the Agent MUST NOT Do
- Invent product data (price, availability, certifications)
- Promise delivery times
- Confirm unverified stock levels
- Share confidential business information
- Process payments
- Collect sensitive personal data (ID numbers, bank details)
- Engage in offensive or inappropriate conversations

### 7.2 Guardrail Implementation
```python
class SafetyGuardrails:
    async def check_response(self, response: str, context: dict) -> bool:
        # Check for invented data
        # Check for prohibited topics
        # Check for hallucinations about specific products
        # Return True if safe, False if needs rewrite/human review
```

### 7.3 Violation Handling
- If guardrails detect a problem: rewrite the response
- If repeated violations: flag for human review
- If critical violation: disable AI for that conversation

## 8. Marketing Content Generation

### 8.1 Content Types
- WhatsApp Status (text + CTA)
- WhatsApp Message (direct or broadcast)
- Instagram Caption
- Facebook Post
- Commercial Email
- Product Advertisement
- Importation Campaign

### 8.2 Tones
- Professional
- Urgent
- Commercial
- Friendly

### 8.3 Generation Parameters
```python
{
    "product_id": "uuid",
    "content_type": "WHATSAPP_STATUS",
    "objective": "PROMOTE_PRODUCT",
    "tone": "PROFESSIONAL",
    "language": "ES",
    "audience": "importers in Central America",
    "call_to_action": "SOLICITA_INFORMACION"
}
```

### 8.4 Call-to-Action Options
- SOLICITA_INFORMACION (Request information)
- SOLICITA_COTIZACION (Request quote)
- ESCRIBENOS_AHORA (Write us now)
- CONSULTA_DISPONIBILIDAD (Check availability)
- PREGUNTA_PRECIOS_MAYORISTAS (Ask about wholesale prices)

## 9. Provider Abstraction

### 9.1 Interface
```python
class AIProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        system_prompt: str,
        messages: list[dict],
        temperature: float = 0.7
    ) -> str:
        ...

    @abstractmethod
    async def classify_intent(
        self,
        message: str,
        conversation_context: dict
    ) -> IntentResult:
        ...

    @abstractmethod
    async def generate_marketing_content(
        self,
        params: MarketingParams
    ) -> MarketingContent:
        ...
```

### 9.2 Supported Providers
- OpenAI (GPT-4o, GPT-4, GPT-3.5)
- Anthropic (Claude 3 Opus, Sonnet, Haiku)
- Extensible via `AI_PROVIDER` environment variable

## 10. Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| AI_PROVIDER | LLM provider name | "openai" |
| AI_API_KEY | API key for LLM provider | - |
| AI_MODEL | Model name | "gpt-4o" |
| AI_TEMPERATURE | Response creativity | 0.7 |
| AI_MAX_TOKENS | Max tokens per response | 1024 |
| AI_CONTEXT_MESSAGES | Recent messages to include | 10 |
| AI_SUMMARY_INTERVAL | Messages between summaries | 20 |