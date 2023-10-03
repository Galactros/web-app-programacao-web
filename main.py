from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import uvicorn 


class Produto(BaseModel):
    codigo: int | None
    nome: str
    preco: float

app = FastAPI()
templates = Jinja2Templates(directory="static")

# Configurando CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="uirses",
    user="uiers",
    password="hudhsahuDSADas243",
    host="postgres",
    port="5432"
)
cursor = conn.cursor()


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse, tags=["root"])
def root_endpoint(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/produtos/")
async def criar_produto(produto: Produto):
    try:
        cursor.execute("INSERT INTO produtos (nome, preco) VALUES (%s, %s) RETURNING codigo;", (produto.nome, produto.preco))
        produto.codigo = cursor.fetchone()[0]
        conn.commit()
        return produto
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/produtos/")
async def listar_produtos():
    try:
        cursor.execute("SELECT codigo, nome, preco FROM produtos;")
        produtos = cursor.fetchall()
        return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/produtos/{codigo}/")
async def atualizar_produto(produto: Produto):
    try:
        cursor.execute("UPDATE produtos SET nome = %s, preco = %s WHERE codigo = %s;", (produto.nome, produto.preco, produto.codigo))
        conn.commit()
        return {"message": f"Produto de código {produto.codigo} atualizado com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/produtos/{codigo}/")
async def excluir_produto(codigo: int):
    try:
        cursor.execute("DELETE FROM produtos WHERE codigo = %s;", (codigo,))
        conn.commit()
        return {"message": f"Produto de código {codigo} excluído com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=80)