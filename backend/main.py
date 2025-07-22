import os
from fastapi import FastAPI, HTTPException, Response, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.security import HTTPBearer
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'config', '.env'))

app = FastAPI()

# Carrega credenciais do .env
SENHA = os.getenv("SENHA")
USUARIO = os.getenv("USUARIO")

# Configuração dos diretórios
base_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(base_dir, ".."))

scripts_dir = os.path.join(root_dir, "scripts")
components_dir = os.path.join(root_dir, "components")
pages_dir = os.path.join(root_dir, "pages")
styles_dir = os.path.join(root_dir, "styles")
assets_dir = os.path.join(root_dir, "public", "assets")

# Montando pastas estáticas
app.mount("/scripts", StaticFiles(directory=scripts_dir), name="scripts")
app.mount("/components", StaticFiles(directory=components_dir), name="components")
app.mount("/styles", StaticFiles(directory=styles_dir), name="styles")
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# Montar páginas como estáticas
app.mount("/static", StaticFiles(directory=pages_dir, html=True), name="static")

print(f"USUARIO={USUARIO}, SENHA={SENHA}")

# Função para verificar se o usuário está autenticado
def verificar_autenticacao(request: Request):
    session = request.cookies.get("session")
    if session != "autorizado":
        raise HTTPException(status_code=401, detail="Não autorizado")
    return True

# Rota principal - sempre serve a página index.html
@app.get("/")
def root():
    index_path = os.path.join(pages_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return RedirectResponse("/static/index.html")

# Endpoint de login - processa as credenciais
from fastapi.responses import JSONResponse

@app.post("/login")
async def login(request: Request):
    try:
        data = await request.json()
        print("Recebido do frontend:", data)
        usuario = data.get("usuario", "")
        password = data.get("password", "")
        print(f"usuario: {usuario}, password: {password}")
        print(f"USUARIO esperado: {USUARIO}, SENHA esperada: {SENHA}")

        if usuario != USUARIO:
            print("Usuário incorreto")
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Usuário incorreto"}
            )

        if password != SENHA:
            print("Senha incorreta")
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Senha incorreta"}
            )

        response = JSONResponse(
            content={
                "success": True,
                "message": "Login realizado com sucesso",
                "redirect": "/catalogo"
            }
        )
        response.set_cookie(key="session", value="autorizado", httponly=True, secure=False, samesite="lax")
        print("Login realizado com sucesso")
        return response

    except Exception as e:
        print(f"Erro no login: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": f"Erro no processamento do login: {str(e)}"}
        )

# Rota protegida para o catálogo
@app.get("/catalogo")
def catalogo(request: Request, autenticado: bool = Depends(verificar_autenticacao)):
    catalogo_path = os.path.join(pages_dir, "catálogo.html")
    if os.path.exists(catalogo_path):
        return FileResponse(catalogo_path)
    else:
        # Se não encontrar catálogo.html, tenta catalog.html
        catalog_path = os.path.join(pages_dir, "catalog.html")
        if os.path.exists(catalog_path):
            return FileResponse(catalog_path)
        raise HTTPException(status_code=404, detail="Página do catálogo não encontrada")

# Rota para logout
@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="session")
    return {"success": True, "message": "Logout realizado com sucesso"}

# Rota para verificar se está logado
@app.get("/verify-auth")
def verify_auth(request: Request):
    try:
        verificar_autenticacao(request)
        return {"authenticated": True}
    except HTTPException:
        return {"authenticated": False}

@app.get("/calculadora")
def calculadora(request: Request, autenticado: bool = Depends(verificar_autenticacao)):
    calculadora_path = os.path.join(pages_dir, "calculadora.html")
    if os.path.exists(calculadora_path):
        return FileResponse(calculadora_path)
    raise HTTPException(status_code=404, detail="Página da calculadora não encontrada")

# Rota protegida para receitas
@app.get("/receitas")
def receitas(request: Request, autenticado: bool = Depends(verificar_autenticacao)):
    receitas_path = os.path.join(pages_dir, "receitas.html")
    if os.path.exists(receitas_path):
        return FileResponse(receitas_path)
    raise HTTPException(status_code=404, detail="Página de receitas não encontrada")

# Rotas protegidas para cada produto
for i in range(1, 7):
    @app.get(f"/produto{i}")
    def produto(request: Request, i=i, autenticado: bool = Depends(verificar_autenticacao)):
        produto_path = os.path.join(pages_dir, f"produto{i}.html")
        if os.path.exists(produto_path):
            return FileResponse(produto_path)
        raise HTTPException(status_code=404, detail=f"Produto {i} não encontrado")

# Middleware para debugging 
@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    print(f"Cookies: {request.cookies}")
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    print(f"Usuário configurado: {USUARIO}")
    print(f"Senha configurada: {'*' * len(SENHA) if SENHA else 'NÃO DEFINIDA'}")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)