from logging.handlers import DatagramHandler
from numpy import int64
import json
import pandas as pd
from datetime import datetime, date
from datasets import mercado_dataframe, objetivos_dataframe, contas_dataframe, transacoes_dataframe
from recursos import selectRecursos

df = transacoes_dataframe()


def balancoMensal():
    return df['Valor'].sum()


def despesas():
    despesas = df.query('Valor < 0')
    return despesas['Valor'].sum()


def receitas():
    receitas = df.query('Valor > 0')
    return receitas['Valor'].sum()


def receitasAlexis():

    receitasAlexis = df.query('Alexis == True')
    receitasAlexis = receitasAlexis.query('Valor > 0')
    return receitasAlexis['Valor'].sum()


def receitasSilvana():

    receitasSilvana = df.query('Silvana == True')
    receitasSilvana = receitasSilvana.query('Valor > 0')
    return receitasSilvana['Valor'].sum()


def receitasByMonth(timestamp):
    recursos = [recurso for recurso in selectRecursos()]
    print(recursos)

    isCurrentMonth = True

    if df.empty:
        return []

    desired_month_year = datetime.fromtimestamp(timestamp)

    previous_desired_month_year = datetime(
        desired_month_year.year, desired_month_year.month - 1, 1)

    most_recent = datetime.fromtimestamp(df.timestamp.max())

    previous_most_recent = datetime(most_recent.year, most_recent.month - 1, 1)

    df['is_desired_month_year'] = df['month_year'].map(
        lambda x: x) == datetime(datetime.fromtimestamp(timestamp).year,
                                 datetime.fromtimestamp(timestamp).month, 1)  # desired_month_year.month + desired_month_year.year

    df['is_previous_desired_month_year'] = df['month_year'].map(
        lambda x: x) == datetime(datetime.fromtimestamp(previous_desired_month_year.timestamp()).year,
                                 datetime.fromtimestamp(previous_desired_month_year.timestamp()).month, 1)  # previous_desired_month_year.month + previous_desired_month_year.year

    df['most_recent'] = df['month_year'].map(
        lambda x: x) == datetime(datetime.fromtimestamp(most_recent.timestamp()).year,
                                 datetime.fromtimestamp(most_recent.timestamp()).month, 1)  # most_recent.month + most_recent.year

    df['previous_most_recent'] = df['month_year'].map(
        lambda x: x) == datetime(datetime.fromtimestamp(previous_most_recent.timestamp()).year,
                                 datetime.fromtimestamp(previous_most_recent.timestamp()).month, 1)  # previous_most_recent.month + previous_most_recent.year

    tm = df.query('is_desired_month_year == True')
    pdm = df.query('is_previous_desired_month_year == True')
    mr = df.query('most_recent == True')
    pmr = df.query('previous_most_recent == True')

    if tm.empty:
        isCurrentMonth = False
        pdm = pmr
        tm = mr

    tm = tm.query('Valor > 0')
    pdm = pdm.query('Valor > 0')

    groupedpmr = pdm.groupby("recurso")
    grouped = tm.groupby("recurso")

    ts = timestamp if isCurrentMonth else df.timestamp.max().item()
    pts = previous_desired_month_year.timestamp(
    ) if isCurrentMonth else previous_most_recent.timestamp()

    desired = json.loads(grouped['Valor'].sum().to_json())
    previous = json.loads(groupedpmr['Valor'].sum().to_json())

    lista = list(map(lambda x: {
        'name': x['nome'],
        'id': x['id'],
        'previous': {'value': previous[x['nome']], 'timestamp': pts*1000},
        'timestamp': ts*1000,
        'value': desired[x['nome']]
    }, recursos))

    return {'isDesired': isCurrentMonth, 'recursos': lista}


def getCusto():

    only_debits = df.query('Valor < 0')
    cost = only_debits["Valor"].sum() / len(df['month_year'].unique()) * -1
    return {'custo': cost}


