# 📡 API Documentation - SentinelX SOC

## Visão Geral

A SentinelX SOC fornece uma API REST para integração com sistemas externos. Todas as respostas são em JSON.

**Base URL**: `http://127.0.0.1:5050/api/v1`

---

## Autenticação

Todos os endpoints (exceto `/auth/login`) requerem um token JWT no header `Authorization`.

```bash
Authorization: Bearer <seu-token-jwt>
```

---

## Endpoints

### 1. Autenticação

#### POST `/auth/login`
Realiza login e retorna token JWT.

**Request**:
```json
{
  "username": "admin",
  "password": "sua-senha"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "admin",
    "role": "administrator"
  }
}
```

**Erros**:
- `401 Unauthorized` - Credenciais inválidas
- `400 Bad Request` - Dados faltando

---

### 2. Análise de Email

#### POST `/email/analyze`
Analisa headers de email para detectar anomalias.

**Request**:
```json
{
  "header": "Return-Path: <user@example.com>\nReceived: from server.com\n..."
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "risk_score": 65,
    "severity": "ALTO",
    "spf_status": "fail",
    "dkim_status": "pass",
    "dmarc_status": "fail",
    "origin_ip": "192.168.1.1",
    "origin_country": "US",
    "suspicious_patterns": [
      "SPF validation failed",
      "DMARC validation failed"
    ]
  }
}
```

**Erros**:
- `400 Bad Request` - Header inválido
- `401 Unauthorized` - Token não autenticado
- `429 Too Many Requests` - Rate limit excedido

---

### 3. Análise de URL

#### POST `/url/analyze`
Escaneia URL para detectar malware e phishing.

**Request**:
```json
{
  "url": "http://example-paypal-verify.com"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "url": "http://example-paypal-verify.com",
    "domain": "example-paypal-verify.com",
    "risk_score": 85,
    "severity": "CRÍTICO",
    "typosquatting_detected": true,
    "similar_domains": [
      {
        "domain": "paypal.com",
        "similarity": 0.92
      }
    ],
    "ssl_certificate": {
      "valid": false,
      "expires": "2023-01-15"
    },
    "virustotal": {
      "malicious": 12,
      "suspicious": 5,
      "undetected": 45
    }
  }
}
```

**Erros**:
- `400 Bad Request` - URL inválida
- `401 Unauthorized` - Token não autenticado
- `429 Too Many Requests` - Rate limit excedido

---

### 4. IOCs (Indicadores de Compromisso)

#### GET `/iocs`
Lista todos os IOCs registrados.

**Parameters**:
- `type` (opcional): `domain`, `ip`, `hash`, `email`
- `limit` (opcional): Número máximo de resultados (padrão: 100)
- `offset` (opcional): Número de resultados a pular (padrão: 0)
- `days` (opcional): Últimos N dias (padrão: 30)

**Request**:
```bash
GET /iocs?type=domain&limit=50&days=30
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": "IOC_001",
      "type": "domain",
      "value": "malware-c2.com",
      "risk_score": 95,
      "detected_by": "email_analyzer",
      "first_seen": "2026-05-10T14:30:00Z",
      "last_seen": "2026-05-13T10:15:00Z",
      "count": 25
    },
    {
      "id": "IOC_002",
      "type": "domain",
      "value": "phishing-site.ru",
      "risk_score": 88,
      "detected_by": "url_scanner",
      "first_seen": "2026-05-11T09:20:00Z",
      "last_seen": "2026-05-13T08:45:00Z",
      "count": 12
    }
  ],
  "total": 145,
  "limit": 50,
  "offset": 0
}
```

#### POST `/iocs/register`
Registra um novo IOC.

**Request**:
```json
{
  "type": "domain",
  "value": "new-malware-domain.com",
  "risk_score": 90,
  "source": "manual_submission"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "data": {
    "id": "IOC_003",
    "type": "domain",
    "value": "new-malware-domain.com",
    "risk_score": 90,
    "created_at": "2026-05-13T11:30:00Z"
  }
}
```

#### DELETE `/iocs/{id}`
Deleta um IOC.

**Response** (200 OK):
```json
{
  "success": true,
  "message": "IOC deletado com sucesso"
}
```

---

### 5. Campanhas

#### GET `/campaigns`
Lista campanhas de ataque detectadas.

**Parameters**:
- `limit` (opcional): Número máximo de resultados
- `offset` (opcional): Número de resultados a pular
- `status` (opcional): `active`, `inactive`, `resolved`

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": "CAMPAIGN_001",
      "name": "Operation Stealth",
      "type": "phishing",
      "status": "active",
      "severity": "CRÍTICO",
      "indicators_count": 45,
      "first_seen": "2026-05-01T00:00:00Z",
      "last_seen": "2026-05-13T10:15:00Z",
      "targets": ["finance", "healthcare"],
      "actors": ["suspected-APT-28"]
    }
  ],
  "total": 5
}
```

#### GET `/campaigns/{id}`
Obtém detalhes de uma campanha específica.

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "CAMPAIGN_001",
    "name": "Operation Stealth",
    "type": "phishing",
    "status": "active",
    "severity": "CRÍTICO",
    "indicators": [
      {
        "type": "domain",
        "value": "fake-bank.com",
        "count": 23
      },
      {
        "type": "ip",
        "value": "192.168.1.100",
        "count": 15
      }
    ],
    "timeline": [
      {
        "date": "2026-05-01",
        "count": 5
      },
      {
        "date": "2026-05-02",
        "count": 8
      }
    ]
  }
}
```

