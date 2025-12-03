# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

We take the security of Titan Platform seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do NOT create a public GitHub issue

Security vulnerabilities should be reported privately to prevent exploitation.

### 2. Report via Email

Send details to: **[Project maintainer email - replace with yours]**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Expected Response Time

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 24-48 hours
  - High: 7 days
  - Medium: 14 days
  - Low: 30 days

---

## Security Best Practices

### API Key Management

**✅ DO:**
- Store API keys in `.env` file  
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate keys regularly
- Use different keys for dev/production

**❌ DON'T:**
- Commit `.env` to git
- Hardcode keys in source code
- Share keys in public forums
- Use production keys in development

### File Permissions

```bash
# Secure .env file (Linux/Mac)
chmod 600 .env

# Secure Memory Bank data
chmod 700 services/memory-bank/chroma_data/

# Secure logs
chmod 755 logs/
```

### Network Security

- Use HTTPS for all external API calls
- Validate SSL certificates
- Implement rate limiting
- Use firewall rules in production

### Data Protection

**User Data** (in Memory Bank):
- Stored locally in ChromaDB
- No cloud transmission by default
- User consent required for data collection
- GDPR-compliant data retention (90 days default)
- Opt-in for analytics

**Market Data**:
- Cached locally from yfinance
- Public data only
- No PII (Personally Identifiable Information)

### Input Validation

All user inputs are validated:
- Tool parameters type-checked with Pydantic
- SQL injection prevention (no raw SQL)
- Command injection prevention (no `os.system` with user input)
- File path validation (no directory traversal)

---

## Known Security Considerations

### 1. API Rate Limits

**Issue**: Excessive API calls may trigger rate limits or incur costs.

**Mitigation**:
- Configure `API_REQUESTS_PER_DAY` and `API_REQUESTS_PER_MINUTE` in `.env`
- Enable caching (`CACHE_ENABLED=true`)
- Monitor dashboard for API usage

### 2. LLM Prompt Injection

**Issue**: Malicious prompts could manipulate agent behavior.

**Mitigation**:
- Use FactChecker agent for claim verification
- ChiefRiskOfficer has VETO power
- Input sanitization in tools
- User queries logged for audit

### 3. Data Persistence

**Issue**: User sensitive data stored in Memory Bank.

**Mitigation**:
- Local storage only (no cloud by default)
- Encryption at rest (optional, user-configured)
- Data compaction removes old entries (90 days)
- Backup encryption recommended

### 4. Third-Party Dependencies

**Issue**: Vulnerabilities in libraries (yfinance, chromadb, etc.)

**Mitigation**:
- Regular `pip audit` checks
- Keep dependencies updated
- Pin versions in `requirements.txt`
- Monitor security advisories

---

## Security Features

### ✅ Implemented

- [x] Environment variable configuration (.env)
- [x] Input validation (Pydantic schemas)
- [x] Logging with PII redaction
- [x] Risk VETO system
- [x] Local data storage (Memory Bank)
- [x] File permission recommendations
- [x] Rate limiting configuration

### 🔄 Planned (Future)

- [ ] Audit logging for all agent decisions
- [ ] Encryption at rest for Memory Bank
- [ ] Multi-user authentication (RBAC)
- [ ] API key rotation automation
- [ ] Security scanning in CI/CD
- [ ] Penetration testing

---

## Compliance

### GDPR (EU)

**Right to Access**: Users can export Memory Bank data  
**Right to Deletion**: Users can delete their profile  
**Data Minimization**: Only necessary data stored  
**Consent**: Explicit opt-in required for data collection

### CCPA (California)

**Do Not Sell**: No user data sold to third parties  
**Transparency**: Clear documentation of data usage  
**Access & Deletion**: Full user control over data

---

## Deployment Security

### Production Checklist

- [ ] Change default `.env` values
- [ ] Use strong API keys
- [ ] Enable HTTPS for web interface
- [ ] Set firewall rules (only necessary ports)
- [ ] Disable debug mode (`DEBUG_MODE=false`)
- [ ] Use production log level (`LOG_LEVEL=WARNING`)
- [ ] Regular backups of Memory Bank
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated
- [ ] Review access controls

### Docker Security

```dockerfile
# Use non-root user
USER appuser

# Read-only root filesystem
RUN chmod 755 /app

# Drop capabilities
USER 1000:1000
```

---

## Incident Response

### If a Security Breach Occurs:

1. **Immediate Actions**:
   - Stop the affected service
   - Preserve logs for forensics
   - Notify affected users (if PII exposed)

2. **Investigation**:
   - Analyze logs (`logs/titan-*.log`)
   - Check Memory Bank access
   - Review API usage patterns

3. **Remediation**:
   - Patch vulnerability
   - Rotate compromised keys
   - Reset affected user data
   - Update documentation

4. **Post-Incident**:
   - Root cause analysis
   - Update security measures
   - Notify community (if appropriate)
   - Publish security advisory

---

## Security Audit History

| Date | Auditor | Findings | Status |
|------|---------|----------|--------|
| Dec 2024 | Internal | Initial security review | ✅ Resolved |
| - | - | - | - |

---

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google AI Safety Best Practices](https://ai.google/responsibility/responsible-ai-practices/)
- [ChromaDB Security](https://docs.trychroma.com/)
- [Python Security Best Practices](https://python.land/cybersecurity)

---

## Contact

For security concerns:  
**Email**: [Your security contact email]  
**Response Time**: Within 48 hours

For general questions:  
**GitHub Issues**: https://github.com/Devvekariya711/titan-platform/issues

---

**Last Updated**: December 2024  
**Version**: 1.0.0
