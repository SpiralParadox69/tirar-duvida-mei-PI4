import pytest

from busca import buscar, carregar_faq, normalizar, radicais


@pytest.fixture(scope="module")
def faq():
    return carregar_faq()


def test_faq_tem_quantidade_minima(faq):
    assert len(faq) >= 20


def test_faq_tem_estrutura_correta(faq):
    for entrada in faq:
        assert {"id", "pergunta", "resposta", "keywords"} <= entrada.keys()


def test_normalizar_remove_acentos_e_maiusculas():
    assert normalizar("Declaração") == "declaracao"


def test_radicais_agrupa_variacoes_da_palavra():
    assert radicais("pagar") == radicais("pagamento")


def test_radicais_ignora_palavras_comuns():
    assert radicais("o que é o DAS") == {"das"}


@pytest.mark.parametrize(
    "pergunta, id_esperado",
    [
        ("quanto eu posso faturar por ano?", 2),
        ("posso atrasar o pagamento do MEI?", 7),
        ("preciso emitir nota fiscal?", 13),
        ("quero fechar meu cnpj", 16),
        ("até quando devo pagar o DAS?", 6),
    ],
)
def test_busca_encontra_entrada_certa(faq, pergunta, id_esperado):
    ids = [entrada["id"] for entrada in buscar(pergunta, faq)]
    assert id_esperado in ids


@pytest.mark.parametrize(
    "pergunta",
    ["qual a capital da França?", "como fazer bolo de chocolate?"],
)
def test_busca_nao_acha_nada_fora_do_tema(faq, pergunta):
    assert buscar(pergunta, faq) == []


def test_busca_respeita_maximo_de_resultados(faq):
    assert len(buscar("limite de faturamento", faq, max_resultados=3)) <= 3