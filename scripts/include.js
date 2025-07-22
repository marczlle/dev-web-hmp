document.addEventListener("DOMContentLoaded", async () => {
  async function processIncludes() {
    const includes = document.querySelectorAll('[data-include]');

    for (const el of includes) {
      const file = el.getAttribute("data-include");
      const res = await fetch(file);
      const html = await res.text();
      el.innerHTML = html;
      el.removeAttribute('data-include'); // Remove o atributo pra evitar loops infinitos

      // Ativa o listener se o include for do login
      if (file.includes('login.html')) {
        ativarLoginListener();
      }
    }

    // Se ainda existirem novos includes (aninhados), chama de novo
    if (document.querySelector('[data-include]')) {
      await processIncludes();
    }
  }

  await processIncludes();
});

function ativarLoginListener() {
  const loginForm = document.getElementById('loginForm');
  if (loginForm && !loginForm.dataset.listener) {
    loginForm.addEventListener('submit', realizarLogin);
    loginForm.dataset.listener = "true"; // evita adicionar múltiplas vezes
  }
}