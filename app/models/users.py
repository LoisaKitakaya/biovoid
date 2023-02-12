from app.extensions import db
from sqlalchemy.sql import func

class User(db.Model):

    _tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    address = db.relationship('Address', backref='user_address')

    def __repr__(self):

        return f"<User '{self.username}'>"

class Address(db.Model):

    _tablename__ = "User Addresses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    city = db.Column(db.String(256), nullable=False)
    state_or_province = db.Column(db.String(256), nullable=False)
    physical_address = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self):

        return f"<Address '{self.city}, {self.state_or_province}, {self.physical_address}, {self.country}'>"
