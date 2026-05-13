# 🤝 Guia de Contribuição - SentinelX SOC

Obrigado por se interessar em contribuir para o SentinelX SOC! Este documento fornece orientações para manter a qualidade e consistência do projeto.

## 📋 Código de Conduta

Todos os contribuidores devem seguir nosso [Código de Conduta](CODE_OF_CONDUCT.md).

---

## 🎯 Como Contribuir

### 1. Reportar Bugs

Encontrou um bug? Abra uma issue com as seguintes informações:

**Título**: Breve descrição do bug
```
[BUG] Problema específico que ocorre
```

**Descrição**:
```markdown
## Descrição do Bug
Descrição clara e concisa do problema.

## Passos para Reproduzir
1. Passo 1
2. Passo 2
3. ...

## Comportamento Esperado
O que deveria acontecer

## Comportamento Real
O que realmente acontece

## Screenshots
Se aplicável, adicione prints

## Ambiente
- OS: Windows 10 / Linux Ubuntu 20.04 / macOS 11
- Python: 3.8 / 3.9 / 3.10
- Versão do SentinelX: v1.0.0

## Logs
```
Cole logs relevantes aqui
```
```

### 2. Sugerir Features

Tem uma ideia legal? Abra uma issue com:

```markdown
## Descrição da Feature
Descrição clara do que você gostaria de adicionar.

## Motivação
Por que essa feature é importante?

## Solução Proposta
Exemplos de código ou mockups.

## Alternativas Consideradas
Outras abordagens que você pensou.

## Contexto Adicional
Outras informações relevantes.
```

### 3. Submeter Code

#### 3.1 Prepare seu Ambiente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/sentinelx-soc.git
cd sentinelx-soc

# Crie uma branch
git checkout -b feature/sua-feature

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 3.2 Desenvolvendo

**Padrões de Código**:

```python
# ✅ BOM - Código limpo e bem estruturado
def analyze_email_header(header: str) -> dict:
    """
    Analisa headers de email para detectar anomalias.
    
    Args:
        header (str): String contendo headers do email
        
    Returns:
        dict: Resultado da análise com risk_score e detalhes
        
    Raises:
        ValueError: Se header está vazio ou inválido
    """
    if not header or not isinstance(header, str):
        raise ValueError("Header must be a non-empty string")
    
    result = {
        "risk_score": 0,
        "spf_status": check_spf(header),
        "dkim_status": check_dkim(header),
        "dmarc_status": check_dmarc(header),
    }
    
    return result


# ❌ RUIM - Código sem estrutura
def analyze(h):
    if not h:
        return None
    r = {}
    # lógica complexa sem comentários
    return r
```

**Convenções**:
- Use **type hints** em todas as funções
- Escreva **docstrings** (Google style)
- Mantenha funções **pequenas** (máx 50 linhas)
- Use **nomes descritivos**
- Adicione **comentários** para lógica complexa

#### 3.3 Testes

```bash
# Execute os testes
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=modules --cov-report=html

# Testes específicos
pytest tests/test_email_analyzer.py::test_spf_validation -v
```

**Escreva testes para suas mudanças**:

```python
# tests/test_email_analyzer.py
import pytest
from modules.email_analyzer.header_analyzer import analyze_header


class TestEmailAnalyzer:
    """Testes para análise de headers de email."""
    
    def test_analyze_valid_header(self):
        """Testa análise de header válido."""
        header = "Return-Path: <test@example.com>\nReceived: from server.com"
        result = analyze_header(header)
        
        assert "risk_score" in result
        assert isinstance(result["risk_score"], int)
        assert result["risk_score"] >= 0
    
    def test_analyze_invalid_header(self):
        """Testa análise de header inválido."""
        with pytest.raises(ValueError):
            analyze_header("")
    
    def test_detect_spoofing(self):
        """Testa detecção de email spoofing."""
        header = "Return-Path: <fake@bank.com>\nReceived: from attacker.com"
        result = analyze_header(header)
        
        assert result["risk_score"] >= 70
```

#### 3.4 Commit e Push

```bash
# Stage suas mudanças
git add .

# Commit com mensagem descritiva
git commit -m "feat: adiciona detecção de typosquatting em URLs"

# Push para seu fork
git push origin feature/sua-feature
```

**Formato de Mensagens de Commit**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: Nova feature
- `fix`: Bug fix
- `docs`: Documentação
- `style`: Formatação (não afeta lógica)
- `refactor`: Refatoração sem mudanças de features
- `perf`: Melhoria de performance
- `test`: Testes
- `chore`: Build, dependencies, etc.

