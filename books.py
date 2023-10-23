from flask import Blueprint, request, jsonify
from models import db, User, Book
from flask_jwt_extended import jwt_required, get_jwt_identity

books_bp = Blueprint('books', __name__)

def create_book():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], published_date=data['published_date'], user_id=user.id)
    
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book created successfully'}), 201

def list_books():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    books = Book.query.filter_by(user_id=user.id).all()
    book_list = [{'title': book.title, 'author': book.author, 'published_date': str(book.published_date)} for book in books]

    return jsonify(book_list), 200

def update_book(book_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    data = request.get_json()
    book = Book.query.filter_by(id=book_id, user_id=user.id).first()

    if book is None:
        return jsonify({'message': 'Book not found or does not belong to the user'}), 404

    book.title = data['title']
    book.author = data['author']
    book.published_date = data['published_date']
    db.session.commit()

    return jsonify({'message': 'Book updated successfully'}), 200

@books_bp.route('/delete/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    book = Book.query.filter_by(id=book_id, user_id=user.id).first()

    if book is None:
        return jsonify({'message': 'Book not found or does not belong to the user'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'}), 200

