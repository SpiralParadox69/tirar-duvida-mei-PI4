# IA responsável

Projeto Integrador IV — Tira-Dúvidas do MEI
Autor: Felipe Cabral Coelho Pinho

Este documento descreve como o assistente trata privacidade (LGPD), segurança, ética e custo. Ele descreve o **produto** (o chatbot). O registro de como a IA foi usada para **desenvolver** o projeto está em [uso-de-ia.md](uso-de-ia.md).

## 1. Privacidade e LGPD

**Quais dados o sistema recebe.** Apenas o texto da pergunta digitada pelo usuário, com no máximo 300 caracteres. Não há cadastro, login nem formulário com dados pessoais.

**O que acontece com esses dados.**
- A aplicação **não grava as perguntas** em banco de dados nem em arquivo.
- A pergunta (junto com as entradas do FAQ selecionadas) é enviada ao serviço de IA externo (**Groq**) para gerar a resposta. Esse envio é a única transferência de dados do sistema, e o tratamento feito pelo Groq segue a política de privacidade da própria empresa.
- A hospedagem (Render) pode manter registros técnicos de acesso do servidor, conforme a política da plataforma.

**Medidas adotadas.**
- **Minimização:** o limite de 300 caracteres reduz a chance de o usuário enviar informações em excesso.
- **Aviso na tela:** o chat informa, perto da caixa de texto, que o usuário **não deve digitar CPF, CNPJ, senhas ou outros dados pessoais** e que as perguntas são enviadas a um serviço de IA externo (transparência sobre o destino dos dados).
- **Sem necessidade de dados pessoais:** nenhuma resposta do assistente depende de identificar o usuário, porque ele responde dúvidas gerais sobre o MEI.
- **Teste de privacidade:** o eval inclui uma pergunta sobre digitar CPF e senha no chat, e a resposta correta orienta o usuário a não fazer isso.

**Limites.** Esta é uma aplicação acadêmica. Não foi feita uma avaliação jurídica formal de conformidade com a LGPD (como relatório de impacto ou definição de base legal). Para uso em produção, isso seria necessário.

## 2. Segurança

| Risco | Como o projeto trata |
|---|---|
| Vazamento da chave da API | A chave do Groq fica em variável de ambiente (`.env` localmente e painel do Render no deploy). O `.env` está no `.gitignore`, e o repositório só tem o `.env.example` com um valor de mentira. |
| Prompt injection (usuário tenta mudar as regras do assistente) | O prompt de sistema manda responder **somente** com base no contexto, ignorar pedidos para mudar as regras ou revelar as instruções, e falar apenas sobre MEI. O eval testa 3 tentativas (pedir para ignorar regras e dar um limite falso, pedir para mostrar as instruções e pedir uma piada). |
| Perguntas fora do tema | Se a busca não encontra entradas, o sistema responde com uma mensagem fixa **sem chamar o modelo**. Quando a busca traz entradas sem relação, o prompt faz o modelo responder que não encontrou a informação. |
| Entrada maliciosa ou inválida | O backend valida a pergunta (vazia, longa demais ou corpo inválido retornam erro 400). |
| XSS (código injetado na tela) | O frontend usa `textContent` para exibir mensagens, e nunca `innerHTML`, então texto digitado ou gerado não é interpretado como HTML. |
| Vazamento de detalhes em erros | Se o modelo falha, o usuário recebe uma mensagem genérica (erro 500), e o detalhe técnico fica apenas no log do servidor. |
| Abuso e uso excessivo | **Ainda não há limite de perguntas por usuário.** É uma limitação conhecida, tratada na seção 4. |

## 3. Ética e transparência

- **Caráter informativo.** O assistente informa em todas as telas que **não substitui um contador nem orientação jurídica**, e o prompt repete essa regra ao modelo.
- **Respostas ancoradas em fontes.** O modelo só responde com base numa base de perguntas e respostas curada por mim a partir de fontes oficiais (Portal do Empreendedor, Sebrae, Receita Federal), o que reduz o risco de invenção de valores, prazos e regras. Quando não há informação, o assistente **admite** e orienta o usuário a consultar o Portal do Empreendedor ou um contador.
- **Incerteza declarada.** Onde as fontes divergiram (carência do salário-maternidade), a resposta orienta o usuário a conferir no Meu INSS, em vez de afirmar um valor incerto.
- **Risco de dano.** Informação errada sobre tributos pode levar o usuário a atrasar guias ou ultrapassar o limite sem perceber. Por isso as respostas são curtas, objetivas e remetem à fonte oficial nos temas sensíveis.
- **Atualização.** Valores e regras (limite de R$ 81.000, valor do DAS) mudam com o tempo. O FAQ reflete as fontes consultadas em 2026 e precisa de revisão manual quando houver mudança.
- **Transparência sobre a IA.** O usuário sabe que está conversando com um assistente de IA, e o chat avisa que as perguntas são processadas por um serviço externo.
- **Acessibilidade e inclusão.** A linguagem das respostas é simples e em português do Brasil, pensada para quem não tem formação contábil.

## 4. Limitações conhecidas

- A busca por palavras-chave **não entende sinônimos nem linguagem muito informal**. O eval mostra 92% de acerto da busca: nos casos restantes, a resposta final continua correta por causa do prompt, mas perguntas reais dos usuários podem expor outros pontos fracos.
- O modelo **não responde sempre igual**: o resultado do eval pode variar um pouco entre execuções.
- A base tem 39 entradas e não cobre todos os temas do MEI.
- **Sem limite de perguntas por usuário.** Isso expõe o projeto a uso excessivo e consome a cota gratuita da API. Uma melhoria futura é um limite por IP ou sessão no backend.
- Não houve teste com usuários reais, apenas o eval automatizado.

## 5. Custo

- **API (Groq):** o projeto usa o plano gratuito, que tem limites de requisições e de tokens. Não há cobrança, mas o serviço pode retornar erro quando o limite é atingido, e o usuário vê uma mensagem de erro amigável.
- **Hospedagem (Render):** plano gratuito. O serviço "dorme" depois de um tempo sem uso, e o primeiro acesso pode demorar até cerca de 50 segundos.
- **Controle do consumo de tokens:**
  - cada chamada envia no máximo 3 entradas do FAQ mais a pergunta (limitada a 300 caracteres), o que mantém o prompt curto;
  - quando a busca não encontra nada, o modelo **não é chamado**, e a mensagem fixa não gasta tokens;
  - a temperatura baixa (0,2) deixa as respostas mais estáveis.
- **Eval:** cada execução faz cerca de 36 chamadas ao modelo, com pausa entre elas e uma nova tentativa em caso de erro, para respeitar os limites do plano gratuito.
- **Se o projeto fosse para produção,** seria preciso um plano pago, um limite de uso por usuário e monitoramento do consumo.

## 6. Responsabilidade

O projeto é acadêmico, desenvolvido e mantido por uma única pessoa. As respostas são informativas e podem conter imprecisões. Em caso de dúvida sobre obrigações fiscais, o usuário deve consultar o Portal do Empreendedor ou um contador.