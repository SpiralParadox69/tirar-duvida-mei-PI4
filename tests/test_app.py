import pytest

import app as modulo_app
from assistente import MSG_SEM_CONTEXTO, montar_contexto, responder


@pytest.fixture
def cliente():
    modulo_app.app.config["TESTING"] = True
    return modulo_app.app.test_client()


def test_pergunta_valida_devolve_resposta(cliente, monkeypatch):
    monkeypatch.setattr(modulo_app, "responder", lambda pergunta: "resposta falsa")
    resposta = cliente.post("/perguntar", json={"pergunta": "teste"})
    assert resposta.status_code == 200
    assert resposta.get_json()["resposta"] == "resposta falsa"


def test_pergunta_vazia_retorna_400(cliente):
    resposta = cliente.post("/perguntar", json={"pergunta": "   "})
    assert resposta.status_code == 400


def test_pergunta_muito_longa_retorna_400(cliente):
    resposta = cliente.post("/perguntar", json={"pergunta": "a" * 301})
    assert resposta.status_code == 400


def test_corpo_invalido_retorna_400(cliente):
    resposta = cliente.post("/perguntar", data="isso nao e json")
    assert resposta.status_code == 400


def test_falha_no_modelo_retorna_500(cliente, monkeypatch):
    def falhar(pergunta):
        raise RuntimeError("falha simulada")

    monkeypatch.setattr(modulo_app, "responder", falhar)
    resposta = cliente.post("/perguntar", json={"pergunta": "teste"})
    assert resposta.status_code == 500


def test_pagina_inicial_carrega(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200


def test_sem_contexto_nao_chama_o_modelo():
    assert responder("qual a capital da França?") == MSG_SEM_CONTEXTO


def test_montar_contexto_formata_perguntas_e_respostas():
    entradas = [{"pergunta": "P1?", "resposta": "R1."}]
    assert montar_contexto(entradas) == "P1: P1?\nR: R1."