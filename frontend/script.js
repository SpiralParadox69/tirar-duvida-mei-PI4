const formulario = document.getElementById("formulario");
const campoPergunta = document.getElementById("pergunta");
const botao = document.getElementById("botao");
const areaMensagens = document.getElementById("mensagens");

function adicionarMensagem(texto, tipo) {
  const div = document.createElement("div");
  div.className = "mensagem " + tipo;
  div.textContent = texto;
  areaMensagens.appendChild(div);
  areaMensagens.scrollTop = areaMensagens.scrollHeight;
  return div;
}

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const pergunta = campoPergunta.value.trim();
  if (!pergunta) return;

  adicionarMensagem(pergunta, "usuario");
  campoPergunta.value = "";
  botao.disabled = true;

  const aviso = adicionarMensagem("Digitando...", "assistente digitando");

  try {
    const resposta = await fetch("/perguntar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta: pergunta }),
    });
    const dados = await resposta.json();
    aviso.remove();

    if (resposta.ok) {
      adicionarMensagem(dados.resposta, "assistente");
    } else {
      adicionarMensagem(dados.erro || "Ocorreu um erro.", "erro");
    }
  } catch (erro) {
    aviso.remove();
    adicionarMensagem("Não foi possível conectar ao servidor.", "erro");
  }

  botao.disabled = false;
  campoPergunta.focus();
});