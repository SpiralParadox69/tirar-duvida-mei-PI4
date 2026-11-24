# Tira-Dúvidas do MEI

Assistente virtual (chatbot) que responde dúvidas frequentes de Microempreendedores Individuais (MEI) sobre DAS, limite de faturamento, prazos, nota fiscal, desenquadramento e outros temas. Projeto Integrador IV (FAESA, 2026/2).

**Aplicação no ar:** https://tirar-duvida-mei-pi4.onrender.com

> O plano gratuito do Render "dorme" depois de um tempo sem uso. No primeiro acesso, a página pode levar até cerca de 50 segundos para carregar.

**Autor:** Felipe Cabral Coelho Pinho (Sistemas de Informação, FAESA)
**Professor:** Howard Cruz Roatti

---

## O problema

O MEI é a principal porta de entrada para o empreendedorismo no Brasil, mas a burocracia e a linguagem técnica das obrigações (guia DAS, declaração anual, limite de faturamento) geram dúvidas e inadimplência. Este projeto oferece um assistente que responde essas dúvidas em linguagem simples, com base em uma base de perguntas e respostas curada a partir de fontes oficiais.

## Como funciona

O projeto usa uma versão simplificada de RAG (geração com recuperação de contexto), sem banco vetorial:

1. O usuário digita uma pergunta no chat.
2. O backend faz uma **busca por palavras-chave** em um arquivo JSON com 39 perguntas e respostas sobre o MEI (`data/mei_faq.json`).
3. As entradas mais relevantes (até 3) são enviadas ao modelo de linguagem, via API do Groq, junto com um prompt de sistema que o obriga a responder **somente com base nesse contexto**.
4. Se a busca não encontra nada, o sistema responde que não encontrou a informação e **não chama o modelo**.

Importante: o sistema **não acessa sites oficiais em tempo real**. Todas as respostas vêm do arquivo curado manualmente.

## Funcionalidades

- Chat web simples, com botões de perguntas sugeridas.
- Aviso de privacidade (LGPD): o usuário é orientado a não digitar CPF, CNPJ, senhas ou dados pessoais.
- Limite de 300 caracteres por pergunta e tratamento de erros (400 e 500).
- Defesa contra prompt injection no prompt de sistema.
- Respostas em texto simples, em português do Brasil.

## Tecnologias

- **Backend:** Python, Flask, gunicorn
- **Frontend:** HTML, CSS e JavaScript puros
- **IA:** API do Groq, modelo `openai/gpt-oss-120b`
- **Testes:** pytest
- **Deploy:** Render (Web Service)

## Estrutura do projeto

```
backend/
  app.py            Servidor Flask (rotas "/" e "/perguntar")
  assistente.py     Prompt de sistema e chamada ao Groq
  busca.py          Busca por palavras-chave no FAQ
  teste_groq.py     Teste rápido de conexão com a API
data/
  mei_faq.json      Base de perguntas e respostas (39 entradas)
frontend/
  index.html, style.css, script.js
tests/
  conftest.py, test_busca.py, test_app.py
  eval_ia.py        Avaliação (eval) do componente de IA
docs/
  uso-de-ia.md      Registro do uso de IA no desenvolvimento
  eval_baseline.md  Resultado do eval antes das correções
  eval_resultados.md  Resultado do eval mais recente
  analise-impacto.md
  ia-responsavel.md
```

## Como rodar localmente

Pré-requisitos: Python 3 e uma chave de API gratuita do [GroqCloud](https://console.groq.com).

```powershell
# 1. Clonar o repositório
git clone https://github.com/SpiralParadox69/tirar-duvida-mei-PI4.git
cd tirar-duvida-mei-PI4

# 2. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Criar o arquivo .env a partir do exemplo e colocar sua chave
copy .env.example .env
#    edite o .env e troque "coloque_sua_chave_aqui" pela sua chave do Groq

# 5. Iniciar o servidor
python backend/app.py
```

Abra `http://localhost:5000` no navegador.

A chave **nunca** deve ser escrita no código nem enviada ao GitHub. O arquivo `.env` está no `.gitignore`.

## Testes

```powershell
pytest
```

Os testes unitários cobrem a busca e a montagem do contexto. Os testes de integração cobrem a rota `/perguntar` (pergunta válida, vazia, longa demais, corpo inválido e falha do modelo), usando um modelo simulado, sem gastar a API.

## Avaliação da IA (eval)

```powershell
python tests/eval_ia.py
```

O script faz 36 perguntas reais ao modelo e mede:

- **taxa de acerto e de erro da resposta** (a resposta contém o termo esperado e nenhum termo proibido);
- **taxa de acerto da busca** (a busca trouxe a entrada certa do FAQ);
- **resultado por tema** e tempo médio de resposta.

Os casos incluem perguntas do FAQ, linguagem informal, perguntas fora do tema e tentativas de prompt injection. O relatório é salvo em `docs/eval_resultados.md`. Por usar a API gratuita do Groq, o script espera entre as chamadas e tenta de novo uma vez em caso de erro.

## Deploy

O deploy é feito no Render, como Web Service, com atualização automática a cada `git push`.

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn --chdir backend app:app`
- **Variável de ambiente:** `GROQ_API_KEY` (configurada no painel do Render, nunca no código)

## Limitações conhecidas

- A busca por palavras-chave **não entende sinônimos nem linguagem muito informal**. Perguntas como "tem como pagar em prestações?" dependem de a palavra estar nas keywords da entrada.
- A base tem 39 entradas. Temas que não estão nela recebem a resposta "não encontrei".
- Valores e regras refletem as fontes consultadas em 2026 e podem mudar. O assistente é **informativo** e não substitui um contador ou orientação jurídica.
- O plano gratuito do Groq e do Render tem limites de uso e de disponibilidade.

## Documentação

- [Uso de IA no desenvolvimento](docs/uso-de-ia.md)
- [Análise de impacto](docs/analise-impacto.md)
- [IA responsável (LGPD, segurança, ética e custo)](docs/ia-responsavel.md)
- [Resultado do eval](docs/eval_resultados.md) e [baseline](docs/eval_baseline.md)