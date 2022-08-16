from logging.handlers import DatagramHandler
from numpy import int64
import json
import pandas as pd
from datetime import datetime, date
df = pd.DataFrame(pd.read_csv("/home/panzee/Dev/fin-project-api/teste.csv", delimiter=';'))
objetivosdf = pd.DataFrame(pd.read_csv(
    "/home/panzee/Dev/fin-project-api/objetivos.csv", delimiter=';'))
contasdf = pd.DataFrame(pd.read_csv(
    "/home/panzee/Dev/fin-project-api/contas.csv", delimiter=';'))

df['datetime'] = pd.to_datetime(
    df.Data, format="%d/%m/%Y")
df['timestamp'] = df.datetime.astype('int64') // 10**9
df["month_year"] = df.timestamp.map(
    lambda x: datetime(datetime.fromtimestamp(x).year,
                       datetime.fromtimestamp(x).month, 1))
# df["month_year"] = df.timestamp.map(
#     lambda x: str(datetime.fromtimestamp(x).month) + str(datetime.fromtimestamp(x).year))
# df['Silvana'] = df.Conta.str.contains('Silvana')
# df['Alexis'] = df.Conta.str.contains('Alexis')
recursos = ['Silvana', 'Alexis']
df['recurso'] = df.Conta.map(
    lambda x: x.split(" ")[len(x.split(" ")) - 1] if any(ext in x for ext in recursos) else None)

MONTH_IN_SECONDS = 2635200
YEAR_IN_SECONDS = 31104000


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
    print(receitasSilvana)
    return receitasSilvana['Valor'].sum()


def receitasByMonth(timestamp):
    isCurrentMonth = True

    if df.empty:
        return []

    desired_month_year = datetime.fromtimestamp(timestamp)
    print(desired_month_year)

    
    # previous_desired_month_year = datetime.fromtimestamp(
    #     timestamp - MONTH_IN_SECONDS)
    previous_desired_month_year = datetime(datetime.now().year, datetime.now().month - 1, 1)
    print(previous_desired_month_year)
    most_recent = datetime.fromtimestamp(df.timestamp.max())
    previous_most_recent = datetime(most_recent.year, most_recent.month - 1, 1)
    print(f"most {previous_most_recent}")

    df['is_desired_month_year'] = df['datetime'].map(
        lambda x: x.month + x.year) == desired_month_year.month + desired_month_year.year

    df['is_previous_desired_month_year'] = df['datetime'].map(
        lambda x: x.month + x.year) == previous_desired_month_year.month + previous_desired_month_year.year

    df['most_recent'] = df['datetime'].map(
        lambda x: x.month + x.year) == most_recent.month + most_recent.year

    df['previous_most_recent'] = df['datetime'].map(
        lambda x: x.month + x.year) == previous_most_recent.month + previous_most_recent.year

    print(df)

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
    pts = timestamp - MONTH_IN_SECONDS if isCurrentMonth else df.timestamp.max().item() - \
        MONTH_IN_SECONDS

    desired = json.loads(grouped['Valor'].sum().to_json())
    previous = json.loads(groupedpmr['Valor'].sum().to_json())

    lista = list(map(lambda x: {
        'name': x,
        'previous': {'value': previous[x], 'timestamp': pts*1000},
        'timestamp': ts*1000,
        'value': desired[x]
    }, recursos))

    return {'isDesired': isCurrentMonth, 'recursos': lista}


def getCusto():

    only_debits = df.query('Valor < 0')
    print(only_debits)
    cost = only_debits["Valor"].sum() / len(df['month_year'].unique()) * -1
    return {'custo': cost}


def recursoAvancado(recurso):
    ha_um_ano = datetime(datetime.now().year - 1,
                         datetime.now().month, 1).timestamp()
    ultimos_doze_meses = df.query(f"timestamp > {ha_um_ano}")

    receitas_total = ultimos_doze_meses.query("Valor > 0")['Valor'].sum()
    print(receitas_total)

    dfrecurso = ultimos_doze_meses.query(f'recurso == "{recurso}"')
    dfrecurso = dfrecurso.sort_values(by='timestamp')

    meses_referencia_count = len(dfrecurso['month_year'].unique())
    print(dfrecurso)

    dfdespesas = dfrecurso.query('Valor < 0')

    dfreceitas = dfrecurso.query('Valor > 0')

    totalpassivo = dfreceitas.query(
        'Subcategoria == "Rendimentos" | Subcategoria == "Proventos" | Subcategoria == "JCP"')

    receitas_agrupadas = dfreceitas.groupby('month_year')
    print(receitas_agrupadas.Valor.sum())
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
        print(f"previous: {previous}, current: {current}")
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

    objetivos_agrupados = objetivosdf.groupby('Descricao')
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
    ha_um_ano = datetime(datetime.now().year - 1,
                         datetime.now().month, 1).timestamp()

    ano_atras = df.query(f"timestamp > {ha_um_ano}")
    meses_referencia_count = len(ano_atras['month_year'].unique())

    despesas = ano_atras.query('Valor < 0')['Valor'].sum()
    receitas = ano_atras.query('Valor > 0')['Valor'].sum()
    print(receitas)

    reserva = contasdf.query('Conta == "Guardado Silvana"')['Valor'].sum()
    reserva2 = contasdf.query('Conta == "Guardado Alexis"')['Valor'].sum()

    return {
        'despesas': despesas / meses_referencia_count * -1,
        'receitas': receitas / meses_referencia_count,
        'reserva': reserva + reserva2
    }
