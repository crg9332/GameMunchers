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

auth_ns = Namespace('auth', description='Authentication related operations')

signup_model = auth_ns.model(
    'Signup', 
    {
        'username': fields.String(required=True, description='Username'),
        'email': fields.String(required=True, description='Email'),
        'password': fields.String(required=True, description='Password'),
        'firstname': fields.String(required=False, description='First name'),
        'lastname': fields.String(required=False, description='Last name'),
    },
)

login_model = auth_ns.model(
    'Login',
    {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password'),
    },
)

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()

        username = data['username']
        email = data['email']
        password = data['password']
        firstname = data['firstname']
        lastname = data['lastname']

        if firstname == "":
            firstname = None
        if lastname == "":
            lastname = None

        # Check if the user already exists
        conn = DbConnection.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        if result:
            DbConnection.close_connection(conn)
            return make_response(jsonify({'error': 'Username already exists'}), 409)
        
        # Check if the email already exists
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        if result:
            DbConnection.close_connection(conn)
            return make_response(jsonify({'error': 'Email already exists'}), 409)
        
        # If the user doesn't exist, create a new user
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, firstname, lastname, userpassword) VALUES (%s, %s, %s, %s, %s)", (username, email, firstname, lastname, generate_password_hash(password, method='sha256')))
        conn.commit()
        cur.close()
        DbConnection.close_connection(conn)
        
        return make_response(jsonify({'message': 'User created successfully'}), 201)

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()

        username = data['username']
        password = data['password']

        # Check if the user exists
        conn = DbConnection.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT userpassword FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        if not result:
            DbConnection.close_connection(conn)
            return make_response(jsonify({'error': 'Username not found'}), 404)


        # If the user exists, check the password
        if check_password_hash(result[0], password):
            # update the user's last login
            cur = conn.cursor()
            cur.execute("UPDATE users SET lastaccesseddate = NOW() WHERE username = %s", (username,))
            conn.commit()
            cur.close()

            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            DbConnection.close_connection(conn)
            return make_response(jsonify({'message': 'Login successful', 'access_token': access_token, 'refresh_token': refresh_token}), 200)
        else:
            DbConnection.close_connection(conn)
            return make_response(jsonify({'error': 'Wrong password'}), 401)

@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return make_response(jsonify({'access_token': access_token}), 200)
