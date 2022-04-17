
from app import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text, nullable=False)
    """
    Suppose that other information will be stored somewhere else.
    """


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class DiscountCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, nullable=False)
    issued_to_user = db.Column(db.Boolean, default=False)
    used = db.Column(db.Boolean, default=False)
    brand_id = db.Column(db.ForeignKey(Brand.id, ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.ForeignKey(Customer.id, ondelete="CASCADE"), nullable=True)
