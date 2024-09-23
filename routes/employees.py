from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, Employee

employees_bp = Blueprint('employees', __name__)

# Đăng ký tài khoản mới
@employees_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('phone_number') or not data.get('password'):
        return jsonify({"message": "Phone number and password are required"}), 400

    existing_employee = Employee.query.filter_by(phone_number=data['phone_number']).first()
    if existing_employee:
        return jsonify({"message": "Phone number already exists"}), 400

    # Tạo tài khoản mới
    new_employee = Employee(
        employee_name=data['employee_name'],
        phone_number=data['phone_number']
    )
    new_employee.set_password(data['password'])
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({"message": "Employee registered successfully"}), 201

# Đăng nhập tài khoản
@employees_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data.get('phone_number') or not data.get('password'):
        return jsonify({"message": "Phone number and password are required"}), 400

    employee = Employee.query.filter_by(phone_number=data['phone_number']).first()
    if not employee or not employee.check_password(data['password']):
        return jsonify({"message": "Invalid phone number or password"}), 401

    access_token = create_access_token(identity=employee.employee_id)
    return jsonify(access_token=access_token), 200
