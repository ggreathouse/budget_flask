from urllib import response
from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from budget_inventory.helpers import token_required
from budget_inventory.models import db, User, Budget, budget_schema, budgets_schema


api = Blueprint('api', __name__, url_prefix = '/api')



@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some' : 'value'}

# CREATE BUDGET ENPOINT
@api.route('/budget', methods = ['POST'])
@token_required
def create_budget(current_user_token):
    month = request.json['month']
    income = request.json['income']
    rent = request.json['rent']
    utilities = request.json['utilities']
    internet = request.json['internet']
    insurance = request.json['insurance']
    phone = request.json['phone']
    misc_bills = request.json['misc_bills']
    groceries = request.json['groceries']
    dine_out = request.json['dine_out']
    transportation = request.json['transportation']
    loans = request.json['loans']
    subscriptions = request.json['subscriptions']
    savings = request.json['savings']
    clothing = request.json['clothing']
    entertainment = request.json['entertainment']
    other = request.json['other']
    user_token = current_user_token


    budget = Budget(month, income, rent, utilities, internet, insurance, phone, misc_bills, 
                    groceries, dine_out, transportation, loans, subscriptions, savings, 
                    clothing, entertainment, other, user_token=current_user_token)
    db.session.add(budget)
    db.session.commit()

    response = budget_schema.dump(budget)
    return jsonify(response)

# RETRIEVE ALL BUDGETS ENDPOINT
@api.route('/budget', methods = ['GET'])
@token_required
def get_budgets(current_user_token):
    owner = current_user_token
    budgets = Budget.query.filter_by(user_token = owner).all()
    response = budgets_schema.dump(budgets)
    return jsonify(response)


# RETIREVE ONE BUDGET ENDPOINT
@api.route('/budget/<id>', methods = ['GET'])
@token_required
def get_budget(current_user_token, id):
    owner = current_user_token
    if owner == current_user_token:
        budget = Budget.query.get(id)
        response = budget_schema.dump(budget)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# UPDATE BUDGET ENDPOINT
@api.route('/budget/<id>', methods = ['POST', 'PUT'])
@token_required
def update_budget(current_user_token, id):
    budget = Budget.query.get(id)

    budget.month = request.json['month']
    budget.income = request.json['income']
    budget.rent = request.json['rent']
    budget.utilities = request.json['utilities']
    budget.internet = request.json['internet']
    budget.insurance = request.json['insurance']
    budget.phone = request.json['phone']
    budget.misc_bills = request.json['misc_bills']
    budget.groceries = request.json['groceries']
    budget.dine_out = request.json['dine_out']
    budget.transportation = request.json['transportation']
    budget.loans = request.json['loans']
    budget.subscriptions = request.json['subscriptions']
    budget.savings = request.json['savings']
    budget.clothing = request.json['clothing']
    budget.entertainment = request.json['entertainment']
    budget.other = request.json['other']
    budget.user_token = current_user_token

    db.session.commit()
    response = budget_schema.dump(budget)
    return jsonify(response)

    # DELETE BUDGET ENDPOINT
@api.route('/budget/<id>', methods = ['DELETE'])
@token_required
def delete_budget(current_user_token, id):
    budget = Budget.query.get(id)
    db.session.delete(budget)
    db.session.commit()
    response = budget_schema.dump(budget)
    return jsonify(response)