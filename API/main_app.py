from flask import Flask, jsonify, request
from flask_cors import CORS
#Blueprints
from carros_api import carros_api
from usuarios_api import usuarios_api
from vendas_api import vendas_api
from exportar_api import exportar_api

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.register_blueprint(carros_api)
    app.register_blueprint(usuarios_api)
    app.register_blueprint(vendas_api)
    app.register_blueprint(exportar_api)
    app.run(debug=True, port=8080)