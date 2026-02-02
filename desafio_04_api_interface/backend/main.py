from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="ANS Data API")

# Habilitar CORS para o Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "ans.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Models
class Operadora(BaseModel):
    registro_ans: Optional[str]
    cnpj: str
    razao_social: str
    modalidade: Optional[str]
    uf: Optional[str]

class Despesa(BaseModel):
    cnpj: str
    data_referencia: str
    ano: int
    trimestre: str
    valor: float

class PaginatedResponse(BaseModel):
    data: List[dict]
    total: int
    page: int
    limit: int

# Routes

@app.get("/api/operadoras", response_model=PaginatedResponse)
async def get_operadoras(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None
):
    conn = get_db_connection()
    offset = (page - 1) * limit
    
    query = "SELECT * FROM operadoras"
    params = []
    
    if search:
        query += " WHERE razao_social LIKE ? OR cnpj LIKE ?"
        params.extend([f"%{search}%", f"%{search}%"])
    
    # Total count for pagination
    count_query = f"SELECT COUNT(*) FROM ({query})"
    total = conn.execute(count_query, params).fetchone()[0]
    
    # Paginated data
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    return {
        "data": [dict(row) for row in rows],
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/operadoras/{cnpj}")
async def get_operadora_detail(cnpj: str):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM operadoras WHERE cnpj = ?", (cnpj,)).fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    
    return dict(row)

@app.get("/api/operadoras/{cnpj}/despesas")
async def get_operadora_despesas(cnpj: str):
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM despesas WHERE cnpj = ? ORDER BY data_referencia DESC", (cnpj,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/estatisticas")
async def get_estatisticas():
    conn = get_db_connection()
    
    # Estatísticas simples (cached em memória na vida real, aqui calculamos para o demo)
    total_despesas = conn.execute("SELECT SUM(ValorDespesas) FROM despesas").fetchone()[0]
    media_despesa = conn.execute("SELECT AVG(ValorDespesas) FROM despesas").fetchone()[0]
    
    # Top 5 operadoras com mais despesas
    top_5_query = """
        SELECT o.razao_social, SUM(d.ValorDespesas) as total
        FROM despesas d
        JOIN operadoras o ON d.cnpj = o.cnpj
        GROUP BY d.cnpj
        ORDER BY total DESC
        LIMIT 5
    """
    top_5 = conn.execute(top_5_query).fetchall()
    
    # Distribuição por UF para o gráfico
    uf_query = """
        SELECT o.uf, SUM(d.ValorDespesas) as total
        FROM despesas d
        JOIN operadoras o ON d.cnpj = o.cnpj
        WHERE o.uf IS NOT NULL AND o.uf != 'N/A'
        GROUP BY o.uf
        ORDER BY total DESC
    """
    uf_dist = conn.execute(uf_query).fetchall()
    
    conn.close()
    
    return {
        "total_geral": total_despesas,
        "media_geral": media_despesa,
        "top_5": [dict(row) for row in top_5],
        "distribuicao_uf": [dict(row) for row in uf_dist]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
