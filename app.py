from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from routes.products import products_bp
from routes.employees import employees_bp

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# Cấu hình JWT
jwt = JWTManager(app)

# Đăng ký các blueprint (routes)
app.register_blueprint(products_bp)
app.register_blueprint(employees_bp)

if __name__ == '__main__':
    app.run(debug=True)
