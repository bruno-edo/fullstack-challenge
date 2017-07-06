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
    pass

@users_bp.route('/stats', methods=['GET'], strict_slashes=False)
def stats(user_id): #Specific user URL stats
    return 'user stats'

@stats_bp.route('/', methods=['GET']) #Returns global stats
@stats_bp.route('/<int:stats_id>', methods=['GET'], strict_slashes=False) #Returns stats from a specific URL
def stats(stats_id=None):
    if stats_id is None: #global
        return 'global stats'

    else: #specific
        return 'specific stats'

@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    json_data = request.get_json(force=True)
    user_id = json_data['id']
    print(json_data)

    db_response = db_client.create_new_user(user_id)

    if db_response:
        response = jsonify({'id' : user_id})
        response.status_code = 201

    else: #error: already exists
        response = Response(status=409)

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
