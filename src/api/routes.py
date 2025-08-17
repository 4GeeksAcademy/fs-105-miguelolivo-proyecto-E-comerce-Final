"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from api.utils import generate_sitemap, APIException
from api.models import db, User, Product, CartItem, Order, OrderItem

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200



# HELPERS


def _abs_image(url: str) -> str:
    """
    Convierte rutas relativas (p.ej. /static/...) en URL absoluta del backend.
    Prioriza PUBLIC_BACKEND_URL si existe para evitar localhost en entornos remotos.
    """
    if not url:
        return url
    if url.startswith('http://') or url.startswith('https://'):
        return url

    
    public_base = os.getenv("PUBLIC_BACKEND_URL")
    if public_base:
        base = public_base.rstrip('/')
    else:
        
        xf_proto = request.headers.get('X-Forwarded-Proto')
        xf_host  = request.headers.get('X-Forwarded-Host')
        if xf_proto and xf_host:
            base = f"{xf_proto}://{xf_host}"
        else:
            
            base = request.host_url.rstrip('/')

    prefix = '' if url.startswith('/') else '/'
    return f"{base}{prefix}{url}"



# PRODUCTOS (CRUD)


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

    items = []
    for p in query.all():
        d = p.serialize()
        d['image_url'] = _abs_image(d.get('image_url'))  # <-- asegura URL absoluta
        items.append(d)
    return jsonify(items), 200


@api.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Producto no encontrado"}), 404
    d = p.serialize()
    d['image_url'] = _abs_image(d.get('image_url'))  # <-- asegura URL absoluta
    return jsonify(d), 200


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
        d = p.serialize()
        d['image_url'] = _abs_image(d.get('image_url'))
        return jsonify(d), 201
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
    d = p.serialize()
    d['image_url'] = _abs_image(d.get('image_url'))
    return jsonify(d), 200


@api.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    p = Product.query.get(product_id)
    if not p:
        return jsonify({"error": "Producto no encontrado"}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"ok": True}), 200


# -------------------------------------------------------------
#                           AUTH
# -------------------------------------------------------------

@api.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not email or not password:
        return jsonify({"error": "email y password son obligatorios"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email ya registrado"}), 409
    user = User(email=email, password=generate_password_hash(password), is_active=True)
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token, "user": user.serialize()}), 201


@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "credenciales inválidas"}), 401
    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token, "user": user.serialize()}), 200


# -------------------------------------------------------------
#                           PERFIL
# -------------------------------------------------------------

@api.route('/me', methods=['GET'])
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.serialize()), 200


@api.route('/me', methods=['PUT'])
@jwt_required()
def me_update():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json() or {}
    if 'email' in data and data['email']:
        email = data['email'].strip().lower()
        # otro usuario con el mismo email
        if User.query.filter(User.email == email, User.id != uid).first():
            return jsonify({"error": "email ya en uso"}), 409
        user.email = email
    if 'password' in data and data['password']:
        user.password = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify(user.serialize()), 200


@api.route('/me', methods=['DELETE'])
@jwt_required()
def me_delete():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"ok": True}), 200


# -------------------------------------------------------------
#                           CARRITO
# -------------------------------------------------------------

@api.route('/cart', methods=['GET'])
@jwt_required()
def cart_list():
    uid = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=uid).all()
    return jsonify([i.serialize() for i in items]), 200


@api.route('/cart', methods=['POST'])
@jwt_required()
def cart_add():
    uid = get_jwt_identity()
    data = request.get_json() or {}
    pid = data.get('product_id')
    qty = int(data.get('quantity') or 1)
    if not pid or qty < 1:
        return jsonify({"error": "product_id y quantity>=1 son obligatorios"}), 400

    prod = Product.query.get(pid)
    if not prod:
        return jsonify({"error": "producto no existe"}), 404

    item = CartItem.query.filter_by(user_id=uid, product_id=pid).first()
    if item:
        item.quantity += qty
    else:
        item = CartItem(user_id=uid, product_id=pid, quantity=qty)
        db.session.add(item)
    db.session.commit()

    return jsonify(item.serialize() if item else None), 201


@api.route('/cart/item/<int:item_id>', methods=['PUT'])
@jwt_required()
def cart_update(item_id):
    uid = get_jwt_identity()
    item = CartItem.query.get(item_id)
    if not item or item.user_id != uid:
        return jsonify({"error": "ítem no encontrado"}), 404

    data = request.get_json() or {}
    qty = int(data.get('quantity') or 1)
    if qty < 1:
        return jsonify({"error": "quantity debe ser >=1"}), 400

    item.quantity = qty
    db.session.commit()
    return jsonify(item.serialize()), 200


@api.route('/cart/item/<int:item_id>', methods=['DELETE'])
@jwt_required()
def cart_delete(item_id):
    uid = get_jwt_identity()
    item = CartItem.query.get(item_id)
    if not item or item.user_id != uid:
        return jsonify({"error": "ítem no encontrado"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"ok": True}), 200


@api.route('/cart', methods=['DELETE'])
@jwt_required()
def cart_clear():
    uid = get_jwt_identity()
    CartItem.query.filter_by(user_id=uid).delete()
    db.session.commit()
    return jsonify({"ok": True}), 200


# -------------------------------------------------------------
#                           PEDIDOS
# -------------------------------------------------------------

def _calc_cart_total(items):
    return float(sum(i.quantity * (i.product.price or 0) for i in items))

@api.route('/orders/checkout', methods=['POST'])
@jwt_required()
def checkout():
    uid = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=uid).all()
    if not items:
        return jsonify({"error": "carrito vacío"}), 400

    order = Order(user_id=uid, status="pending", total=_calc_cart_total(items))
    db.session.add(order)
    db.session.flush()  # para tener order.id antes de commit

    for it in items:
        oi = OrderItem(
            order_id=order.id,
            product_id=it.product_id,
            quantity=it.quantity,
            unit_price=it.product.price or 0
        )
        db.session.add(oi)

    # Vaciar carrito del usuario
    CartItem.query.filter_by(user_id=uid).delete()

    # Simulación: marcar como pagado si viene ?simulate_paid=1
    if request.args.get("simulate_paid") == "1":
        order.status = "paid"

    db.session.commit()
    return jsonify(order.serialize()), 201


@api.route('/orders', methods=['GET'])
@jwt_required()
def orders_list():
    uid = get_jwt_identity()
    orders = Order.query.filter_by(user_id=uid).order_by(Order.created_at.desc()).all()
    return jsonify([o.serialize() for o in orders]), 200


@api.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def orders_detail(order_id):
    uid = get_jwt_identity()
    order = Order.query.get(order_id)
    if not order or order.user_id != uid:
        return jsonify({"error": "pedido no encontrado"}), 404
    return jsonify(order.serialize()), 200
