from app.extensions import db
from sqlalchemy.sql import func

class OrderItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    order = db.relationship('Order', backref='order_items')

    def __repr__(self) -> str:
        
        return f"<OrderItem {self.public_id}>"

class PaymentDetails(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    order = db.relationship('Order', backref='payment_details')

    def __repr__(self) -> str:
        
        return f"<PaymentDetails {self.public_id}>"

class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    order_item_id = db.Column(db.Integer, db.ForeignKey("order_item.id"))
    payment_details_id = db.Column(db.Integer, db.ForeignKey("payment_details.id"))
    status = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self) -> str:
        
        return f"<Order {self.public_id}>"