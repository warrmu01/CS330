#!/usr/bin/env python3
"""Models"""

from config import db, ma


class Product(db.Model):
    """Product class"""

    __tablename__ = "product"
    an_id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, nullable=False)
    available = db.Column(db.String)
    species = db.Column(db.String)
    price = db.Column(db.String)
    image_url = db.Column(db.String)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"<Product(item={self.item!r})>"


class ProductSchema(ma.SQLAlchemySchema):
    """Product schema"""

    class Meta:
        """Product metadata"""

        model = Product
        load_instance = True

    an_id = ma.auto_field()
    item = ma.auto_field()
    available = ma.auto_field()
    species = ma.auto_field()
    price = ma.auto_field()
    image_url = ma.auto_field()
    quantity = ma.auto_field()
    