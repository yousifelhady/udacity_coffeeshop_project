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
!! NOTE THIS WILL DROP ALL RECORDS AND START THE DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN AND THEN RECOMMENT IT
'''
#db_drop_and_create_all()

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
    }), 200

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
    }), 200

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
    #check for drink title, as it should be unique
    if is_drink_title_exist(drink_title):
        print('drink title already exists: ' + drink_title)
        abort(422)
    drink_recipes = body.get('recipe')
    drink_recipes = verify_recipe_format(drink_recipes)
    recipes_as_string = json.dumps(drink_recipes)
    new_drink = Drink(title= drink_title, recipe= recipes_as_string)
    new_drink.insert()
    return jsonify({
        'success': True,
        'drinks': [new_drink.long()]
    }), 200

#recipe should be list formated
#recipe should have the following format according to number of ingredients
#[{'color': string, 'name':string, 'parts':number}, {'color': string, 'name':string, 'parts':number}, ...]
def verify_recipe_format(recipe):
    if not isinstance(recipe, list) and not isinstance(recipe, dict):
        raise InvalidRecipe(str(recipe), 400)
    if isinstance(recipe, list):
        for item in recipe:
            if not is_valid_recipe_item(item):
                raise InvalidRecipe(str(recipe), 400)
        return recipe
    elif isinstance(recipe, dict):
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

def is_drink_title_exist(drink_title):
    drink_exist = Drink.query.filter_by(title=drink_title).all()
    if drink_exist == []:
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
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    drink_to_be_updated = Drink.query.get(drink_id)
    if drink_to_be_updated is None:
        abort(404)
    drink_to_be_updated_title = drink_to_be_updated.title
    drink_to_be_updated_recipes = drink_to_be_updated.recipe

    body = request.get_json()
    new_title = body.get('title')
    if new_title is not None:
        if new_title != drink_to_be_updated_title:
            #check for drink title, as it should be unique
            if is_drink_title_exist(new_title):
                abort(422)
            drink_to_be_updated.title = new_title

    new_recipes = body.get('recipe')
    if new_recipes is not None:
        new_recipes = verify_recipe_format(new_recipes)
        recipes_as_string = json.dumps(new_recipes)
        if recipes_as_string != drink_to_be_updated_recipes:
            drink_to_be_updated.recipe = recipes_as_string
    
    drink_to_be_updated.update()
    return jsonify({
        'success': True,
        'drinks': [drink_to_be_updated.long()]
    }), 200

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
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.get(drink_id)
    if drink is None:
        abort(404)
    drink.delete()
    return jsonify({
        'success': True,
        'delete': drink_id
    }), 200

## Error Handling

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
def handle_InvalidRecipe(error):
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": "Wrong recipe database format: " + error.recipe
        }), error.status_code