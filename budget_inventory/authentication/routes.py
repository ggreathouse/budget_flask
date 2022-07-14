from flask import Blueprint, request, flash, jsonify, session
from flask_session import Session
from budget_inventory.models import User, db, check_password_hash, user_schema
from budget_inventory.helpers import token_required



auth = Blueprint('auth',__name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    firstName = request.json["firstName"]
    lastName = request.json["lastName"]
    username = request.json["username"]
    password = request.json["password"]

    user_exists = User.query.filter_by(username=username).first() is not None
    if user_exists:
        return jsonify({"error": "username already exists"})

    user = User(first_name=firstName, last_name=lastName, username=username, password=password)
            
    db.session.add(user)
    db.session.commit()

    flash(f"You have successfully created a user account: {username}", 'user-created')
    response = user_schema.dump(user)
    return jsonify(response)
            

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    username = request.json["username"]
    password = request.json["password"]

    

    logged_user = User.query.filter(User.username == username).first()
    if logged_user and check_password_hash(logged_user.password, password):
        flash('You were successfully logged in via username/password', 'auth-success')
        response = user_schema.dump(logged_user)
        user_token = response['token']
        session["token"] = user_token
        session["username"] = logged_user.username
        return jsonify(response)
    else:
        flash('Your username/password is incorrect', 'auth-failed')
    

@auth.route('/token', methods = ['GET'])
def get_token():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(username=username).first()

    return jsonify(user_schema.dump(user)['token'])


@auth.route('/logout', methods = ['POST'])
def logout_user():
    session.pop('username')
    return '200'
