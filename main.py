import db_client
import json
from flask import Flask, request, Blueprint, Response, jsonify, redirect

users_bp = Blueprint('users_blueprint', __name__, url_prefix='/users/<string:user_id>')
stats_bp = Blueprint('stats_blueprint', __name__, url_prefix='/stats')
app = Flask(__name__)

@app.route('/urls/<int:url_id>', methods=['GET', 'DELETE'], strict_slashes=False)
def urls(url_id):
    if request.method == 'GET':
        db_response, url = db_client.get_url(url_id)

        if db_response:
            response = redirect(url, code=301)

        else:
            response = Response(status=404)

        return response

    else:
        db_client.delete_url(url_id)
        return Response(status=200)

@users_bp.route('/urls', methods=['POST'], strict_slashes=False)
def user_urls(user_id):
    json_data = request.get_json(force=True)
    url = json_data['url']

    if url.find("http://") != 0 and url.find("https://") != 0:
        url = 'http://' + url

    partial_short_url = 'http://' + request.host
    db_response, stats = db_client.create_new_url(url, partial_short_url, user_id)

    if db_response:
        response = jsonify(stats)
        response.status_code = 201

    else:
        response = Response(status=409)
        response.headers['Content-Type'] = 'application/json'

    return response

@users_bp.route('/stats', methods=['GET'], strict_slashes=False)
def stats(user_id): #Specific user URL stats
    db_response, stats = db_client.get_user_stats(user_id)

    if db_response:
        response = jsonify(stats)
        response.status_code = 200

    else:
        response = Response(status=404)
        response.headers['Content-Type'] = 'application/json'

    return response

@stats_bp.route('/', methods=['GET']) #Returns global stats
@stats_bp.route('/<int:url_id>', methods=['GET'], strict_slashes=False) #Returns stats from a specific URL
def stats(url_id=None):
    if url_id is None: #global
        response = jsonify(db_client.get_global_stats())
        response.status_code = 200
        return response

    else: #specific
        db_response, stats = db_client.get_url_stats(url_id)

        if db_response:
            response = jsonify(stats)
            response.status_code = 200

        else:
            response = Response(status=404)
            response.headers['Content-Type'] = 'application/json'

        return response

@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    json_data = request.get_json(force=True)
    user_id = json_data['id']

    db_response = db_client.create_new_user(user_id)

    if db_response:
        response = jsonify({'id' : user_id})
        response.status_code = 201

    else:
        response = Response(status=409)
        response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/user/<string:user_id>', methods=['DELETE'], strict_slashes=False) #DELETE /user/:userId was the specification. Maybe they meant to utilize 'users' like in the other URLs?
def delete(user_id):
    db_client.delete_user(user_id)
    response = Response(status=200)
    response.headers['Content-Type'] = 'application/json'
    return response

#These must be placed here, as the code that runs the blueprints has to be instantiated before registering the blueprint
app.register_blueprint(users_bp)
app.register_blueprint(stats_bp)

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='localhost', port=5000)
    #ContentType: application/json -> para todos os métodos menos o de redirecão
