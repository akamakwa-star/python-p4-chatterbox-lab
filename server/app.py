#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message  # Assuming you created a Message model

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

# Create tables
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return '<h1>Chatterbox Flask API</h1>'


# GET all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200


# POST a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or 'body' not in data or 'username' not in data:
        return jsonify({"error": "Missing body or username"}), 400

    message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201


# PATCH a message by id
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    data = request.get_json()
    if not data or 'body' not in data:
        return jsonify({"error": "Missing body"}), 400

    message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict()), 200


# DELETE a message by id
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()
    return jsonify({}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
