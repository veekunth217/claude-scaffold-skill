---
name: security
description: Application and server security — OWASP Top 10, WordPress hardening, server hardening (UFW/fail2ban), SSL/TLS, secrets management, WAF
version: 1.0.0
author: veekunth217
tags: [security, owasp, hardening, ssl, tls, waf, fail2ban, ufw, secrets, wordpress-security, xss, sqli]
platforms: [claude-code, cursor, codex]
---

# Security Skill

Application security, server hardening, and secrets management — from OWASP Top 10 mitigations to production WAF configuration.

**RULE: Security changes are high-impact. Always show what will change, explain the risk being mitigated, and wait for GO.**

> **🚧 Status: Stub — implementation pending**
>
> This reference skill has the structure but the snippet content is still being filled in
> (you'll see `<!-- TODO -->` placeholders below). It activates and tells Claude the topic
> exists, but won't yield deep snippets yet.
>
> **Want to help?** Pick any TODO, write the snippet, open a PR. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
> Each contribution moves the skill closer to "Ready" status.

---

## Capabilities

### OWASP Top 10
<!-- TODO: Injection (SQL, command, LDAP) — prevention patterns per language -->
<!-- TODO: Broken access control — authz checks, IDOR prevention -->
<!-- TODO: Cryptographic failures — hashing (bcrypt/argon2), encryption at rest -->
<!-- TODO: XSS — CSP headers, output encoding, DOMPurify -->
<!-- TODO: Security misconfiguration — headers audit, error message leakage -->
<!-- TODO: Vulnerable components — npm audit, pip-audit, Dependabot -->

### WordPress Hardening
<!-- TODO: DISALLOW_FILE_EDIT, disable XML-RPC, hide WP version -->
<!-- TODO: Block /wp-login.php by IP at Nginx level -->
<!-- TODO: User enumeration prevention (?author=1 block) -->
<!-- TODO: Database prefix, secrets in wp-config.php above webroot -->
<!-- TODO: File permission hardening (644 files, 755 dirs, 600 wp-config) -->

### Server Hardening (UFW / fail2ban)
<!-- TODO: UFW rules: default deny, SSH rate limiting -->
<!-- TODO: fail2ban jails: sshd, nginx-http-auth, wordpress -->
<!-- TODO: SSH hardening: key-only, disable root, port change, AllowUsers -->
<!-- TODO: Disable unused services, remove default accounts -->
<!-- TODO: Automatic security updates (unattended-upgrades) -->

### SSL/TLS Configuration
<!-- TODO: TLS 1.2+ only, disable TLS 1.0/1.1 -->
<!-- TODO: Cipher suite hardening (Mozilla SSL Config Generator) -->
<!-- TODO: HSTS header with preload, OCSP stapling -->
<!-- TODO: Certificate transparency, CAA DNS records -->

### Secrets Management
<!-- TODO: AWS Secrets Manager vs SSM Parameter Store — when to use each -->
<!-- TODO: Never in env files committed to git, never in Docker args -->
<!-- TODO: External Secrets Operator for Kubernetes -->
<!-- TODO: Secret rotation patterns, break-glass procedures -->

### WAF Configuration
<!-- TODO: AWS WAF rules: managed rule groups, rate limiting, geo-blocking -->
<!-- TODO: Nginx WAF (ModSecurity + OWASP Core Rule Set) -->
<!-- TODO: Cloudflare WAF rules, challenge vs block -->

---

## Quick Wins (apply to any server)

### fail2ban WordPress jail
```ini
# /etc/fail2ban/jail.local
[wordpress]
enabled  = true
filter   = wordpress
logpath  = /var/log/nginx/access.log
maxretry = 5
bantime  = 3600
findtime = 600

# /etc/fail2ban/filter.d/wordpress.conf
[Definition]
failregex = ^<HOST> .* "POST /wp-login.php
ignoreregex =
```

### Nginx security headers
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
server_tokens off;
```

### SSH hardening (/etc/ssh/sshd_config)
```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers [your-user]
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
```

<!-- TODO: Add full interactive workflows for each capability above -->
