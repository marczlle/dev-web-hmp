document.addEventListener("DOMContentLoaded", async () => {
  async function processIncludes() {
    const includes = document.querySelectorAll('[data-include]');

    for (const el of includes) {
      const file = el.getAttribute("data-include");
      const res = await fetch(file);
      const html = await res.text();
      el.innerHTML = html;
      el.removeAttribute('data-include');

      // Reexecuta os scripts internos do HTML incluído
      const scripts = el.querySelectorAll("script");
      for (const oldScript of scripts) {
        const newScript = document.createElement("script");
        if (oldScript.src) {
          newScript.src = oldScript.src;
        } else {
          newScript.textContent = oldScript.textContent;
        }
        oldScript.parentNode.replaceChild(newScript, oldScript);
      }
    }

    // Verifica recursivamente se há includes aninhados
    if (document.querySelector('[data-include]')) {
      await processIncludes();
    }
  }

  await processIncludes();

  // Emite evento avisando que todos includes terminaram
  document.dispatchEvent(new Event("includesLoaded"));
});
