# Tira-Dúvidas do MEI

Assistente de IA que responde dúvidas frequentes de Microempreendedores Individuais (MEI) sobre suas obrigações básicas — como emissão da guia DAS, prazos de pagamento, limite de faturamento, desenquadramento, emissão de nota fiscal e declaração anual.

## Sobre o projeto

Projeto desenvolvido para a disciplina Projeto Integrador IV (FAESA, 2026/2), na área temática de Trabalho e Empreendedorismo. O objetivo é reduzir a barreira de informação enfrentada por MEIs, que muitas vezes não têm acesso fácil a orientação contábil, traduzindo obrigações burocráticas em respostas simples e diretas.

## Como funciona

O assistente usa uma técnica de RAG simplificada: as perguntas do usuário são comparadas por busca de palavra-chave contra uma base própria de perguntas e respostas (curada a partir de fontes oficiais como Portal do Empreendedor, Sebrae e Receita Federal). O contexto encontrado é enviado, junto com a pergunta, para um modelo de linguagem (LLM) via API do Groq, que gera a resposta final em linguagem natural.

## Tecnologias previstas

- **Backend:** Python + Flask
- **Frontend:** HTML, CSS e JavaScript
- **IA:** API Groq (LLMs abertos e gratuitos)
- **Testes:** pytest (testes unitários e de integração)
- **Deploy:** Render ou Railway (free tier)

## Status atual

🟡 Em planejamento — C2 (protótipo funcional, com testes automatizados e eval) entregue.

## Autor e Grupo:

Felipe Cabral Coelho Pinho — Sistemas de Informação, FAESA