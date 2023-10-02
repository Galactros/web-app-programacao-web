from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import uvicorn 

app = FastAPI()

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
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


@app.post("/produtos/")
async def criar_produto(nome: str, preco: float):
    try:
        cursor.execute("INSERT INTO produtos (nome, preco) VALUES (%s, %s) RETURNING codigo;", (nome, preco))
        codigo = cursor.fetchone()[0]
        conn.commit()
        return {"codigo": codigo, "nome": nome, "preco": preco}
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
async def atualizar_produto(codigo: int, nome: str, preco: float):
    try:
        cursor.execute("UPDATE produtos SET nome = %s, preco = %s WHERE codigo = %s;", (nome, preco, codigo))
        conn.commit()
        return {"message": f"Produto de código {codigo} atualizado com sucesso."}
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