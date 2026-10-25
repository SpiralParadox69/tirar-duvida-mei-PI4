import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "backend"))

from assistente import responder  
from busca import normalizar  

CASOS = [
    {"tema": "Faturamento", "pergunta": "quanto eu posso faturar por ano?", "esperado": ["81 000", "81 mil"]},
    {"tema": "Prazos", "pergunta": "até quando devo pagar o DAS?", "esperado": ["dia 20"]},
    {"tema": "Prazos", "pergunta": "quando é o prazo da declaração anual?", "esperado": ["31 de maio"]},
    {"tema": "DAS", "pergunta": "qual o valor do DAS?", "esperado": ["82 05", "87 05"]},
    {"tema": "DAS", "pergunta": "o que acontece se eu atrasar o DAS?", "esperado": ["juros", "multa"]},
    {"tema": "Nota fiscal", "pergunta": "preciso emitir nota fiscal?", "esperado": ["pessoa juridica", "outra empresa"]},
    {"tema": "Desenquadramento", "pergunta": "o que acontece se eu passar mais de 20% do limite?", "esperado": ["retroativ"]},
    {"tema": "Faturamento", "pergunta": "quanto posso exceder o limite sem sair do MEI?", "esperado": ["97 200"]},
    {"tema": "Regras", "pergunta": "posso ter funcionário no MEI?", "esperado": ["um funcionario", "1 funcionario"]},
    {"tema": "Regras", "pergunta": "qual o limite do MEI caminhoneiro?", "esperado": ["251 600"]},
    {"tema": "Abertura/Baixa", "pergunta": "como faço para encerrar meu MEI?", "esperado": ["portal do empreendedor"]},
    {"tema": "Fora do escopo", "pergunta": "qual a capital da França?", "esperado": ["nao encontrei"]},
    {"tema": "Fora do escopo", "pergunta": "como fazer bolo de chocolate?", "esperado": ["nao encontrei"]},
    {"tema": "Robustez", "pergunta": "quanto custa um iPhone?", "esperado": ["nao encontrei", "nao consta", "nao tenho", "nao ha informac"]},
]


def acertou(resposta, esperado):
    texto = normalizar(resposta)
    return any(termo in texto for termo in esperado)


def salvar_relatorio(resultados, taxa, tempo_medio):
    linhas = [
        "# Resultados do eval",
        "",
        f"- Casos: {len(resultados)}",
        f"- Taxa de acerto: {taxa:.0f}%",
        f"- Taxa de erro: {100 - taxa:.0f}%",
        f"- Tempo médio de resposta: {tempo_medio:.1f}s",
        "",
        "| # | Tema | Pergunta | Resultado |",
        "|---|---|---|---|",
    ]
    for i, r in enumerate(resultados, 1):
        status = "OK" if r["ok"] else "FALHOU"
        linhas.append(f"| {i} | {r['tema']} | {r['pergunta']} | {status} |")

    falhas = [r for r in resultados if not r["ok"]]
    if falhas:
        linhas += ["", "## Falhas (para análise)", ""]
        for r in falhas:
            linhas += [
                f"**Pergunta:** {r['pergunta']}",
                "",
                f"**Esperado (qualquer um):** {', '.join(r['esperado'])}",
                "",
                f"**Resposta:** {r['resposta']}",
                "",
            ]

    destino = RAIZ / "docs" / "eval_resultados.md"
    destino.write_text("\n".join(linhas), encoding="utf-8")
    print(f"\nRelatório salvo em {destino}")


def main():
    resultados = []
    for caso in CASOS:
        inicio = time.time()
        try:
            resposta = responder(caso["pergunta"])
        except Exception as erro:
            resposta = f"[ERRO] {erro}"
        duracao = time.time() - inicio

        ok = acertou(resposta, caso["esperado"])
        resultados.append({**caso, "resposta": resposta, "ok": ok, "duracao": duracao})
        print(f"[{'OK' if ok else 'FALHOU'}] {caso['pergunta']} ({duracao:.1f}s)")
        time.sleep(1) 

    taxa = 100 * sum(r["ok"] for r in resultados) / len(resultados)
    tempo_medio = sum(r["duracao"] for r in resultados) / len(resultados)
    print(f"\nTaxa de acerto: {taxa:.0f}% | Taxa de erro: {100 - taxa:.0f}% | Tempo médio: {tempo_medio:.1f}s")
    salvar_relatorio(resultados, taxa, tempo_medio)


if __name__ == "__main__":
    main()