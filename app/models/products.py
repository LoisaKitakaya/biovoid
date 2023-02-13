from app.extensions import db
from sqlalchemy.sql import func

class ProductCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    category_description = db.Column(db.String(1000), nullable=False)
    product = db.relationship('Product', backref='product_category')

    def __repr__(self) -> str:
        
        return f'<ProductCategory {self.category_name}>'

class ProductDiscount(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    discount_name = db.Column(db.String(100), unique=True, nullable=False)
    discount_description = db.Column(db.String(1000), nullable=False)
    discount_percentage = db.Column(db.Integer, nullable=False)
    discount_active = db.Column(db.Boolean, nullable=False)
    product = db.relationship('Product', backref='product_discount')

    def __repr__(self) -> str:
        
        return f'<ProductDiscount {self.discount_name}>'

class ProductInventory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now())
    product = db.relationship('Product', backref='product_inventory')

    def __repr__(self) -> str:
        
        return f'<ProductInventory {self.product_quantity}>'

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256), unique=True, nullable=False)
    product_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    product_discount_id = db.Column(db.Integer, db.ForeignKey('product_discount.id'))
    product_inventory_id = db.Column(db.Integer, db.ForeignKey('product_inventory.id'))
    product_name = db.Column(db.String(100), nullable=False)
    product_image_url = db.Column(db.String(256), nullable=False)
    product_dimensions = db.Column(db.String(256), nullable=False)
    product_brand = db.Column(db.String(100), nullable=False)
    product_weight = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.String(1000), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=False, default=func.now())

    def __repr__(self) -> str:
        
        return f'<Product {self.product_name}>'