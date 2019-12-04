from flask import Flask, jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from connect_db import connectDb
import psycopg2
import requests 
import json
import os
import zipfile as zip

exportar_api = Blueprint('exportar_api', 'exportar_api', url_prefix="/api/exportar")

@exportar_api.route('/', methods=['GET'])
def api_exportar():

    url_carros = 'http://127.0.0.1:8080/api/carros/'
    url_usuarios = 'http://127.0.0.1:8080/api/usuarios/'
    url_vendas = 'http://127.0.0.1:8080/api/vendas/'

    carros = requests.get(url_carros).json()
    usuarios =  requests.get(url_usuarios).json()
    vendas = requests.get(url_vendas).json()

    exportarJson('carros', carros)
    exportarJson('usuarios', usuarios)
    exportarJson('vendas', vendas)

    ziparArquivos()
    
    return 'Arquivos exportados com sucesso'

def exportarJson(fileNome, dados):
    if(not os.path.exists('c:\\dados_json')):
        os.makedirs('c:\\dados_json')

    file = open('c:\\dados_json/'+fileNome + ".json", "w")
    json.dump(dados, file, indent=4)
    file.close()

def ziparArquivos():
    if(not os.path.exists('c:\\dados_exportados')):
        os.makedirs('c:\\dados_exportados')

    path_zip = os.path.join(os.sep, 'c:\\', "dados_exportados/dados.zip")
    path_dir = os.path.join(os.sep, 'c:\\', "dados_json")

    zf = zip.ZipFile(path_zip,"w")
    for dirname, subdirs, files in os.walk(path_dir):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()