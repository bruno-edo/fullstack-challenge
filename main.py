import db_client

from flask import Flask, request, Blueprint, Response, jsonify

users_bp = Blueprint('users_blueprint', __name__, url_prefix='/users/<string:user_id>')
stats_bp = Blueprint('stats_blueprint', __name__, url_prefix='/stats')
app = Flask(__name__)

@app.route('/urls/<int:id>', methods=['GET', 'DELETE'], strict_slashes=False)
def urls(id):
    if request.method == 'GET':
        return 'get urls'
    else:
        pass

@users_bp.route('/urls', methods=['POST'], strict_slashes=False)
def urls(user_id):
    json_data = request.get_json(force=True)
    url = json_data['url']
    short_url = 'temp'
    db_response, stats = db_client.create_new_url(url, short_url, user_id)

    if db_response:
        response = jsonify(stats)
        response.status_code = 201

    else:
        response = Response(status=409)

    return response

@users_bp.route('/stats', methods=['GET'], strict_slashes=False)
def stats(user_id): #Specific user URL stats
    db_response, stats = db_client.get_user_stats(user_id)

    if db_response:
        response = jsonify(stats)
        response.status_code = 200

    else:
        response = Response(status=404)
        #response.headers['Content-Type'] = 'application/json'

    return response

@stats_bp.route('/', methods=['GET']) #Returns global stats
@stats_bp.route('/<int:url_id>', methods=['GET'], strict_slashes=False) #Returns stats from a specific URL
def stats(url_id=None):
    if url_id is None: #global
        #return 'global stats'
        return 'Hello, world! running on %s' % request.host

    else: #specific
        db_response, stats = get_url_stats(url_id)

        if db_response:
            response = jsonify(stats)
            response.status_code = 200

        else:
            response = Response(status=404)

        return 'specific stats'

@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    json_data = request.get_json(force=True)
    user_id = json_data['id']

    db_response = db_client.create_new_user(user_id)

    if db_response:
        response = jsonify({'id' : user_id})
        response.status_code = 201

    else: #error: already exists
        response = Response(status=409)
        #response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/user/<string:user_id>', methods=['DELETE'], strict_slashes=False) #DELETE /user/:userId was the specification. Maybe they meant to utilize 'users' like in the other URLs?
def delete(user_id):
    pass

#These must be placed here, as the code that runs the blueprints has to be instantiated before registering the blueprint
app.register_blueprint(users_bp)
app.register_blueprint(stats_bp)

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='localhost', port=5000)
    #ContentType: application/json -> para todos os métodos menos o de redirecão
