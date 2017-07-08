import db_client
import json
from flask import Flask, request, Blueprint, Response, jsonify, redirect, abort

app = Flask(__name__)

################################################################################
# RESTful Endpoints

def urls(url_id):
    if request.method == 'GET':
        db_response, url = db_client.get_url(url_id)

        if db_response:
            response = redirect(url, code=301)
            return response

        else:
            abort(404)

    else: #Delete
        db_response = db_client.delete_url(url_id)
        if db_response:
            return Response(status=200)

        else:
            abort(404)

def register_user_urls(user_id):
    try:
        json_data = request.get_json(force=True)
        url = json_data['url']

        if url.find("http://") != 0 and url.find("https://") != 0:
            url = 'http://' + url

        partial_short_url = 'http://' + request.host
        db_response, stats = db_client.create_new_url(url, partial_short_url, user_id)

        if db_response:
            response = jsonify(stats)
            response.status_code = 201
            return response

        else:
            abort(409)

    except KeyError as err:
        print('Could not parse JSON data')
        abort(400)

def user_stats(user_id): #Specific user URL stats
    db_response, stats = db_client.get_user_stats(user_id)

    if db_response:
        response = jsonify(stats)
        response.status_code = 200
        return response

    else:
        abort(404)

def stats(url_id=None):
    if url_id is None: #Global
        response = jsonify(db_client.get_global_stats())
        response.status_code = 200
        return response

    else: #Specific
        db_response, stats = db_client.get_url_stats(url_id)

        if db_response:
            response = jsonify(stats)
            response.status_code = 200
            return response

        else:
            abort(404)

def register_users():
    try:
        json_data = request.get_json(force=True)
        user_id = json_data['id']

        db_response = db_client.create_new_user(user_id)

        if db_response:
            response = jsonify({'id' : user_id})
            response.status_code = 201
            return response

        else:
            abort(409)

    except KeyError as err:
        print('Could not parse JSON data')
        abort(400)

#DELETE /user/:userId was the specification. Maybe they meant to utilize 'users'
#like the other URLs?
def delete_user(user_id):
    db_response = db_client.delete_user(user_id)

    if db_response:
        response = Response(status=200)
        return response

    else:
        abort(404)

def coffee(): #Identifies the server as a teapot (not coffee machine)
    abort(418)

################################################################################
# Routing rules

users_bp = Blueprint('users_blueprint', __name__, url_prefix='/users/<string:user_id>')
stats_bp = Blueprint('stats_blueprint', __name__, url_prefix='/stats')

users_bp.add_url_rule('/urls', view_func=register_user_urls, methods=['POST'], strict_slashes=False)
users_bp.add_url_rule('/stats', view_func=user_stats, methods=['GET'], strict_slashes=False)

stats_bp.add_url_rule('/', view_func=stats, methods=['GET']) #Returns global stats
stats_bp.add_url_rule('/<int:url_id>', view_func=stats, methods=['GET'], strict_slashes=False) #Returns stats from a specific URL

app.add_url_rule('/urls/<int:url_id>', view_func=urls, methods=['GET', 'DELETE'], strict_slashes=False)
app.add_url_rule('/users', view_func=register_users, methods=['POST'], strict_slashes=False)
app.add_url_rule('/user/<string:user_id>', view_func=delete_user, methods=['DELETE'], strict_slashes=False)
app.add_url_rule('/coffee', view_func=coffee, methods=['GET'], strict_slashes=False) #This is just a little joke :)

app.register_blueprint(users_bp)
app.register_blueprint(stats_bp)

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=5000)
