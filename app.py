from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reading_list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)


if __name__ == '__main__':
    app.run(debug=True)

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    books = db.relationship('Book', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    published_date = db.Column(db.Date)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, author, published_date, user_id):
        self.title = title
        self.author = author
        self.published_date = published_date
        self.user_id = user_id

from models import db

db.create_all()

from books.books import books_bp

app.register_blueprint(books_bp, url_prefix='/books')