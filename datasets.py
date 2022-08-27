from drive import drive
import pandas as pd
from datetime import datetime, date
import json

file = open("file_ids.json")
keys = json.load(file)
file.close()


def mercado_dataframe():
    mercadofile = drive().CreateFile({"id": keys["MERCADO"]})
    mercadofile.GetContentFile("mercado.csv", mimetype="text/csv")
    return pd.read_csv("mercado.csv", delimiter=",")


def objetivos_dataframe():
    objetivosfile = drive().CreateFile({"id": keys["OBJETIVOS"]})
    objetivosfile.GetContentFile("objetivos.csv", mimetype="text/csv")
    return pd.read_csv("objetivos.csv", delimiter=";")


def contas_dataframe():
    contasfile = drive().CreateFile({"id": keys["CONTAS"]})
    contasfile.GetContentFile("contas.csv", mimetype="text/csv")
    return pd.read_csv("contas.csv", delimiter=";")


def transacoes_dataframe():
    recursos = ['Silvana', 'Alexis']
    transacoesfile = drive().CreateFile({"id": keys["TRANSACOES"]})
    transacoesfile.GetContentFile("transacoes.csv", mimetype="text/csv")
    transacoesdf = pd.read_csv("transacoes.csv", delimiter=";")
    transacoesdf['datetime'] = pd.to_datetime(
        transacoesdf.Data, format="%d/%m/%Y")
    transacoesdf['timestamp'] = transacoesdf.datetime.astype('int64') // 10**9
    transacoesdf["month_year"] = transacoesdf.timestamp.map(
        lambda x: datetime(datetime.fromtimestamp(x).year,
                           datetime.fromtimestamp(x).month, 1))
    transacoesdf['recurso'] = transacoesdf.Conta.map(
        lambda x: x.split(" ")[len(x.split(" ")) - 1] if any(ext in x for ext in recursos) else None)
    return transacoesdf
