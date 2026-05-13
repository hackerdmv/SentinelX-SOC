# 🚀 Guia de Instalação - SentinelX SOC

Este guia fornece instruções detalhadas para instalar e configurar o SentinelX SOC em diferentes ambientes.

---

## 📋 Pré-requisitos

### Sistema Operacional
- **Windows**: 10 ou superior
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 9+
- **macOS**: 10.14+

### Software Requerido
- **Python**: 3.8 ou superior
- **pip**: Última versão
- **git**: Para clonar repositório (opcional)

### Hardware Recomendado
- **CPU**: 2 cores mínimo
- **RAM**: 4GB mínimo (8GB recomendado)
- **Disco**: 2GB espaço livre

---

## 💻 Instalação em Windows

### Passo 1: Instalar Python

1. Acesse [python.org](https://www.python.org/downloads/)
2. Baixe **Python 3.10+** (64-bit recomendado)
3. Execute o instalador
4. **IMPORTANTE**: Marque "Add Python to PATH"
5. Clique "Install Now"

**Verificar instalação**:
```bash
python --version
pip --version
```

### Passo 2: Clonar/Baixar Projeto

**Opção A - Com Git**:
```bash
git clone https://github.com/seu-usuario/sentinelx-soc.git
cd sentinelx-soc
```

**Opção B - Download ZIP**:
1. Acesse GitHub
2. Clique em "Code" → "Download ZIP"
3. Extraia o arquivo
4. Abra terminal na pasta extraída

### Passo 3: Criar Ambiente Virtual

```bash
python -m venv venv
venv\Scripts\activate
```

Você deve ver `(venv)` no início do prompt.

### Passo 4: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 5: Configurar Projeto

```bash
python setup_project.py
```

Isso criará a estrutura de pastas necessária.

### Passo 6: Executar

**Interface Web**:
```bash
python launcher.py
```

**CLI**:
```bash
python main.py
```

**Monitor contínuo**:
```bash
python monitor.py
```

---

## 🐧 Instalação em Linux/macOS

### Passo 1: Instalar Dependências

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv git
```

**CentOS/RHEL**:
```bash
sudo yum install python3 python3-pip git
```

**macOS**:
```bash
brew install python@3.10 git
```

### Passo 2: Clonar Projeto

```bash
git clone https://github.com/seu-usuario/sentinelx-soc.git
cd sentinelx-soc
```

### Passo 3: Criar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 4: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 5: Configurar Projeto

```bash
python3 setup_project.py
```

### Passo 6: Dar Permissões (Linux)

```bash
chmod +x launcher.py main.py monitor.py
```

### Passo 7: Executar

```bash
python3 launcher.py
```

---

## 🐳 Instalação com Docker

### Passo 1: Criar Dockerfile

Crie arquivo `Dockerfile` na raiz do projeto:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Criar estrutura
RUN python setup_project.py

# Expor porta
EXPOSE 5050

# Iniciar aplicação
CMD ["python", "launcher.py"]
```

### Passo 2: Criar docker-compose.yml

```yaml
version: '3.8'

services:
  sentinelx:
    build: .
    ports:
      - "5050:5050"
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    environment:
      - FLASK_ENV=production
      - LOG_LEVEL=INFO
    restart: unless-stopped
```

### Passo 3: Build e Run

```bash
docker-compose up -d
```

Acesse: http://localhost:5050

---

## ⚙️ Configuração Pós-Instalação

### 1. Editar config/settings.json

```bash
# Abra o arquivo
nano config/settings.json  # Linux/macOS
notepad config/settings.json  # Windows
```

Configure:
- API keys (VirusTotal, etc)
- SMTP para alertas
- Firewall endpoint

### 2. Configurar Permissões de Firewall

Se usando bloqueio ativo:

**Windows**:
```bash
# Execute como administrador
python core/blocking/firewall_blocker.py --setup
```

**Linux**:
```bash
# Pode precisar de sudo para iptables
sudo usermod -a -G docker $USER
```

### 3. Adicionar Targets para Monitorar

Edite `data/monitor/targets.json`:

```json
{
  "urls": [
    "http://suspicious-site-1.com",
    "http://suspicious-site-2.com"
  ],
  "headers": [
    "Return-Path: <sender@domain.com>\n..."
  ]
}
```

### 4. Integração com Threat Intelligence

Obtenha chaves de API:

**VirusTotal**:
1. Acesse https://www.virustotal.com
2. Registre-se
3. Vá para "Settings" → "API key"
4. Copie sua chave

**Adicione a config/settings.json**:
```json
{
  "threat_intelligence": {
    "virustotal_api_key": "sua-chave-aqui"
  }
}
```

---

## 🧪 Verificar Instalação

### 1. Testar Importações

```bash
python -c "import flask; print('Flask OK')"
python -c "import requests; print('Requests OK')"
python -c "from modules.email_analyzer import header_analyzer; print('Email Analyzer OK')"
```

### 2. Testar Estrutura

```bash
python setup_project.py
ls -la data/  # Verificar pastas criadas
```

### 3. Teste Rápido

```python
# Abra Python interativo
python

# Cole:
from modules.email_analyzer.header_analyzer import analyze_header
result = analyze_header("Test header")
print(result)
# Deve retornar um dicionário
```

---

## 🔧 Troubleshooting

### Problema: "Python não encontrado"

**Solução**:
```bash
# Windows - Instale Python do site oficial
# Linux - sudo apt-get install python3-dev

# Verifique
python3 --version
```

### Problema: "ModuleNotFoundError: No module named 'flask'"

**Solução**:
```bash
# Ative o ambiente virtual
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Reinstale dependências
pip install -r requirements.txt
```

### Problema: "Port 5050 already in use"

**Solução Windows**:
```bash
# Encontre processo usando port 5050
netstat -ano | findstr :5050

# Mate o processo (substitua PID)
taskkill /PID PID_NUMBER /F
```

**Solução Linux/macOS**:
```bash
lsof -i :5050
kill -9 PID
```

**Ou mude a porta em launcher.py**:
```python
app.run(host="127.0.0.1", port=8080)  # Use porta 8080
```

### Problema: "Permission denied"

**Linux**:
```bash
chmod +x launcher.py main.py monitor.py
```

**Windows**:
- Execute cmd como administrador
- Navegue até pasta do projeto
- Execute normalmente

### Problema: "No module named 'ui.dashboard.app'"

**Solução**:
```bash
# Certifique-se que ui/dashboard/app.py existe
ls ui/dashboard/

# Se não existir, crie structure:
python setup_project.py
```

---

## 🚀 Instalação em Produção

### 1. Usar Gunicorn (não Flask dev server)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5050 ui.dashboard.app:app
```

### 2. Usar Supervisor (Linux)

Crie `/etc/supervisor/conf.d/sentinelx.conf`:

```ini
[program:sentinelx]
command=/home/user/sentinelx-soc/venv/bin/python /home/user/sentinelx-soc/launcher.py
directory=/home/user/sentinelx-soc
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/sentinelx.log
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start sentinelx
```

### 3. Usar Nginx como Reverse Proxy

```nginx
server {
    listen 80;
    server_name sentinelx.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Configurar SSL/TLS

```bash
# Usando Let's Encrypt
sudo certbot certonly --nginx -d sentinelx.yourdomain.com
```

---

## 🐛 Debug

### Ativar modo debug

```python
# Edite launcher.py
app.run(debug=True)  # Cuidado: nunca em produção!
```

### Ver logs

```bash
tail -f data/logs/launcher.log
tail -f data/logs/analysis.log
```

### Debug interativo

```bash
python -m pdb launcher.py
```

---

## 📞 Suporte

- **Documentação**: Veja README.md
- **Issues**: GitHub Issues
- **Comunidade**: Discord do SentinelX
- **Email**: support@sentinelx-soc.com

---

## ✅ Próximos Passos

1. ✅ Leia [README.md](README.md)
2. ✅ Acesse dashboard em http://127.0.0.1:5050
3. ✅ Configure config/settings.json
4. ✅ Adicione URLs/headers para analisar
5. ✅ Configure alertas de email
6. ✅ Integrate com Threat Intelligence

---

**Bem-vindo ao SentinelX SOC! 🛡️**
