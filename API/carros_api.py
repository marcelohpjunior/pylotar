from flask import Flask, jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from connect_db import connectToDb
import psycopg2

carros_api = Blueprint('carros_api', 'carros_api', url_prefix="/api/carros")

@carros_api.route('/', methods=['GET', 'POST', 'PUT'])
def api_verbs():
    if request.method == 'GET':
        conn = connectToDb()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute('select * from tb_carros')
            result = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


        return jsonify(result)

    elif request.method == 'POST':
        dados = request.json

        conn = connectToDb()
        cur = conn.cursor()

        try:
            cur.execute('''
                        insert into tb_carros ( marca, modelo, ano, cor, valor)
                        values (%s, %s, %s, %s, %s);
                        ''',
                        (dados['marca'],
                        dados['modelo'],
                        dados['ano'],
                        dados['cor'],
                        dados['valor']))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return "Carro inserido com sucesso"

    else:
        dados = request.json

        conn = connectToDb()
        cur = conn.cursor()

        try:
            cur.execute('''
                        update tb_carros
                        set marca = %s, modelo = %s, ano = %s, cor = %s, valor = %s
                        where id = %s
                        ''',
                        (dados['marca'],
                         dados['modelo'],
                         dados['ano'],
                         dados['cor'],
                         dados['valor'],
                         dados['id']))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return("Carro atualizado com sucesso")


@carros_api.route('/<string:id>', methods=['GET'])
def get_carros_by_id(id):
    conn = connectToDb()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    print(id)

    try:
        cur.execute('''select * from tb_carros where id = %s''', (id))
        result = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return jsonify(result)

@carros_api.route('/<string:id>', methods=['DELETE'])
def delete(id):
    conn = connectToDb()
    cur = conn.cursor()

    try:
        cur.execute('''delete from tb_carros where id = %s ''', (id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return "Carro deletado com sucesso"

