from database import db
import json


def insertObjetivo(objetivo):
    dbase = db()
    cursor = dbase.cursor()
    try:
        cursor.execute(
            f"INSERT INTO objetivos VALUES (?, ?)", (objetivo.id, objetivo.descricao))
        dbase.commit()
        dbase.close()

    except cursor as err:
        print(err)


def selectObjetivos():
    dbase = db()
    cursor = dbase.cursor()
    try:
        rows = cursor.execute(
            "SELECT * FROM objetivos").fetchall()
        dbase.commit()
        dbase.close()
        return json.loads(json.dumps([dict(ix) for ix in rows]))
    except cursor as err:
        print(err)
