import json
import re
import unicodedata
from pathlib import Path

CAMINHO_FAQ = Path(__file__).resolve().parent.parent / "data" / "mei_faq.json"

STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "de", "do", "da", "dos", "em", "no",
    "na", "nos", "nas", "por", "para", "com", "e", "ou", "que", "se", "eu",
    "meu", "minha", "posso", "pode", "como", "qual", "quais", "quando",
    "tenho", "ser", "ao", "aos", "mais", "mas", "ja", "sao", "mei",
}


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", texto)


def radicais(texto):
    palavras = [p for p in normalizar(texto).split() if p not in STOPWORDS]
    return {p[:4] for p in palavras}


def carregar_faq(caminho=CAMINHO_FAQ):
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def buscar(pergunta, faq, max_resultados=3):
    radicais_pergunta = radicais(pergunta)
    resultados = []

    for entrada in faq:
        radicais_keywords = radicais(" ".join(entrada["keywords"]))
        radicais_texto = radicais(entrada["pergunta"])
        pontos = 2 * len(radicais_pergunta & radicais_keywords)
        pontos += len(radicais_pergunta & (radicais_texto - radicais_keywords))

        if pontos >= 2:
            resultados.append((pontos, entrada))

    resultados.sort(key=lambda item: item[0], reverse=True)
    return [entrada for _, entrada in resultados[:max_resultados]]


if __name__ == "__main__":
    faq = carregar_faq()
    print(f"FAQ carregado: {len(faq)} perguntas. Digite 'sair' para encerrar.\n")
    while True:
        pergunta = input("Pergunta: ")
        if pergunta.strip().lower() == "sair":
            break
        achadas = buscar(pergunta, faq)
        if not achadas:
            print("  Nada encontrado.\n")
        for entrada in achadas:
            print(f"  [{entrada['id']}] {entrada['pergunta']}")
        print()