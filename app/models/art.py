from app.extensions import db
from datetime import datetime

class Image(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    image_name = db.Column(db.String(100), unique=True, nullable=False)
    image_url = db.Column(db.String(300), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self) -> str:
        
        return f"<Image: '{self.image_name}'>"