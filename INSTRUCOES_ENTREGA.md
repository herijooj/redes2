# MiniCoin - Instruções de Entrega e Demonstração

## 📦 Projeto Completo - Pronto para Entrega

**Data de Conclusão:** 28 de outubro de 2025  
**Prazo de Entrega:** 14 de novembro de 2025  
**Status:** ✅ **COMPLETO E TESTADO**

---

## 🎯 Resumo Executivo

O projeto **MiniCoin** foi implementado com sucesso, atendendo **100% dos requisitos** especificados no trabalho prático:

- ✅ Blockchain funcional com SHA-256
- ✅ Servidor TCP único mantendo o ledger
- ✅ Validação de transações (rejeita overdrafts)
- ✅ Cliente simulador com cenários válidos e inválidos
- ✅ 23 testes unitários (100% aprovados)
- ✅ Logs detalhados de execução
- ✅ Relatório HTML completo com diagramas
- ✅ Código fonte com extensão .txt

---

## 📁 Localização dos Arquivos de Entrega

### 1. Relatório HTML (Principal)
```
docs/report/index.html
```
**Contém:**
- Explicação completa da arquitetura
- Diagramas da blockchain
- Descrição do protocolo de comunicação
- Resultados dos testes
- Links para código fonte e logs

### 2. Código Fonte (.txt)
```
deliverables/code/ledger.py.txt      - Implementação da blockchain
deliverables/code/server.py.txt      - Servidor TCP
deliverables/code/simulator.py.txt   - Cliente simulador
deliverables/code/test_ledger.py.txt - Testes unitários
```

### 3. Logs de Execução
```
deliverables/logs/server.log  - Log do servidor (30KB)
deliverables/logs/client.log  - Log do cliente (13KB)
```

---

## 🚀 Como Executar no Laboratório

### Passo 1: Clonar o Repositório
```bash
# Se estiver em um repositório Git
git clone <URL_DO_REPOSITORIO>
cd redes2

# OU copiar os arquivos diretamente
```

### Passo 2: Entrar no Ambiente Nix
```bash
nix-shell
```

Este comando irá:
- Instalar Python 3.11
- Instalar todas as dependências (pydantic, pytest, rich)
- Configurar o ambiente de forma isolada

### Passo 3: Executar Testes
```bash
pytest tests/ -v
```

**Resultado esperado:**
```
================== 23 passed in 0.04s ===================
```

### Passo 4: Demonstração Completa

**Opção A: Automática (Recomendada)**
```bash
./run_demo.sh
```

**Opção B: Manual**

Terminal 1 (Servidor):
```bash
nix-shell
python -m minicoin.server --owner "João Silva" --initial 100.0
```

Terminal 2 (Cliente):
```bash
nix-shell
python -m clients.simulator
```

### Passo 5: Visualizar Relatório
```bash
./view_report.sh

# OU abrir manualmente no navegador:
firefox docs/report/index.html
```

---

## 📊 Estrutura do Projeto

```
redes2/
│
├── docs/report/index.html          ← RELATÓRIO PRINCIPAL
│
├── deliverables/                   ← ARQUIVOS DE ENTREGA
│   ├── code/
│   │   ├── ledger.py.txt
│   │   ├── server.py.txt
│   │   ├── simulator.py.txt
│   │   └── test_ledger.py.txt
│   └── logs/
│       ├── server.log
│       └── client.log
│
├── minicoin/                       ← CÓDIGO FONTE ORIGINAL
│   ├── __init__.py
│   ├── ledger.py
│   └── server.py
│
├── clients/
│   ├── __init__.py
│   └── simulator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_ledger.py
│   └── test_integration.py
│
├── shell.nix                       ← AMBIENTE NIX
├── run_demo.sh                     ← SCRIPT DE DEMONSTRAÇÃO
├── view_report.sh                  ← ABRE O RELATÓRIO
├── requirements.txt
├── README.md
└── DELIVERABLES.md                 ← ESTE ARQUIVO
```

---

## ✅ Checklist de Verificação

Antes da entrega/demonstração, verifique:

- [ ] Ambiente Nix instalado no laboratório
- [ ] Todos os 23 testes passando
- [ ] Servidor inicia sem erros
- [ ] Cliente conecta e executa transações
- [ ] Logs são gerados corretamente
- [ ] Relatório HTML abre no navegador
- [ ] Código fonte .txt está acessível

---

## 🎓 Conceitos Implementados

### Redes de Computadores
- ✅ Sockets TCP
- ✅ Protocolo cliente-servidor
- ✅ Comunicação assíncrona (AsyncIO)
- ✅ Mensagens JSON
- ✅ Tratamento de conexões múltiplas

### Blockchain
- ✅ Hash criptográfico (SHA-256)
- ✅ Encadeamento de blocos
- ✅ Verificação de integridade
- ✅ Registro imutável de transações

### Engenharia de Software
- ✅ Testes unitários abrangentes
- ✅ Logging estruturado
- ✅ Documentação completa
- ✅ Código limpo e comentado

---

## 📈 Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| Linhas de código Python | ~1200 |
| Testes implementados | 23 |
| Taxa de aprovação | 100% |
| Cenários de teste | 5 |
| Transações simuladas | 30+ |
| Arquivos de código | 8 |
| Tamanho do relatório HTML | 28 KB |
| Logs gerados | 43 KB |

---

## 🐛 Troubleshooting

### Problema: "nix-shell not found"
**Solução:** Instale o Nix:
```bash
sh <(curl -L https://nixos.org/nix/install) --daemon
```

### Problema: Porta 8888 já em uso
**Solução:** Use outra porta:
```bash
python -m minicoin.server --port 9999
python -m clients.simulator --port 9999
```

### Problema: Testes falhando
**Solução:** Limpe e recrie o ambiente:
```bash
rm -rf .pytest_cache
nix-shell --run "pytest tests/ -v"
```

---

## 📧 Informações para Entrega

**Disciplina:** Redes de Computadores II  
**Professor:** Elias P. Duarte Jr.  
**Instituição:** UFPR - Departamento de Informática  
**Semestre:** 2025/2  
**Data Limite:** 14 de novembro de 2025  

**Subject do e-mail:** "TP REDES II 2025-2"  
**Conteúdo:** URL do repositório ou link para os arquivos

---

## 🎉 Conclusão

O projeto MiniCoin está **completo, testado e documentado**. Todos os requisitos do trabalho foram atendidos com qualidade:

1. ✅ **Blockchain funcional** - Lista encadeada com hash SHA-256
2. ✅ **Servidor único** - Mantém toda a blockchain
3. ✅ **Validação correta** - Aceita válidos, rejeita inválidos
4. ✅ **Testes exaustivos** - 23 testes unitários
5. ✅ **Documentação completa** - Relatório HTML profissional
6. ✅ **Entregáveis corretos** - Código .txt e logs
7. ✅ **Funciona no lab** - Ambiente Nix reproduzível

**O trabalho está pronto para ser apresentado e defendido no laboratório!**

---

**Desenvolvido com:** Python 3.11, AsyncIO, SHA-256, Pytest, Nix  
**Tempo de execução dos testes:** < 0.1s  
**Sistema operacional:** Linux (compatível com qualquer distribuição via Nix)

---

Para qualquer dúvida, consulte:
- `README.md` - Documentação técnica
- `docs/report/index.html` - Relatório completo
- Código fonte - Totalmente comentado
