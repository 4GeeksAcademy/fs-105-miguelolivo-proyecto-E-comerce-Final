"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Product  # Importa Product también
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

# ENDPOINT PARA PRODUCTOS 

@api.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

@api.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    required_fields = ['name', 'description', 'price', 'image_url']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo obligatorio: {field}"}), 400

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image_url=data['image_url'],
        aroma=data.get('aroma'),
        ritual=data.get('ritual')
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify(new_product.serialize()), 201
