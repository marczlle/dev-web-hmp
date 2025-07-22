
async function realizarLogin(event) {
    event.preventDefault();

    // Pega os valores dos campos de login
    const usuario = document.getElementById('usuario').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!usuario || !password) {
        alert('Por favor, preencha todos os campos');
        return;
    }

    try {
        console.log('Enviando dados de login...');

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                usuario: usuario,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            console.log('Login bem-sucedido');
            alert('Login realizado com sucesso!');

            // Redireciona para o catálogo
            window.location.href = '/catalogo';
        } else {
            console.error('Erro no login:', data.detail);
            alert(`Erro: ${data.detail}`);
        }

    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro de conexão. Tente novamente.');
    }
}

// Função para verificar se está logado (opcional)
async function verificarAutenticacao() {
    try {
        const response = await fetch('/verify-auth');
        const data = await response.json();

        if (!data.authenticated && window.location.pathname === '/catalogo') {
            window.location.href = '/';
        }

        return data.authenticated;
    } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        return false;
    }
}

// Função para logout
async function realizarLogout() {
    try {
        const response = await fetch('/logout', {
            method: 'POST'
        });

        if (response.ok) {
            alert('Logout realizado com sucesso');
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Erro no logout:', error);
    }
}

// Adiciona event listener quando a página carregar
document.addEventListener('DOMContentLoaded', function () {
    // Para o formulário de login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', realizarLogin);
    }

    // Para botão de logout (se existir)
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', realizarLogout);
    }

    // Verifica autenticação em páginas protegidas
    if (window.location.pathname === '/catalogo') {
        verificarAutenticacao();
    }
});