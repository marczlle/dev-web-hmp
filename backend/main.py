import os
from fastapi import FastAPI, HTTPException, Depends, Response, Cookie, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import logging


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'config', '.env'))

app = FastAPI()

SENHA = os.getenv("SENHA")
USUARIO = os.getenv("USUARIO")

base_dir = os.path.dirname(__file__)
pages_dir = os.path.abspath(os.path.join(base_dir, '..', 'pages'))
components_dir = os.path.abspath(os.path.join(base_dir, '..', 'components'))

@app.get("/")
def root():
    return FileResponse(os.path.join(pages_dir, "index.html"))

# tenho que terminar isso aqui
@app.post("/login")
async def login(request: Request, response: Response):
    data = await request.json()
    password = data.get("password")
    if password == SENHA:
        response.set_cookie(key="session", value="autorizado", httponly=True)
        return {"success": True}
    raise HTTPException(status_code=401, detail="Senha incorreta")