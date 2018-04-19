from app import db,lm,whooshe
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64),unique = True)
    email = db.Column(db.String(255),unique = True)
    password_hash = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    avartar = db.Column(db.String(255))
    #birth_day = db.Column(db.Date)
    role = db.Column(db.String(30))

    orders = db.relationship('Order',backref='users',lazy = 'dynamic')

    def set_password(self,secret):
        self.password_hash = generate_password_hash(secret)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __init__(self,username,email,password_hash):
        self.username=username
        self.email=email
        self.password_hash = generate_password_hash(password_hash)
        self.address = ''
        self.avartar=''
        self.phone_number=''

    def update(self,adress):
        self.address = adress

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250),unique = True)

    products = db.relationship('Product',backref='category',lazy = 'dynamic')
    def __init__(self,name):
        self.name=name

@whooshe.register_model('name')
class Product(db.Model):
    __tablename__= 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    orderdetails = db.relationship('OrderDetail', backref='products', lazy='dynamic')


    def __init__(self,name,price,category_id,image,description):
        self.name=name
        self.price=price
        self.category_id=category_id
        self.image=image
        self.description=description


class Order(db.Model):
    __tablename__   = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    user_adress = db.Column(db.String(250))
    message = db.Column(db.String(500))
    created = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    total_cost = db.Column(db.Float(5))

    orderdetail = db.relationship('OrderDetail',backref='order',lazy = 'dynamic')

    def __init__(self,user_id,user_adress,message,created,total_cost):
        self.user_id = user_id
        self.user_adress = user_adress
        self.message = message
        self.created = created
        self.status = False
        self.total_cost = total_cost

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer,db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer())
    


