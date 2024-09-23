from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Product, ActivityLog
from datetime import datetime

products_bp = Blueprint('products', __name__)

# Thêm sản phẩm mới (yêu cầu đăng nhập)
@products_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    current_employee_id = get_jwt_identity()
    data = request.json
    new_product = Product(
        product_name=data['product_name'],
        barcode=data.get('barcode'),
        quantity=data['quantity'],
        expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d')
    )
    db.session.add(new_product)
    db.session.commit()

    # Ghi nhật ký
    log = ActivityLog(
        employee_id=current_employee_id,
        product_id=new_product.product_id,
        action="Add Product"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Product added", "product": data}), 201

# Sửa sản phẩm
@products_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    current_employee_id = get_jwt_identity()
    product = Product.query.get_or_404(product_id)
    data = request.json

    product.product_name = data['product_name']
    product.barcode = data.get('barcode')
    product.quantity = data['quantity']
    product.expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d')
    db.session.commit()

    # Ghi nhật ký
    log = ActivityLog(
        employee_id=current_employee_id,
        product_id=product_id,
        action="Update Product"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Product updated"}), 200

# Xóa sản phẩm
@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    current_employee_id = get_jwt_identity()
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    # Ghi nhật ký
    log = ActivityLog(
        employee_id=current_employee_id,
        product_id=product_id,
        action="Delete Product"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Product deleted"}), 200

# Lấy danh sách sản phẩm cận date hoặc hết date
@products_bp.route('/products/expired', methods=['GET'])
@jwt_required()
def get_expiring_products():
    today = datetime.utcnow().date()
    expiring_products = Product.query.filter(Product.expiry_date <= today).all()

    products = []
    for product in expiring_products:
        products.append({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "expiry_date": product.expiry_date.strftime('%Y-%m-%d')
        })

    return jsonify({"expiring_products": products}), 200
