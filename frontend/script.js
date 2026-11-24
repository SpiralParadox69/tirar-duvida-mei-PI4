const formulario = document.getElementById("formulario");
const campoPergunta = document.getElementById("pergunta");
const botao = document.getElementById("botao");
const areaMensagens = document.getElementById("mensagens");
const areaSugestoes = document.getElementById("sugestoes");

function adicionarMensagem(texto, tipo) {
  const div = document.createElement("div");
  div.className = "mensagem " + tipo;
  div.textContent = texto;
  areaMensagens.appendChild(div);
  areaMensagens.scrollTop = areaMensagens.scrollHeight;
  return div;
}

async function enviarPergunta(pergunta) {
  adicionarMensagem(pergunta, "usuario");
  campoPergunta.value = "";
  botao.disabled = true;
  areaSugestoes.hidden = true;

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
}

formulario.addEventListener("submit", (evento) => {
  evento.preventDefault();
  const pergunta = campoPergunta.value.trim();
  if (pergunta) enviarPergunta(pergunta);
});

areaSugestoes.addEventListener("click", (evento) => {
  const sugestao = evento.target.closest(".sugestao");
  if (sugestao && !botao.disabled) enviarPergunta(sugestao.textContent);
});