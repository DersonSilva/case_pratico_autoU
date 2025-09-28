// --- Elementos do DOM ---
const form = document.getElementById("emailForm");
const fileInput = document.getElementById("file");
const fileStatus = document.getElementById("fileStatus");
const fileNameSpan = document.getElementById("fileName");

const resultDiv = document.getElementById("result");
const categorySpan = document.getElementById("category");
const responseSpan = document.getElementById("response");

const analyzeBtn = document.getElementById("analyzeBtn");
const btnText = document.getElementById("btnText");
const btnPlane = document.getElementById("btnPlane");
const btnSpinner = document.getElementById("btnSpinner");

// --- Função para alternar estado de loading do botão ---
function setLoading(isLoading = true) {
  analyzeBtn.disabled = isLoading;
  analyzeBtn.setAttribute("aria-busy", isLoading);

  analyzeBtn.classList.toggle("opacity-80", isLoading);
  analyzeBtn.classList.toggle("cursor-wait", isLoading);

  btnPlane.classList.toggle("hidden", isLoading);
  btnSpinner.classList.toggle("hidden", !isLoading);

  btnText.textContent = isLoading ? "Analisando..." : "Analisar";
}

// --- Função para atualizar preview do arquivo ---
function updateFilePreview() {
  if (fileInput.files.length > 0) {
    fileNameSpan.textContent = fileInput.files[0].name;
    fileStatus.classList.remove("hidden");
  } else {
    fileStatus.classList.add("hidden");
    fileNameSpan.textContent = "";
  }
}

// --- Função para resetar formulário ---
function resetFormElements() {
  form.reset(); // limpa textarea e file input
  fileStatus.classList.add("hidden");
  fileNameSpan.textContent = "";
}

// --- Função principal de envio ---
async function handleSubmit(event) {
  event.preventDefault();

  // Resetando resultado
  resultDiv.classList.remove("hidden");
  categorySpan.textContent = "...";
  responseSpan.textContent = "Analisando...";

  const formData = new FormData();
  const text = document.getElementById("text").value.trim();
  const file = fileInput.files[0];

  if (text) formData.append("text", text);
  if (file) formData.append("file", file);

  try {
    setLoading(true);

    const response = await fetch("/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.error) {
      categorySpan.textContent = "Erro";
      responseSpan.textContent = data.error;
    } else {
      categorySpan.textContent = data.category || "Não definido";
      responseSpan.textContent =
        data.suggested_reply || "Sem resposta sugerida";
    }
  } catch (err) {
    console.error("Erro na requisição:", err);
    categorySpan.textContent = "Erro";
    responseSpan.textContent = "Não foi possível conectar ao servidor.";
  } finally {
    setLoading(false);
    resetFormElements(); // <- limpa textarea e arquivo após envio
  }
}

// --- Event Listeners ---
fileInput.addEventListener("change", updateFilePreview);
form.addEventListener("submit", handleSubmit);
