"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger  # (opcional, si usas swagger)
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands

# --- Cargar variables de entorno ---
load_dotenv()

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"

# Rutas a directorios estáticos
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DIST_DIR = os.path.join(BASE_DIR, '../dist/')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__)
app.url_map.strict_slashes = False

# --- JWT config (para /auth, /me, /cart, /orders) ---
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
jwt = JWTManager(app)

# --- Config DB ---
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'mydb.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Inicializar DB y migraciones ---
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

# --- Admin y comandos (seed, etc.) ---
setup_admin(app)
setup_commands(app)

# --- Blueprint API ---
app.register_blueprint(api, url_prefix='/api')

# --- Error handler ---
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# --- Sitemap / raíz ---
@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(DIST_DIR, 'index.html')

# --- Servir SIEMPRE archivos de src/static ---
@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Sirve ficheros estáticos desde src/static, por ejemplo:
    /static/images/jabon_lavanda.png
    """
    response = send_from_directory(STATIC_DIR, filename)
    response.cache_control.max_age = 0  # no cache en dev
    return response

# --- Catch-all para frontend (dist) ---
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    """
    Sirve el frontend compilado (dist). No interfiere con /static/ gracias a la ruta anterior.
    """
    full_path = os.path.join(DIST_DIR, path)
    if not os.path.isfile(full_path):
        path = 'index.html'
    response = send_from_directory(DIST_DIR, path)
    response.cache_control.max_age = 0
    return response

# --- Run ---
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
