from database import db
import json


def insertRecursoObjetivo(recurso_objetivo):
    dbase = db()
    cursor = dbase.cursor()
    try:
        cursor.execute(
            f"INSERT INTO recurso_objetivo VALUES (?, ?, ?, ?, ?)", (recurso_objetivo.id, recurso_objetivo.id_recurso, recurso_objetivo.id_objetivo, recurso_objetivo.fixa, recurso_objetivo.value))
        dbase.commit()
        dbase.close()

    except cursor as err:
        print(err)


def insertRecursosObjetivos(recurso_objetivo):
    for i in recurso_objetivo:
        dbase = db()
        cursor = dbase.cursor()
        try:
            cursor.execute(
                f"INSERT INTO recurso_objetivo VALUES (?, ?, ?, ?, ?)", (i.id, i.id_recurso, i.id_objetivo, i.fixa, i.value))
            dbase.commit()
            dbase.close()

        except cursor as err:
            print(err)


def updateRecursoObjetivo(recurso_objetivo):
    dbase = db()
    cursor = dbase.cursor()
    try:
        cursor.execute(
            f"UPDATE recurso_objetivo SET fixa = ?, value = ? where id = ?", (recurso_objetivo.fixa, recurso_objetivo.value, recurso_objetivo.id))
        dbase.commit()
        dbase.close()

    except cursor as err:
        print(err)


def updateRecursosObjetivos(recurso_objetivo):
    for i in recurso_objetivo:
        dbase = db()
        cursor = dbase.cursor()
        try:
            cursor.execute(
                f"UPDATE recurso_objetivo SET fixa = ?, value = ? where id = ?", (i.fixa, i.value, i.id))
            dbase.commit()
            dbase.close()

        except cursor as err:
            print(err)


def selectRecursoObjetivos():
    dbase = db()
    cursor = dbase.cursor()
    try:
        rows = cursor.execute(
            "SELECT a.id, id_recurso, id_objetivo, value, nome, descricao, fixa FROM recurso_objetivo a INNER JOIN recursos ON recursos.id = a.id_recurso INNER JOIN objetivos ON objetivos.id = a.id_objetivo").fetchall()
        dbase.commit()
        dbase.close()
        return json.loads(json.dumps([dict(ix) for ix in rows]))
    except cursor as err:
        print(err)
