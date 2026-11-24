# Análise de impacto

Projeto Integrador IV — Tira-Dúvidas do MEI
Autor: Felipe Cabral Coelho Pinho

## 1. Comunidade impactada

Microempreendedores Individuais (MEIs), principalmente os que trabalham de forma autônoma (comércio, serviços, alimentação) e não têm recursos para contratar assessoria contábil. Para esse público, termos como DAS, DASN-SIMEI e desenquadramento são difíceis de entender, e o desconhecimento das obrigações leva à inadimplência e ao cancelamento do CNPJ.

Conforme levantamentos do Sebrae citados no relatório C1, o Brasil já tem mais de 13 milhões de MEIs ativos, e o próprio Governo Federal lançou o programa Desenrola MEI (Edital nº 9/2026) para renegociar dívidas da categoria. O problema, portanto, é amplo.

## 2. O que esta análise mede

O relatório C1 definiu três indicadores simples. Esta análise mostra o resultado de cada um e compara o estado do projeto **antes** e **depois** das melhorias da C3. O "antes" é a primeira execução do eval completo de 36 casos, já com o FAQ ampliado para 39 entradas; o "depois" é a execução final, depois da correção das palavras-chave do FAQ.

Os números vêm do eval automatizado (`tests/eval_ia.py`), que faz perguntas reais ao modelo e confere as respostas. O relatório completo de cada execução está em `docs/eval_baseline.md` (antes) e `docs/eval_resultados.md` (depois).

## 3. Resultados dos indicadores

### Indicador 1 — Taxa de acerto

Percentual das 36 perguntas do eval que o assistente respondeu corretamente.

| | Antes (baseline) | Depois |
|---|---|---|
| Casos no eval | 36 | 36 |
| Respostas corretas | 34 (94%) | 36 (100%) |

### Indicador 2 — Taxa de erro

É o inverso do indicador 1: respostas erradas, vagas ou fora do FAQ.

| | Antes (baseline) | Depois |
|---|---|---|
| Taxa de erro | 6% | 0% |

### Indicador 3 — Cobertura de temas

Checklist dos temas mais importantes do MEI e as entradas do FAQ que os cobrem:

| Tema | Presente? | Entradas do FAQ (id) |
|---|---|---|
| DAS | Sim | 5, 6, 7, 20, 32 |
| Prazos | Sim | 6, 8 |
| Faturamento | Sim | 2, 3, 4, 9, 23, 36 |
| Nota fiscal | Sim | 13, 30 |
| Desenquadramento | Sim | 9, 10, 37 |

**Cobertura: 5 de 5 temas (100%).** O FAQ passou de 25 para 39 entradas na C3, incluindo parcelamento de dívidas, multa por atraso, certificado do MEI, alvará, carência de benefícios do INSS, aposentadoria e privacidade de dados.

### Indicador complementar — Acerto da busca

Mede se a busca por palavras-chave trouxe a entrada correta do FAQ, independentemente da resposta final.

| | Antes (baseline) | Depois |
|---|---|---|
| Acerto da busca | 83% (30/36) | 92% (33/36) |

## 4. O que os números mostram

- **O assistente respondeu corretamente a quase todas as perguntas** do eval no estado inicial. As duas respostas erradas vinham de falhas da **busca**, não do modelo: a busca não encontrou a entrada certa para "tem como pagar em prestações?" e "vendi 90 mil no ano, e agora?", porque essas frases não usam as palavras cadastradas no FAQ. Foram corrigidas adicionando palavras-chave às entradas de parcelamento e de excesso do limite.
- **O prompt de sistema segurou o modelo quando a busca falhou.** Em perguntas fora do tema em que a busca trouxe entradas sem relação (como "quanto custa um carro novo?" e imposto de renda de pessoa física), o modelo respondeu que não encontrou a informação, em vez de inventar. O mesmo vale para as tentativas de prompt injection testadas.
- **Depois das correções, a taxa de acerto subiu de 94% para 100% e a de busca de 83% para 92%.** A melhora veio de ajustar palavras-chave do FAQ: foram adicionadas palavras às entradas de parcelamento e de excesso do limite, e foi retirada a palavra "quanto" das keywords de duas entradas, que fazia a busca trazer entradas sem relação para perguntas como "quanto custa um iPhone?".
- **Restam 3 casos em que a busca não trouxe o resultado esperado**, todos de perguntas fora do tema: "quanto custa um carro novo?", "como declarar imposto de renda de pessoa física?" e o pedido para contar uma piada. Nos três, a busca trouxe entradas sem relação por coincidência de palavras, mas a **resposta final saiu correta**, porque o prompt de sistema impediu o modelo de usar o contexto errado.
- **A busca é o ponto mais fraco do projeto.** A busca por palavras-chave não entende sinônimos nem linguagem informal, e o uso dos 4 primeiros caracteres das palavras gera alguns falsos positivos (por exemplo, "conte" e "contador"). Uma melhoria futura seria trocar a busca por embeddings.

## 5. Impacto esperado

O assistente pode reduzir a dependência de um contador para dúvidas básicas, o que importa para quem não pode pagar por assessoria. Ele funciona a qualquer hora, responde em linguagem simples e indica o Portal do Empreendedor ou um contador quando não tem a informação. Isso ajuda a prevenir erros comuns, como atrasar o DAS, esquecer a declaração anual (prazo de 31 de maio) ou ultrapassar o limite de faturamento sem perceber.

## 6. Limites desta análise

Para a análise ser honesta, é preciso registrar o que ela **não** mostra:

- Os 36 casos do eval foram escritos pelo próprio autor. Eles medem se o sistema acerta perguntas conhecidas, não como pessoas reais perguntam.
- As correções de palavras-chave foram feitas justamente nos casos que falharam no eval. Por isso, o 100% mostra que esses casos foram resolvidos, mas **não garante** o mesmo desempenho em perguntas novas. É por isso que o indicador de acerto da busca (89%) é mais informativo do que o de resposta.
- Um dos critérios do eval foi ajustado depois de ver o resultado: no caso do pedido para contar uma piada, o modelo recusou corretamente ("não posso atender a esse pedido"), mas o eval só aceitava a frase "não encontrei". O critério passou a aceitar as duas recusas. A resposta do modelo não mudou, apenas o eval ficou menos rígido. O modelo também não responde sempre igual, então os percentuais podem variar um pouco entre execuções.
- A conferência da resposta é automática: procura termos esperados no texto. Uma resposta pode conter o termo certo e ainda assim estar mal explicada, e o contrário também pode acontecer.
- O projeto **não foi testado com usuários reais**. Portanto, o impacto descrito na seção 5 é esperado, não medido. Como próximo passo, seria preciso coletar perguntas reais de MEIs e medir a satisfação.
- O conteúdo do FAQ foi curado a partir de fontes oficiais consultadas em 2026. Se as regras mudarem (por exemplo, o limite de faturamento), o arquivo precisa ser atualizado manualmente.
- Em uma entrada (salário-maternidade) as fontes consultadas divergiram sobre a carência, e por isso a resposta orienta o usuário a conferir no Meu INSS.