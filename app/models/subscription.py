from app.extensions import db
from datetime import datetime

class Account(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    subscription = db.Column(db.String(50), nullable=False , default="Free")
    generation_count = db.Column(db.Integer, nullable=False, default=0)
    payment = db.relationship('Payment', backref='account_payment')

    def __repr__(self) -> str:
        
        return f"<Account: '{self.subscription}'>"
    
class Payment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    transaction_id = db.Column(db.String(256), unique=True, nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    payed_by = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        
        return f"<Payment: '{self.transaction_id}'>"