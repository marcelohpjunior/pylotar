from flask import Flask, jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from connect_db import connectDb
import psycopg2
from collections import OrderedDict

vendas_api = Blueprint('vendas_api', 'vendas_api', url_prefix="/api/vendas")

@vendas_api.route('/', methods=['GET', 'POST', 'PUT'])
def api_verbs():
    if request.method == 'GET':
        con = connectDb()
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute('select * from tb_vendas')
            result = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

        if(result == None):
            return 'Nenhum venda encontrado'

        return jsonify(result)

    elif request.method == 'POST':
        dados = request.json

        con = connectDb()
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute('''
                        insert into tb_vendas ( id_usuario, id_carro, nome_comprador, data_venda)
                        values (%s, %s, %s, %s);
                        ''',
                        (dados['id_usuario'],
                         dados['id_carro'],
                         dados['nome_comprador'],
                         dados['data_venda']))
            con.commit()
            cur.execute('''
                        select * from tb_vendas where id = (select max(id) from tb_vendas); 
                        ''')
            result = cur.fetchone()
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
            dados['id'] = str(dados['id'])
            result = get_vendas_by_id(dados['id'])

            if(result == None or type(result) == str):
                con.close()
                return 'ERRO PUT\nVenda com id ' + dados['id'] + ' não encontrado'
            
            cur.execute('''
                        update tb_vendas
                        set id_usuario = %s, id_carro = %s, nome_comprador = %s, data_venda = %s
                        where id = %s
                        ''',
                        (dados['id_usuario'],
                         dados['id_carro'],
                         dados['nome_comprador'],
                         dados['data_venda'],
                         dados['id']))
            con.commit()  
            result = get_vendas_by_id(dados['id'])          
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

        return result

@vendas_api.route('/<string:id>', methods=['GET'])
def get_vendas_by_id(id):
    con = connectDb()
    cur = con.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute('''select * from tb_vendas where id = %s''', (id,))
        result = cur.fetchone()
        cur.close()

        if(result == None):
            return 'ERRO GET\nVenda com id ' + id + ' não encontrado'

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return jsonify(result)

@vendas_api.route('/<string:id>', methods=['PUT'])
def put(id):
    dados = request.json

    con = connectDb()
    cur = con.cursor()

    try:
        result = get_vendas_by_id(id)

        if(result == None or type(result) == str):
            con.close()
            return 'ERRO PUT\nVenda com id ' + id + ' não encontrado'

        cur.execute('''
                        update tb_vendas
                        set id_usuario = %s, id_carro = %s, nome_comprador = %s, data_venda = %s
                        where id = %s
                        ''',
                        (dados['id_usuario'],
                         dados['id_carro'],
                         dados['nome_comprador'],
                         dados['data_venda'],                         
                         id))
        con.commit()
        result = get_vendas_by_id(id)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return result

@vendas_api.route('/<string:id>', methods=['DELETE'])
def delete(id):
    con = connectDb()
    cur = con.cursor()

    try:      

        result = get_vendas_by_id(id)

        if(result == None or type(result) == str):
            con.close()
            return 'ERRO DELETE\nVenda com id ' + id + ' não encontrado'
        
        cur.execute('''delete from tb_vendas where id = %s ''', (id,))
        con.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return "Venda " + id + " deletado com sucesso"