---

### 6. Alertas

#### GET `/alerts`
Lista alertas gerados.

**Parameters**:
- `severity` (opcional): `CRÍTICO`, `ALTO`, `MÉDIO`, `BAIXO`
- `limit` (opcional): Número máximo de resultados
- `start_date` (opcional): Data inicial (YYYY-MM-DD)
- `end_date` (opcional): Data final (YYYY-MM-DD)

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": "ALERT_001",
      "timestamp": "2026-05-13T10:15:00Z",
      "type": "email",
      "severity": "CRÍTICO",
      "risk_score": 85,
      "subject": "Suspicious email from fake@bank.com",
      "details": {
        "sender": "fake@bank.com",
        "recipient": "user@company.com",
        "spf_status": "fail"
      },
      "action_taken": "blocked",
      "status": "resolved"
    }
  ],
  "total": 156,
  "unread_count": 12
}
```

#### PATCH `/alerts/{id}`
Marca um alerta como lido/resolvido.

**Request**:
```json
{
  "status": "resolved",
  "notes": "Falso positivo - remetente é legítimo"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": "ALERT_001",
    "status": "resolved",
    "updated_at": "2026-05-13T11:30:00Z"
  }
}
```

---

### 7. Bloqueios

#### POST `/blocking/block-domain`
Bloqueia um domínio no firewall.

**Request**:
```json
{
  "domain": "malware-domain.com",
  "reason": "Known phishing domain",
  "duration_days": 30
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "domain": "malware-domain.com",
    "blocked_at": "2026-05-13T11:30:00Z",
    "expires_at": "2026-06-12T11:30:00Z",
    "firewall_response": "Domain blocked successfully"
  }
}
```

#### POST `/blocking/block-ip`
Bloqueia um IP no firewall.

**Request**:
```json
{
  "ip": "192.168.100.50",
  "reason": "Brute force attack detected",
  "duration_days": 7
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "ip": "192.168.100.50",
    "blocked_at": "2026-05-13T11:30:00Z",
    "expires_at": "2026-05-20T11:30:00Z",
    "firewall_response": "IP blocked successfully"
  }
}
```

---

### 8. Relatórios

#### GET `/reports/summary`
Obtém relatório resumido de segurança.

**Parameters**:
- `days` (opcional): Últimos N dias (padrão: 30)

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "period": "last_30_days",
    "total_emails_analyzed": 2450,
    "total_urls_scanned": 1890,
    "total_alerts": 156,
    "critical_alerts": 12,
    "high_alerts": 34,
    "domains_blocked": 45,
    "ips_blocked": 23,
    "campaigns_detected": 5,
    "top_threats": [
      {
        "type": "phishing",
        "count": 67
      },
      {
        "type": "malware",
        "count": 34
      }
    ]
  }
}
```

#### GET `/reports/export`
Exporta relatório em formato especificado.

**Parameters**:
- `format`: `json`, `csv`, `pdf` (obrigatório)
- `days` (opcional): Últimos N dias (padrão: 30)

**Response**:
Arquivo baixado em formato especificado.

---

## Códigos de Resposta HTTP

| Código | Significado |
|--------|------------|
| 200 | OK - Sucesso |
| 201 | Created - Recurso criado |
| 204 | No Content - Sem conteúdo |
| 400 | Bad Request - Dados inválidos |
| 401 | Unauthorized - Não autenticado |
| 403 | Forbidden - Sem permissão |
| 404 | Not Found - Recurso não encontrado |
| 429 | Too Many Requests - Rate limit excedido |
| 500 | Internal Server Error - Erro do servidor |

---

## Rate Limiting

- **Limite**: 100 requests por minuto
- **Header Response**: `X-RateLimit-Remaining: 45`
- **Erro**: `429 Too Many Requests` quando excedido

---

## Exemplos com cURL

### Login
```bash
curl -X POST http://127.0.0.1:5050/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "senha"
  }'
```

### Analisar Email
```bash
curl -X POST http://127.0.0.1:5050/api/v1/email/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer seu-token" \
  -d '{
    "header": "Return-Path: <user@example.com>\n..."
  }'
```

### Listar IOCs
```bash
curl -X GET "http://127.0.0.1:5050/api/v1/iocs?type=domain&limit=50" \
  -H "Authorization: Bearer seu-token"
```

---

## Webhooks (Opcional)

Configure webhooks em `config/settings.json` para receber notificações em tempo real.

**Evento**: Novo alerta crítico

```json
{
  "event": "alert.critical",
  "timestamp": "2026-05-13T11:30:00Z",
  "alert": {
    "id": "ALERT_001",
    "type": "email",
    "severity": "CRÍTICO",
    "risk_score": 85
  }
}
```

---

## Suporte

- **Documentação Interativa**: `/api/docs` (Swagger UI)
- **OpenAPI Schema**: `/api/openapi.json`
- **Issues**: GitHub Issues
- **Email**: api-support@sentinelx-soc.com
