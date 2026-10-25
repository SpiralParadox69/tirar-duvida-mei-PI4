from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from assistente import responder

PASTA_FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
LIMITE_CARACTERES = 300  

app = Flask(__name__, static_folder=str(PASTA_FRONTEND), static_url_path="")


@app.route("/")
def inicio():
    return send_from_directory(PASTA_FRONTEND, "index.html")


@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.get_json(silent=True) or {}
    pergunta = str(dados.get("pergunta", "")).strip()

    if not pergunta:
        return jsonify({"erro": "Digite uma pergunta."}), 400
    if len(pergunta) > LIMITE_CARACTERES:
        return jsonify(
            {"erro": f"A pergunta pode ter no máximo {LIMITE_CARACTERES} caracteres."}
        ), 400

    try:
        resposta = responder(pergunta)
    except Exception as erro:
        print(f"Erro ao consultar o modelo: {erro}")
        return jsonify(
            {"erro": "Não consegui responder agora. Tente novamente em instantes."}
        ), 500

    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)