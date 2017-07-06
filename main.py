from flask import Flask, request, Blueprint

users_bp= Blueprint('users_blueprint', __name__)

app = Flask(__name__)
app.register_blueprint(users_bp, url_prefix='/users/<string:userid>')


@app.route('/urls/<int:id>', methods=['GET', 'DELETE'])
def urls(id):
    if request.method == 'GET':
        pass
    else:
        pass

@users_bp.route('/urls', methods=['POST'])
def urls(userid):
    pass

@users_bp.route('/stats', methods=['GET'])
def stats(userid):
    pass

@app.route('/stats', methods=['GET']) #Returns global stats
@app.route('/stats/<int:id>', methods=['GET']) #Returns stats from a specific URL
def stats(): #global
    pass
def stats(id): #specific url
    pass

@app.route('/users', methods=['POST'])
def users():
    json_data = request.get_json()
    user_id = json_data['id']
    print(json_data)

@app.route('/user/<string:userid>', methods=['DELETE']) #DELETE /user/:userId was the specification. Maybe they meant to utilize 'users' like in the other URLs?
def delete(userid):
    pass

if __name__ == '__main__':
    pass
    #ContentType: application/json -> para todos os métodos menos o de redirecão
