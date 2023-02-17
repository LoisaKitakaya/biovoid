from app.extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default="standarduser")
    image = db.relationship('Image', backref='user_image')

    def __repr__(self):

        return f"<User: '{self.username}'>"
