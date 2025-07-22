import os
from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'config', '.env'))

SENHA = os.getenv("SENHA")
USUARIO = os.getenv("USUARIO")


app = FastAPI()

SENHA = os.getenv("SENHA")
USUARIO = os.getenv("USUARIO")

base_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(base_dir, ".."))

scripts_dir = os.path.join(root_dir, "scripts")
components_dir = os.path.join(root_dir, "components")
pages_dir = os.path.join(root_dir, "pages")
styles_dir = os.path.join(root_dir, "styles")
assets_dir = os.path.join(root_dir, "public", "assets")

# Montando pastas estáticas (apontando para /static)
app.mount("/scripts", StaticFiles(directory=scripts_dir), name="scripts")
app.mount("/components", StaticFiles(directory=components_dir), name="components")
app.mount("/styles", StaticFiles(directory=styles_dir), name="styles")
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# MONTAR pages/ em /static para servir HTMLs, CSS, JS etc
app.mount("/static", StaticFiles(directory=pages_dir, html=True), name="static")

# Redireciona / para /static/index.html
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")

# Login endpoint POST
@app.post("/login")
async def login(request: Request, response: Response):
    data = await request.json()
    usuario = data.get("usuario")
    password = data.get("password")
    
    print(f"Recebido -> usuario: '{usuario}', senha: '{password}'")
    
    if usuario != USUARIO:
        raise HTTPException(status_code=401, detail="Usuário incorreto")

    if password != SENHA:
        raise HTTPException(status_code=401, detail="Senha incorreta")

    response.set_cookie(key="session", value="autorizado", httponly=True)
    return {"success": True}
