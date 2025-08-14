"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Product
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

# -------------------------------------------------------------
#                       PRODUCTOS (CRUD)
# -------------------------------------------------------------

@api.route('/products', methods=['GET'])
def list_products():
    """Devuelve un ARRAY directo (tu front hace setProducts(data)).
    Soporta ?limit, ?aroma y ?q (búsqueda por nombre).
    """
    limit = request.args.get('limit', type=int)
    aroma = request.args.get('aroma', type=str)
    q = request.args.get('q', type=str)

    query = Product.query
    if aroma:
        query = query.filter(Product.aroma == aroma)
    if q:
        like = f"%{q}%"
        query = query.filter(Product.name.ilike(like))

    query = query.order_by(Product.id.desc())
    if limit:
        query = query.limit(limit)

    items = [p.serialize() for p in query.all()]
    return jsonify(items), 200

@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(p.serialize()), 200

@api.route('/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}

    # Validaciones mínimas: basadas en tu modelo
    required_fields = ['name', 'description', 'price', 'image_url']
    missing = [f for f in required_fields if data.get(f) in (None, '')]
    if missing:
        return jsonify({"error": f"Falta(n) campo(s): {', '.join(missing)}"}), 400

    try:
        p = Product(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            image_url=data['image_url'],
            aroma=data.get('aroma'),
            ritual=data.get('ritual')
        )
        db.session.add(p)
        db.session.commit()
        return jsonify(p.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@api.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.get_json() or {}
    for field in ['name', 'description', 'price', 'image_url', 'aroma', 'ritual']:
        if field in data and data[field] is not None:
            if field == 'price':
                try:
                    setattr(p, field, float(data[field]))
                except ValueError:
                    return jsonify({"error": "'price' debe ser numérico"}), 400
            else:
                setattr(p, field, data[field])

    db.session.commit()
    return jsonify(p.serialize()), 200

@api.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Producto no encontrado"}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"ok": True}), 200