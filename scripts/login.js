console.log("login.js carregado!");

async function realizarLogin(event) {
    event.preventDefault();

    const usuario = document.getElementById('usuario').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!usuario || !password) {
        alert('Por favor, preencha todos os campos');
        return;
    }

    try {
        console.log({ usuario, password });
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usuario, password }),
            credentials: 'same-origin' // ESSENCIAL para o cookie funcionar!
        });

        const data = await response.json();

        if (response.ok && data.success) {
            window.location.href = data.redirect;
        } else {
            alert(data.detail || data.message || 'Usuário ou senha incorretos');
        }
    } catch (error) {
        alert('Erro ao tentar fazer login. Tente novamente.');
        console.error(error);
    }
}

async function realizarLogout() {
    try {
        const response = await fetch('/logout', {
            method: 'POST',
            credentials: 'same-origin'
        });

        if (response.ok) {
            alert('Logout realizado com sucesso');
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Erro no logout:', error);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', realizarLogin);
    }

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', realizarLogout);
    }
});