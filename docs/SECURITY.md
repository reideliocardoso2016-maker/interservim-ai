# INTERSERVIM AI SALES AGENT — Security Policy

## 1. Authentication & Authorization

### JWT Token Strategy
- **Access Token**: Short-lived (1 hour), sent in Authorization header
- **Refresh Token**: Long-lived (7 days), stored securely in HTTP-only cookie or secure storage
- **Algorithm**: HS256 or RS256
- **Claims**: sub (user_id), role, exp, iat

### Password Policy
- Hashing algorithm: bcrypt (cost factor 12)
- Minimum length: 8 characters
- Password complexity: at least 1 uppercase, 1 lowercase, 1 digit

### Role-Based Access Control (RBAC)

| Permission | ADMIN | MANAGER | SALES_AGENT | VIEWER |
|------------|-------|---------|-------------|--------|
| Manage users | ✅ | ❌ | ❌ | ❌ |
| Manage products | ✅ | ✅ | ❌ | ❌ |
| View products | ✅ | ✅ | ✅ | ✅ |
| Manage customers | ✅ | ✅ | ✅ | ❌ |
| View customers | ✅ | ✅ | ✅ | ✅ |
| Manage conversations | ✅ | ✅ | ✅ | ❌ |
| View conversations | ✅ | ✅ | ✅ | ✅ |
| Send messages | ✅ | ✅ | ✅ | ❌ |
| Manage quotes | ✅ | ✅ | ✅ | ❌ |
| View quotes | ✅ | ✅ | ✅ | ✅ |
| Manage AI settings | ✅ | ✅ | ❌ | ❌ |
| View analytics | ✅ | ✅ | ✅ | ✅ |
| Manage knowledge base | ✅ | ✅ | ❌ | ❌ |
| Manage campaigns | ✅ | ✅ | ❌ | ❌ |

## 2. API Security

### Headers
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-XSS-Protection: 1; mode=block
```

### CORS
- Restricted to known origins (mobile app, admin domain)
- No wildcard in production

### Rate Limiting
- General API: 100 requests/minute per IP
- Auth endpoints: 10 requests/minute per IP
- AI generation: 30 requests/minute per user
- Webhook: 200 requests/minute per IP

### Input Validation
- All inputs validated via Pydantic schemas
- SQL injection prevention via SQLAlchemy parameterized queries
- No raw SQL concatenation

## 3. Data Protection

### Secrets Management
- **NEVER** write API keys, passwords, or tokens in code
- All secrets via environment variables (.env file)
- .env.example committed (with placeholder values)
- .env in .gitignore

### Environment Variables (Sensitive)
```
AI_API_KEY
WHATSAPP_ACCESS_TOKEN
WHATSAPP_VERIFY_TOKEN
JWT_SECRET
DATABASE_URL
REDIS_URL
```

### Database
- Connection strings use `postgresql://user:password@host:port/db` format
- Passwords in connection strings are read from env, never hardcoded
- SSL recommended for production database connections

### WhatsApp Integration
- Official WhatsApp Cloud API only (no unofficial APIs)
- Webhook verify token checked on every GET request
- Request signature verification on incoming webhooks

## 4. Logging Security

### DO Log
- Request IDs
- User actions (non-sensitive)
- Error types and codes
- Webhook reception events
- AI response generation status
- Performance metrics

### DO NOT Log
- API keys
- Passwords or password hashes
- JWT tokens (full)
- Credit card information
- Personal sensitive data (full)
- WhatsApp message content in plain text (anonymize)

## 5. Mobile App Security

- **Token Storage**: Use flutter_secure_storage (encrypted storage)
- **No secrets in APK**: API endpoints are configurable; no hardcoded keys
- **Certificate Pinning**: Recommended for production
- **ProGuard**: Enable code obfuscation and minification for release builds
- **Root Detection**: Optional, for sensitive operations

## 6. Network Security

- All API traffic over HTTPS (TLS 1.2+)
- Webhook endpoints use signature verification
- Internal services (Redis, PostgreSQL) not exposed to public internet
- Docker network isolation for services

## 7. Incident Response

### If a secret is leaked:
1. Revoke the compromised token/key immediately
2. Rotate all affected credentials
3. Audit logs for unauthorized access
4. Notify affected parties if necessary

### If unauthorized access is detected:
1. Block the offending IP/token
2. Preserve logs for investigation
3. Determine scope of breach
4. Patch the vulnerability
5. Document the incident

## 8. Compliance Considerations

- GDPR: Right to access, rectification, erasure of personal data
- Data retention policies configurable
- Export functionality for user data
- Consent tracking for marketing communications

## 9. Security Testing

- Automated vulnerability scanning in CI/CD
- Dependency scanning for known CVEs
- Regular penetration testing (quarterly recommended)
- Code review for all security-sensitive changes