**Exemplos**:
```
feat(email-analyzer): adiciona validação de DMARC

fix(url-scanner): corrige falha em detecção de typosquatting

docs: atualiza README com novos exemplos

test(campaign-detector): aumenta cobertura de testes
```

#### 3.5 Pull Request

1. **Crie um PR** contra a branch `main`
2. **Preencha o template**:

```markdown
## 📝 Descrição
Descrição clara do que foi mudado e por quê.

## 🔗 Issues Relacionadas
Fecha #123

## 🧪 Como Testar
Passos para testar as mudanças:
1. ...
2. ...

## 📸 Screenshots
Se aplicável, adicione screenshots ou GIFs.

## ✅ Checklist
- [ ] Código segue os padrões do projeto
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Sem breaking changes
- [ ] Commits têm mensagens descritivas
```

3. **Aguarde review** - Mantenedores revisarão sua mudança
4. **Resolva comentários** - Faça ajustes se solicitado
5. **Merge** - Uma vez aprovado, será merged!

---

## 📚 Estrutura de Pastas

Adicione novos módulos seguindo a estrutura:

```
modules/novo_modulo/
├── __init__.py
├── analyzer.py          # Lógica principal
├── utils.py             # Funções utilitárias
└── tests/
    ├── __init__.py
    ├── test_analyzer.py
    └── fixtures/
```

---

## 🧪 Padrões de Teste

```python
# ✅ BOM
def test_returns_dict_with_risk_score():
    """Testa se retorna dicionário com risk_score."""
    result = analyze_url("http://example.com")
    assert isinstance(result, dict)
    assert "risk_score" in result

# ❌ RUIM
def test_works():
    """Testa se funciona."""
    result = analyze_url("http://example.com")
    assert result is not None
```

---

## 📖 Documentação

### Docstrings

```python
def detect_phishing(email_content: str, threshold: float = 0.7) -> dict:
    """
    Detecta potencial phishing em conteúdo de email.
    
    Usa análise comportamental e pattern matching para identificar
    tentativas de phishing. Suporta detecção de:
    - Urgência artificial
    - Pedidos de credenciais
    - Links suspeitos
    
    Args:
        email_content (str): Conteúdo do email a analisar.
        threshold (float): Score mínimo para alertar (0.0-1.0).
                          Padrão: 0.7
    
    Returns:
        dict: Dicionário contendo:
            - 'is_phishing' (bool): Se é provável phishing
            - 'confidence' (float): Confiança da detecção (0.0-1.0)
            - 'indicators' (list): Lista de indicadores encontrados
            
    Raises:
        ValueError: Se email_content está vazio
        TypeError: Se threshold não é float
        
    Examples:
        >>> result = detect_phishing("Click here to verify your account")
        >>> result['is_phishing']
        True
        >>> result['confidence']
        0.95
    """
```

### README de Módulo

```markdown
# URL Scanner

Módulo para análise e validação de URLs suspeitas.

## Recursos

- Detecção de typosquatting
- Análise de reputação de domínio
- Integração com VirusTotal
- Cache de resultados

## Uso

```python
from modules.url_scanner.url_analyzer import analyze_url

result = analyze_url("http://suspicious-url.com")
print(result['risk_score'])
```

## Configuração

Adicione à `config/settings.json`:

```json
{
  "virustotal_api_key": "sua_chave"
}
```

## Testes

```bash
pytest tests/url_scanner/ -v
```
```

---

## 🔄 Processo de Review

1. **Verificação de CI/CD** - Testes devem passar
2. **Code Review** - Pelo menos 1 mantenedor
3. **Approval** - 2 approvals de mantenedores
4. **Merge** - Squash merge para manter histórico limpo

---

## 💡 Dicas

- ✅ Comece com issues simples (tagged `good-first-issue`)
- ✅ Comunique-se antes de começar trabalho grande
- ✅ Revise PRs de outros para aprender
- ✅ Faça PRs pequenas (melhor revisão)
- ✅ Mantenha o histórico git limpo

---

## 🚫 O Que Não Fazer

- ❌ Não commitar dependências (`node_modules`, `venv`, etc.)
- ❌ Não adicionar secrets/chaves de API
- ❌ Não fazer grandes refatorações sem discussão
- ❌ Não ignorar linting ou testes falhando
- ❌ Não fazer rebase em branches públicas

---

## 📞 Dúvidas?

- **Discussões**: GitHub Discussions
- **Discord**: [Comunidade SentinelX](https://discord.gg/sentinelx)
- **Email**: dev@sentinelx-soc.com

---

## 🎉 Obrigado!

Sua contribuição torna o SentinelX SOC melhor para todos!

**Happy coding! 🚀**
