from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from ext import db, login_manager



class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

class Product(db.Model, BaseModel):
    __tablename__ = "products"


    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    img = db.Column(db.String(), nullable=False, default="default_photo.jpg")




class CartItem(db.Model, BaseModel):
    __tablename__ = "cartitem"
    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='cart_items')
    img = db.Column(db.String(), nullable=False, default="default_photo.jpg")
    quantity = db.Column(db.Integer, default=1)


class ContactMessage(db.Model, BaseModel):
    __tablename__ = "contact_message"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    problem = db.Column(db.Text, nullable=False)





class User(db.Model, BaseModel, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String())

    def __init__(self, username, password, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role



    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)





class Club(db.Model, BaseModel):
    __tablename__ = "clubs"


    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    address = db.Column(db.Integer(), nullable=False)
    img = db.Column(db.String(), nullable=False, default="default_photo.jpg")