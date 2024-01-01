from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
import secrets
app = Flask(__name__)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.token = self.set_token(24)

    def __repr__(self):
        return f"<User {self.email}>"

    def generate_password_hash(self, password):
        self.password = generate_password_hash(password)
    
    def set_token (self, length):
        self.token = secrets.token_hex(length)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_token = db.Column(db.String(50), db.ForeignKey('user.token'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, make, model, year, color, price, user_token):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.user_token = user_token

    def __repr__(self):
        return f"<Car {self.make} {self.model} {self.year} {self.color} {self.price} {self.user_token}>"

    

