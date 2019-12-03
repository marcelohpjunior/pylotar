from flask import Flask, jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from connect_db import connectDb
import psycopg2
from collections import OrderedDict

usuarios_api = Blueprint('usuarios_api', 'usuarios_api', url_prefix="/api/usuarios")

@usuarios_api.route('/', methods=['GET', 'POST', 'PUT'])
def api_verbs():
    if request.method == 'GET':
        con = connectDb()
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute('select * from tb_usuarios')
            result = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

        if(result == None):
            return 'Nenhum usuário encontrado'

        return jsonify(result)

    elif request.method == 'POST':
        dados = request.json

        con = connectDb()
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute('''
                        insert into tb_usuarios ( nome, sobrenome, telefone, cpf, email, senha)
                        values (%s, %s, %s, %s, %s, %s);
                        ''',
                        (dados['nome'],
                        dados['sobrenome'],
                        dados['telefone'],
                        dados['cpf'],
                        dados['email'],
                        dados['senha']))
            con.commit()
            cur.execute('''
                        select * from tb_usuarios where id = (select max(id) from tb_usuarios); 
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
            result = get_usuarios_by_id(dados['id'])

            if(result == None or type(result) == str):
                con.close()
                return 'ERRO PUT\nCarro com id ' + dados['id'] + ' não encontrado'
            
            cur.execute('''
                        update tb_usuarios
                        set nome = %s, sobrenome = %s, telefone = %s, cpf = %s, email = %s, senha = %s
                        where id = %s
                        ''',
                        (dados['nome'],
                         dados['sobrenome'],
                         dados['telefone'],
                         dados['cpf'],
                         dados['email'],
                         dados['senha'],
                         dados['id']))
            con.commit()  
            result = get_usuarios_by_id(dados['id'])          
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

        return result

@usuarios_api.route('/<string:id>', methods=['GET'])
def get_usuarios_by_id(id):
    con = connectDb()
    cur = con.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute('''select * from tb_usuarios where id = %s''', (id,))
        result = cur.fetchone()
        cur.close()

        if(result == None):
            return 'ERRO GET\nUsuario com id ' + id + ' não encontrado'

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return jsonify(result)

@usuarios_api.route('/<string:id>', methods=['PUT'])
def put(id):
    dados = request.json

    con = connectDb()
    cur = con.cursor()

    try:
        result = get_usuarios_by_id(id)

        if(result == None or type(result) == str):
            con.close()
            return 'ERRO PUT\nCarro com id ' + id + ' não encontrado'

        cur.execute('''
                        update tb_usuarios
                        set nome = %s, sobrenome = %s, telefone = %s, cpf = %s, email = %s, senha = %s
                        where id = %s
                        ''',
                        (dados['nome'],
                         dados['sobrenome'],
                         dados['telefone'],
                         dados['cpf'],
                         dados['email'],
                         dados['senha'],
                         id))
        con.commit()
        result = get_usuarios_by_id(id)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return result

@usuarios_api.route('/<string:id>', methods=['DELETE'])
def delete(id):
    con = connectDb()
    cur = con.cursor()

    try:      

        result = get_usuarios_by_id(id)

        if(result == None or type(result) == str):
            con.close()
            return 'ERRO DELETE\nUsuário com id ' + id + ' não encontrado'
        
        cur.execute('''delete from tb_usuarios where id = %s ''', (id,))
        con.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return "Usuário " + id + " deletado com sucesso"

#<string:email>&<string:senha>
@usuarios_api.route('/login', methods=['GET','POST'])
def login():
    con = connectDb()
    cur = con.cursor(cursor_factory=RealDictCursor)
    result = ''
    
    if request.method == 'GET':
        email = request.args.get('email')
        senha= request.args.get('senha')
    else:
        email = request.json['email']
        senha = request.json['senha']

    try:      
        cur.execute('''select * from tb_usuarios where email = %s and senha = %s ''', (email,senha,))
        result = cur.fetchall()
      

        if(result == None or type(result) == str):
            con.close()
            return 'ERRO LOGIN\nLogin invalido'
        

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

    return jsonify(result)