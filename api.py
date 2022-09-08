from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from analise import balancoMensal, despesas, receitas, receitasAlexis, receitasSilvana, receitasByMonth, getCusto, recursoAvancado, getObjetivos, dashboard, mercado
from recursos import insertRecurso, selectRecursos
from objetivos import insertObjetivo, selectObjetivos
from recurso_objetivo import insertRecursoObjetivo, selectRecursoObjetivos, updateRecursoObjetivo, updateRecursosObjetivos, insertRecursosObjetivos


class Recurso(BaseModel):
    id: str
    nome: str


class Objetivo(BaseModel):
    id: str
    descricao: str


class RecursoObjetivo(BaseModel):
    id: str
    id_recurso: str
    id_objetivo: str
    fixa: bool
    value: float


app = FastAPI()


@app.get("/balanco")
def getBalancoMensal():
    return balancoMensal()


@app.get("/despesas")
def getDespesas():
    return despesas()


@app.get("/receitas")
def getReceitas():
    return receitas()


@app.get("/receitasAlexis")
def getReceitasAlexis():
    return receitasAlexis()


@app.get("/receitasSilvana")
def getReceitasSilvana():
    return receitasSilvana()


@app.get("/receitas/{timestamp}")
def getReceitasByMonth(timestamp: int):
    return receitasByMonth(timestamp)


@app.get("/custo")
def custo():
    return getCusto()


@app.get("/recurso/{recurso}")
def getRecursoAvancado(recurso):
    return recursoAvancado(recurso)


@app.get("/objetivos")
def objetivos():
    return getObjetivos()


@app.get("/dashboard")
def getDasboard():
    return dashboard()


@app.get("/mercado")
def getMercado():
    return mercado()


@app.post("/recurso")
def setRecurso(recurso: Recurso):
    insertRecurso(recurso)


@app.post("/objetivo")
def setRecurso(objetivo: Objetivo):
    insertObjetivo(objetivo)


@app.post("/recursoObjetivo")
def setRecurso(recurso_objetivo: RecursoObjetivo):
    insertRecursoObjetivo(recurso_objetivo)


@app.get("/recursos")
def getRecursos():
    return selectRecursos()


@app.get("/objeitvos")
def getObjetivos():
    return selectObjetivos()


@app.get("/recursoObjetivos")
def getRecursoObjetivos():
    return selectRecursoObjetivos()


@app.put("/recursoObjetivo")
def atualizaRecursoObjetivos(recurso_objetivo: RecursoObjetivo):
    return updateRecursoObjetivo(recurso_objetivo)


@app.put("/recursosObjetivos")
def atualizaRecursosObjetivos(recurso_objetivo: List[RecursoObjetivo]):
    return updateRecursosObjetivos(recurso_objetivo)


@app.post("/recursosObjetivos")
def createRecursosObjetivos(recurso_objetivo: List[RecursoObjetivo]):
    return insertRecursosObjetivos(recurso_objetivo)
