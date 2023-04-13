# To handle when a User adds/unadds another user as a friend or follows/unfollows a friend
from flask_restx import Resource, Namespace, fields
from models import User
from connection import DbConnection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flask import Flask, request, jsonify, make_response

social_ns = Namespace('social', description='Social related operations')

friend_model = social_ns.model(
    'Friend',
    {
        'username': fields.String(required=True, description='Username'),
    },
)

follow_model = social_ns.model(
    'Follow',
    {
        'username': fields.String(required=True, description='Username'),
    },
)

@social_ns.route('/addfriend')
class AddFriend(Resource):
    @social_ns.expect(friend_model)
    def post(self):
        data = request.get_json()

        username = data['username']

        # Check if the user already exists
        conn = DbConnection.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        if not result:
            DbConnection.close_connection(conn)
            return make_response(jsonify({'error': 'Username does not exist'}), 409)
        
        # If the user exists, add the user as a friend
        cur = conn.cursor()
        cur.execute("INSERT INTO friends (username, friendname) VALUES (%s, %s)", (get_jwt_identity(), username))
        conn.commit()
        cur.close()
        DbConnection.close_connection(conn)
        return make_response(jsonify({'message': 'Friend added successfully'}), 200)