import sqlite3
import json


def db():
    db = sqlite3.connect('poup.sqlite', check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db

# cursor = db().cursor()
# cursor.execute(
#     "CREATE TABLE IF NOT EXISTS objetivos (id integer PRIMARY KEY, descricao text NOT NULL)")


# database = db()
# cursor = database.cursor()
# cursor.execute(
#     "CREATE TABLE recurso_objetivo (id text PRIMARY KEY, id_recurso text, id_objetivo text, fixa boolean, value float, FOREIGN KEY (id_recurso) REFERENCES recursos(id), FOREIGN KEY (id_objetivo) REFERENCES objetivos(id))")
# database.commit()
# database.close()

# database = db()
# cursor = database.cursor()
# cursor.execute(
#     "DELETE FROM recursos WHERE nome = 'Sofá'")
# database.commit()
# database.close()

# database = db()
# cursor = database.cursor()
# cursor.execute(
#     "DELETE FROM objetivos WHERE descricao = 'Investimento'")
# database.commit()
# database.close()

# database = db()
# cursor = database.cursor()
# cursor.execute(
#     "ALTER TABLE recurso_objetivo ALTER COLUMN fixa BOOLEAN")
# database.commit()
# database.close()

# database = db()
# cursor = database.cursor()
# rows = cursor.execute(
#     "SELECT value, nome, descricao, fixa FROM recurso_objetivo INNER JOIN recursos ON recursos.id = recurso_objetivo.id_recurso INNER JOIN objetivos ON objetivos.id = recurso_objetivo.id_objetivo").fetchall()
# database.commit()
# database.close()

# print(json.loads(json.dumps([dict(ix) for ix in rows])))
