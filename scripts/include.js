document.addEventListener("DOMContentLoaded", async () => {
  async function processIncludes() {
    const includes = document.querySelectorAll('[data-include]');
    
    for (const el of includes) {
      const file = el.getAttribute("data-include");
      const res = await fetch(file);
      const html = await res.text();
      el.innerHTML = html;
      el.removeAttribute('data-include'); // Remove o atributo pra evitar loops infinitos
    }

    // Se ainda existirem novos includes (aninhados), chama de novo
    if (document.querySelector('[data-include]')) {
      await processIncludes();
    }
  }

  await processIncludes();
});
