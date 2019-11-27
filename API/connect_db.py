import psycopg2.extras
import psycopg2 as pg

def connectToDb():
    try:
        return pg.connect(
            database='pylotar',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
    except Exception as erro:
        print(erro)