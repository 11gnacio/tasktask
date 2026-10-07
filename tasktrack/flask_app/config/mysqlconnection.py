import os
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Ocurrió un problema en la consulta MySQL:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db=None):
    if db is None:
        db = os.environ.get("DB_NAME", "esquema_tasktrack")
    return MySQLConnection(db)
