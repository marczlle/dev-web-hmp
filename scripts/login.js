async function validarLogin(event) {
    event.preventDefault();

    const usuario = document.getElementById("usuario-login").value;
    const senha = document.getElementById("senha-login").value;

    document.getElementById("error-usuario-login").textContent = "";
    document.getElementById("error-senha-login").textContent = "";

    try {
        const res = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                usuario: usuario,
                password: senha
            })
        });

        if (res.ok) {
            window.location.href = "/catálogo.html";
        } else {
            const error = await res.json();
            if (error.detail === "Usuário incorreto") {
                document.getElementById("error-usuario-login").textContent = "Usuário incorreto";
            } else if (error.detail === "Senha incorreta") {
                document.getElementById("error-senha-login").textContent = "Senha incorreta";
            } else {
                alert("Erro desconhecido.");
            }
        }
    } catch (e) {
        alert("Erro ao conectar com o servidor.");
    }
}

const form = document.getElementById("form-login");
if (form) {
    form.addEventListener("submit", validarLogin);
} else {
    console.error("Formulário #form-login não encontrado!");
}