def recursoAvancado(recurso):
    ha_um_ano = datetime(datetime.now().year - 1,
                         datetime.now().month, 1).timestamp()
    ultimos_doze_meses = df.query(f"timestamp > {ha_um_ano}")

    receitas_total = ultimos_doze_meses.query("Valor > 0")['Valor'].sum()

    dfrecurso = ultimos_doze_meses.query(f'recurso == "{recurso}"')
    dfrecurso = dfrecurso.sort_values(by='timestamp')

    meses_referencia_count = len(dfrecurso['month_year'].unique())

    dfdespesas = dfrecurso.query('Valor < 0')

    dfreceitas = dfrecurso.query('Valor > 0')

    totalpassivo = dfreceitas.query(
        'Subcategoria == "Rendimentos" | Subcategoria == "Proventos" | Subcategoria == "JCP"')

    receitas_agrupadas = dfreceitas.groupby('month_year')
    despesas_agrupadas = dfdespesas.groupby('month_year')

    variacao_despesas_soma = list(despesas_agrupadas['Valor'].sum())
    variacao_despesas = 0

    for previous, current in zip(variacao_despesas_soma, variacao_despesas_soma[1:]):

        variacao_despesas += (current - previous) * 100 / current

    lista = list(receitas_agrupadas['Valor'].sum())

    maxValue = receitas_agrupadas["Valor"].sum().max()
    idMaxValue = receitas_agrupadas["Valor"].sum().idxmax()
    timestampMaior = dfdespesas.query(f'month_year == "{idMaxValue}"')[
        'timestamp'].values[0].item()

    variacao = 0

    for previous, current in zip(lista, lista[1:]):
        variacao += (current - previous) * 100 / current

    return {
        'variacao': variacao,
        "totalReceitas": dfreceitas['Valor'].sum(),
        "totalDespesas": dfdespesas['Valor'].sum(),
        "passivoAcumulado": totalpassivo['Valor'].sum(),
        "maiorRenda": maxValue,
        'timestampMaior': timestampMaior*1000,
        'variacaoDespesas': variacao_despesas,
        "mesesReferencia": meses_referencia_count,
        "porcentagemReceitas": dfreceitas['Valor'].sum() / receitas_total * 100
    }


def getObjetivos():
    objdf = objetivos_dataframe()

    objetivos_agrupados = objdf.groupby('Descricao')
    objetivos = []
    for name, group in objetivos_agrupados:
        group = group.groupby('Recurso')
        recursos = []
        for r, g in group:
            recursos.append(json.loads(g[['Valor', 'Fixa', 'Recurso']
                                         ].to_json(orient='records'))[0])

        objetivos.append({'descricao': name, 'recursos': recursos})

    return objetivos


def dashboard():
    contasdf = contas_dataframe()
    print(contasdf)

    ha_um_ano = datetime(datetime.now().year - 1,
                         datetime.now().month, 1).timestamp()

    ano_atras = df.query(f"timestamp > {ha_um_ano}")
    meses_referencia_count = len(ano_atras['month_year'].unique())

    despesas = ano_atras.query('Valor < 0')['Valor'].sum()
    receitas = ano_atras.query('Valor > 0')['Valor'].sum()

    max_time = contasdf['timestamp'].max()
    contasdf = contasdf.query(f'timestamp == {max_time}')
    print(contasdf)

    reserva = contasdf.query('conta == "Guardado Silvana"')['valor'].sum()
    reserva2 = contasdf.query('conta == "Guardado Alexis"')['valor'].sum()

    return {
        'despesas': despesas / meses_referencia_count * -1,
        'receitas': receitas / meses_referencia_count,
        'reserva': reserva + reserva2
    }


def mercado():
    mercadodf = mercado_dataframe()
    mercadodf['datetime'] = pd.to_datetime(mercadodf.date, format="%d/%m/%Y")
    mercadodf_grouped = mercadodf.groupby("description")

    months = mercadodf["date"].unique()

    items = []
    for name, group in mercadodf_grouped:
        date_diff = ((mercadodf["datetime"].max() -
                     group["datetime"].max()).days / 30.25)
        date_diff = date_diff if date_diff > 1 else 1
        sugerido = date_diff >= len(months) / group["price"].count().item()
        items.append({
            "item": name,
            "frequencia": group["price"].count().item(),
            "media": group["price"].mean().item(),
            "quantidade": len(months),
            'picked': True if sugerido else False,
            "lastBuy": group["datetime"].max(),
            "sugerido":  sugerido
        })

    return items
