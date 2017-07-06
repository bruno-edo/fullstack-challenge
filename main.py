from flask import Flask, request, Blueprint

users_bp= Blueprint('users_blueprint', __name__, url_prefix='/users/<string:user_id>')
app = Flask(__name__)

@app.route('/urls/<int:id>/', methods=['GET', 'DELETE'])
def urls(id):
    if request.method == 'GET':
        return 'get urls'
    else:
        pass

@users_bp.route('/urls/', methods=['POST'])
def urls(user_id):
    pass

@users_bp.route('/stats/', methods=['GET'])
def stats(user_id):
    return 'user stats'

@app.route('/stats/', methods=['GET']) #Returns global stats
@app.route('/stats/<int:stats_id>/', methods=['GET']) #Returns stats from a specific URL
def global_stats(stats_id=None):
    if stats_id is None: #global
        return 'global stats'

    else: #specific
        return 'specific stats'


@app.route('/users/', methods=['POST'])
def users():
    json_data = request.get_json()
    user_id = json_data['id']
    print(json_data)

@app.route('/user/<string:user_id>/', methods=['DELETE']) #DELETE /user/:userId was the specification. Maybe they meant to utilize 'users' like in the other URLs?
def delete(user_id):
    pass

if __name__ == '__main__':
    app.register_blueprint(users_bp)
    app.config['DEBUG'] = True
    app.run(host='localhost', port=5000)
    #ContentType: application/json -> para todos os métodos menos o de redirecão
