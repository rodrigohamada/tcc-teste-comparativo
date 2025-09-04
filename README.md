# Projeto de TCC: Análise Comparativa de Esteiras CI/CD com e sem DevSecOps

Este repositório é um projeto prático que demonstra a diferença fundamental entre uma esteira de Integração Contínua (CI) tradicional e uma esteira moderna que incorpora práticas de segurança (DevSecOps).

## 🎯 Objetivo

O objetivo principal é evidenciar, de forma prática, como a integração de ferramentas de segurança automatizadas em uma esteira de CI/CD pode **prevenir ativamente** a introdução de vulnerabilidades no código-fonte, criando uma barreira de proteção que não existe em fluxos de trabalho tradicionais.

---

## 🔬 A Aplicação de Exemplo

Para realizar a comparação, utilizamos uma mini-aplicação web construída em **Flask (Python)**. Esta aplicação foi **desenvolvida propositalmente com múltiplas falhas de segurança** para servir como um campo de testes para as nossas esteiras.

As vulnerabilidades introduzidas são exemplos clássicos de erros de desenvolvimento e configuração, mapeadas para serem detectadas pelas ferramentas de segurança na esteira DevSecOps.

### Tabela de Vulnerabilidades Intencionais

| Tipo de Vulnerabilidade | Localização no Código | Descrição da Falha | Ferramenta de Detecção |
| :--- | :--- | :--- | :--- |
| **Análise de Dependências (SCA)** | `requirements.txt` | Uso de bibliotecas (`Flask`, `PyYAML`) com versões antigas e notoriamente vulneráveis a dezenas de CVEs. | **Trivy** |
| **Vazamento de Segredos (Secrets)** | `app.py` e `config.py` | Chaves de API, senhas de banco de dados e credenciais da AWS foram deixadas diretamente no código (hardcoded). | **Gitleaks** |
| **Injeção de SQL (SQLi)** | `app.py` (rota `/usuario`) | A consulta SQL é construída concatenando texto diretamente com a entrada do usuário, permitindo a manipulação da query. | **Semgrep** |
| **Injeção de Comando (RCE)** | `app.py` (rota `/executar`) | Um comando do sistema operacional é executado usando `subprocess` com `shell=True`, utilizando diretamente a entrada do usuário. | **Semgrep** |
| **Modo de Depuração Ativo** | `app.py` (final do arquivo) | A aplicação Flask é executada com `debug=True`, o que é um risco de segurança gravíssimo em produção. | **Semgrep** |

---

## ⚙️ As Esteiras de CI/CD

Ao realizar um `push` de código para este repositório, duas esteiras de trabalho (GitHub Actions) são acionadas simultaneamente. Elas representam duas filosofias diferentes de desenvolvimento e automação.

### 1. Esteira de CI Tradicional
[![Status da Esteira Tradicional](https://img.shields.io/badge/Status-Sucesso-brightgreen)](.github/workflows/tradicional-ci.yml)

Este workflow (`tradicional-ci.yml`) simula um processo de CI focado exclusivamente na funcionalidade.

* **O que faz?**
    1.  Baixa o código do repositório.
    2.  Instala as dependências listadas no `requirements.txt`.
    3.  Simula a execução de testes unitários e o processo de build.

* **Resultado Esperado:**
    A esteira **passa com sucesso (✔️)**. Ela é completamente "cega" às vulnerabilidades de segurança, pois seu único objetivo é garantir que a aplicação não quebre funcionalmente. Isso gera uma falsa sensação de segurança.

### 2. Esteira de CI com DevSecOps
[![Status da Esteira DevSecOps](https://img.shields.io/badge/Status-Falha-red)](.github/workflows/devsecops-ci.yml)

Este workflow (`devsecops-ci.yml`) representa a abordagem moderna de "Shift-Left", integrando a segurança diretamente no ciclo de desenvolvimento.

* **O que faz?**
    1.  Baixa o código do repositório.
    2.  **[SAST]** Executa o **Semgrep** para análise estática de código, procurando por padrões de código inseguros.
    3.  **[Secrets]** Executa o **Gitleaks** para escanear todo o histórico em busca de segredos vazados.
    4.  **[SCA]** Executa o **Trivy** para analisar as dependências em busca de vulnerabilidades conhecidas (CVEs).
    5.  Envia os resultados para a aba de Segurança do GitHub.

* **Resultado Esperado:**
    A esteira **FALHA ativamente (❌)**. Ao detectar as vulnerabilidades de criticidade alta (como senhas no código e bibliotecas vulneráveis), as ferramentas retornam um código de erro que interrompe o fluxo. Ela atua como uma barreira de qualidade, impedindo que o código inseguro seja integrado.

---

## 📊 Como Visualizar os Resultados

1.  **Aba "Actions"**: No GitHub, esta aba mostra a execução das duas esteiras. Você verá a `CI Tradicional` com um ✔️ verde e a `CI com DevSecOps` com um ❌ vermelho.

    ![Imagem da Aba Actions](https://i.imgur.com/8f6u11R.png)

2.  **Aba "Security"**: A esteira DevSecOps envia todos os achados para a aba `Security > Code scanning`. Lá, é possível ver um relatório detalhado de cada vulnerabilidade encontrada pelo Semgrep, Gitleaks e Trivy, com a localização exata no código.

    ![Imagem da Aba Security](https://i.imgur.com/kSg3Gk2.png)

## ✅ Conclusão

Este projeto demonstra que uma esteira de CI tradicional, embora útil, não é suficiente para garantir a segurança de uma aplicação. A abordagem DevSecOps, por outro lado, fornece uma rede de segurança automatizada e imediata, capacitando os desenvolvedores a encontrar e corrigir falhas no início do ciclo de vida do software, reduzindo custos e riscos.
