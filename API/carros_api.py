from flask import Flask, jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from connect_db import connectDb
import psycopg2
from collections import OrderedDict

carros_api = Blueprint('carros_api', 'carros_api', url_prefix="/api/carros")

@carros_api.route('/', methods=['GET', 'POST', 'PUT'])
def api_verbs():
    if request.method == 'GET':
        con = connectDb()
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute('select * from tb_carros')
            result = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

        if(result == None):
            return 'Nenhum carro encontrado'

        return jsonify(result)

    elif request.method == 'POST':
        dados = request.json

        con = connectDb()
        cur = con.cursor(cursor_factory=RealDictCursor)

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
            con.commit()
            cur.execute('''
                        select * from tb_carros where id = (select max(id) from tb_carros); 
                        ''')
            result = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()
    
        return jsonify(result)

    else:
        dados = request.json

        con = connectDb()
        cur = con.cursor()

        try:
            result = get_carros_by_id(dados['id'])

            if(result == None):
                con.close()
                return 'ERRO PUT\nCarro com id ' + dados['id'] + ' não encontrado'
            
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
            con.commit()  
            result = get_carros_by_id(dados['id'])          
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

        return result

@carros_api.route('/<string:id>', methods=['GET'])
def get_carros_by_id(id):
    con = connectDb()
    cur = con.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute('''select * from tb_carros where id = %s''', (id,))
        result = cur.fetchall()
        cur.close()

        if(result == None):
            return 'ERRO GET\nCarro com id ' + id + ' não encontrado'

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return jsonify(result)

@carros_api.route('/<string:marca>', methods=['GET'])
def get_carros_by_marca(marca):
    con = connectDb()
    cur = con.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute('''select * from tb_carros where marca = %s''', (marca,))
        result = cur.fetchall()
        cur.close()

        if(result == None):
            return 'ERRO GET\nCarro da marca ' + id + ' não encontrado'

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return jsonify(result)   

@carros_api.route('/<string:ano>', methods=['GET'])
def get_carros_by_ano(ano):
    con = connectDb()
    cur = con.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute('''select * from tb_carros where ano = %s''', (ano,))
        result = cur.fetchall()
        cur.close()

        if(result == None):
            return 'ERRO GET\nCarro com o ano ' + ano + ' não encontrado'

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return jsonify(result)

@carros_api.route('/<string:id>', methods=['PUT'])
def put(id):
    dados = request.json

    con = connectDb()
    cur = con.cursor()

    try:
        result = get_carros_by_id(id)

        if(result == None):
            con.close()
            return 'ERRO PUT\nCarro com id ' + id + ' não encontrado'

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
                    id))
        con.commit()
        result = get_carros_by_id(id)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return result

@carros_api.route('/<string:id>', methods=['DELETE'])
def delete(id):
    con = connectDb()
    cur = con.cursor()

    try:        
        result = get_carros_by_id(id)

        if(result == None):
            con.close()
            return 'ERRO DELETE\nCarro com id ' + id + ' não encontrado'
        
        cur.execute('''delete from tb_carros where id = %s ''', (id,))
        con.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return "Carro " + id + " deletado com sucesso"
