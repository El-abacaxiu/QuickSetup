const btnTema = document.getElementById("toggle-theme");
let tema = "escuro";

btnTema.addEventListener("click", () => {
  document.body.classList.toggle("claro");

  tema = tema === "escuro" ? "claro" : "escuro";
  btnTema.textContent = tema === "escuro" ? "🌙 Modo Escuro" : "☀️ Modo Claro";
});
