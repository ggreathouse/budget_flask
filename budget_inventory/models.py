from enum import unique
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    username = db.Column(db.String(50), nullable = False, unique=True)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    budget = db.relationship('Budget', backref = 'owner', lazy=True)

    def __init__(self, username, first_name, last_name, password = '', id='', g_auth_verify = False, token = ''):
        self.id = self.set_id()
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.g_auth_verify = g_auth_verify
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.username} has been added to the database"

class Budget(db.Model):
    id = db.Column(db.String, primary_key = True)
    month = db.Column(db.String(150))
    income = db.Column(db.Integer, nullable = False)
    rent = db.Column(db.Integer, nullable = True)
    utilities = db.Column(db.Integer, nullable = True)
    internet = db.Column(db.Integer, nullable = True)
    insurance = db.Column(db.Integer, nullable = True)
    phone = db.Column(db.Integer, nullable = True)
    misc_bills = db.Column(db.Integer, nullable = True)
    groceries = db.Column(db.Integer, nullable = True)
    dine_out = db.Column(db.Integer, nullable = True)
    transportation = db.Column(db.Integer, nullable = True)
    loans = db.Column(db.Integer, nullable = True)
    subscriptions = db.Column(db.Integer, nullable = True)
    savings = db.Column(db.Integer, nullable = True)
    clothing = db.Column(db.Integer, nullable = True)
    entertainment = db.Column(db.Integer, nullable = True)
    other = db.Column(db.Integer, nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, month, income, rent, utilities, internet, insurance, phone, 
                misc_bills, groceries, dine_out, transportation, loans, subscriptions,
                savings, clothing, entertainment, other, user_token, id = ''):
                
        self.id = self.set_id()
        self.month = month
        self.income= income
        self.rent = rent
        self.utilities = utilities
        self.internet = internet
        self.insurance = insurance
        self.phone = phone
        self.misc_bills = misc_bills
        self.groceries = groceries
        self.dine_out = dine_out
        self.transportation = transportation
        self.loans = loans
        self.subscriptions = subscriptions
        self.savings = savings
        self.clothing = clothing
        self.entertainment = entertainment
        self.other = other
        self.user_token = user_token

    def set_id(self):
        return str((secrets.token_urlsafe()))

    def __repr__(self):
        return f"The month of {self.month} has been added to the database"

class BudgetSchema(ma.Schema):
    class Meta:
        fields = ['id', 'month', 'income', 'rent', 'utilities', 'internet', 'insurance', 
                      'phone', 'misc_bills', 'groceries', 'dine_out', 'transportation', 'loans',
                      'subscriptions', 'savings', 'clothing', 'entertainment', 'other']
class UserSchema(ma.Schema):
    class Meta:
        fields =['first_name', 'last_name', 'username', 'password', 'token']
budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)
user_schema = UserSchema()
