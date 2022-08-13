from fastapi import FastAPI
from analise import balancoMensal, despesas, receitas, receitasAlexis, receitasSilvana, receitasByMonth, getCusto, recursoAvancado, getObjetivos, dashboard


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
