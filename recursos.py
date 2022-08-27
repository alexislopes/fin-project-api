from database import db
import json


def insertRecurso(recurso):
    dbase = db()
    cursor = dbase.cursor()
    try:
        cursor.execute(
            f"INSERT INTO recursos VALUES (?, ?)", (recurso.nome, recurso.agregador))
        dbase.commit()
        dbase.close()

    except cursor as err:
        print(err)


def selectRecursos():
    dbase = db()
    cursor = dbase.cursor()
    try:
        rows = cursor.execute(
            "SELECT * FROM recursos").fetchall()
        dbase.commit()
        dbase.close()
        return json.loads(json.dumps([dict(ix) for ix in rows]))
    except cursor as err:
        print(err)
