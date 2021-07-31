#-----------------------------------------------------------#
# Imports.
#-----------------------------------------------------------#
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

#-----------------------------------------------------------#
# Connections.
#-----------------------------------------------------------#
app = Flask(__name__)
setup_db(app)
CORS(app)
db_drop_and_create_all()


#-----------------------------------------------------------#
# after_request.
#-----------------------------------------------------------#
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origins', '*')
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'
    )
    return response


#-----------------------------------------------------------#
# Get drinks.
#-----------------------------------------------------------#
@app.route('/drinks', methods=['GET'])
def get_drinks():
    all_drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in all_drinks]
    })


#-----------------------------------------------------------#
# Get drinks-detail.
#-----------------------------------------------------------#
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    all_drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in all_drinks]
    })


#-----------------------------------------------------------#
# Post drinks.
#-----------------------------------------------------------#
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    body = request.get_json()
    try:
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        drink = Drink(
            title=title,
            recipe=json.dumps(recipe)
        )
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }, 200)
    except:
        abort(422)


#-----------------------------------------------------------#
# Patch drinks.
#-----------------------------------------------------------#
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, id):
    body = request.get_json()
    try:
        drink = Drink.query.get(id)
        if drink is None:
            abort(404)
        if 'title' in body:
            drink.title = body['title']
        if 'recipe' in body:
            drink.recipe = json.dumps(body['recipe'])
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        abort(422)


#-----------------------------------------------------------#
# Delete drinks.
#-----------------------------------------------------------#
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    body = request.get_json()
    try:
        drink = Drink.query.get(id)
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except:
        abort(422)


#-----------------------------------------------------------#
# errorhandler for 400.
#-----------------------------------------------------------#
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400, 
        'message': 'Bad request.'
    }), 400


#-----------------------------------------------------------#
# errorhandler for 404.
#-----------------------------------------------------------#
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found.'
    }), 404


#-----------------------------------------------------------#
# errorhandler for 405.
#-----------------------------------------------------------#
@app.errorhandler(405)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Not found.'
    }), 405


#-----------------------------------------------------------#
# errorhandler for 422.
#-----------------------------------------------------------#
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
    }), 422


#-----------------------------------------------------------#
# errorhandler for AuthError.
#-----------------------------------------------------------#
@app.errorhandler(AuthError)
def auth_error(AuthError):
    return jsonify({
        'success': False,
        'error': AuthError.status_code,
        'message': AuthError.error['description']
    }), AuthError.status_code
