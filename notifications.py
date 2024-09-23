from models import db, Product, Notification
from datetime import datetime, timedelta

def check_and_notify():
    today = datetime.utcnow().date()
    warning_date = today + timedelta(days=7)

    products = Product.query.filter(Product.expiry_date <= warning_date).all()
    
    for product in products:
        notification = Notification(
            product_id=product.product_id,
            notification_type="Expiry Warning"
        )
        db.session.add(notification)
        db.session.commit()

        # Gửi thông báo đến nhân viên qua email, SMS, hoặc ứng dụng.
        print(f"Product {product.product_name} is nearing expiry on {product.expiry_date}.")
