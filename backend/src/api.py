import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
setup_db(app)
CORS(app)


class InvalidRecipe(Exception):
    def __init__(self, recipe, status_code):
        self.recipe = recipe
        self.status_code = status_code


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    all_drinks = Drink.query.order_by(Drink.id).all()
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in all_drinks]
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    all_drinks = Drink.query.order_by(Drink.id).all()
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in all_drinks]
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    body = request.get_json()
    drink_title = body.get('title')
    drink_recipe = body.get('recipe')
    print(drink_recipe)
    print(str(drink_recipe))
    #drink_recipe = verify_recipe_format(drink_recipe)
    new_drink = Drink(title= drink_title, recipe= str(drink_recipe))
    new_drink.insert()
    print(new_drink)
    print(new_drink.long())
    return jsonify({
        'success': True,
        'drinks': new_drink.long()
    })

#recipe should be list formated
#recipe should have the following format according to number of ingredients
#[{'color': string, 'name':string, 'parts':number}, {'color': string, 'name':string, 'parts':number}, ...]
def verify_recipe_format(recipe):
    print(recipe)
    if not isinstance(recipe, list) and not isinstance(recipe, dict):
        print("not list, not dict")
        #raise InvalidRecipe(recipe, 400)
    if isinstance(recipe, list):
        print("is list")
        for item in recipe:
            if not is_valid_recipe_item(item):
                raise InvalidRecipe(recipe, 400)
        return recipe
    elif isinstance(recipe, dict):
        print("is dict")
        is_valid_recipe_item(recipe)
        ret = []
        ret.append(recipe)
        return ret

def is_valid_recipe_item(recipe_item):
    color = recipe_item['color']
    name = recipe_item['name']
    parts = recipe_item['parts']
    if not isinstance(color, str) or not isinstance(name, str) or not isinstance(parts, (str,int,float)):
        return False
    return True

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
# @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
# @requires_auth('patch:drinks')
# def update_drink(payload, drink_id):
#     drink_to_be_updated = Drink.query.get(drink_id)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(HTTPException)
def handle_HTTPException(error):
    return jsonify({
        "success": False, 
        "error": error.code,
        "message": error.name
        }), error.code

@app.errorhandler(AuthError)
def handle_AuthExcption(error):
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": error.error
        }), error.status_code

@app.errorhandler(InvalidRecipe)
def handle_AuthExcption(error):
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": error.recipe
        }), error.status_code


