import json
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)

@app.route('/')
def root():
    return render_template('index.html')

@app.route("/api/todos/<username>", methods=['GET', 'POST', 'PUT', 'DELETE'])
# @app.route("/api/todos", methods=['GET'])
def contacts(username = None):
    if request.method == 'GET':
        if username is not None:
            user = User.query.filter(User.username.like("%"+username+"%")).first()
            return jsonify(user.serialize()), 200        
        else:
            pass
            # users = User.query.all()
            # users = list(map(lambda user: user.serialize(), users))
            # return jsonify(users), 200
    if request.method == 'POST':
        user = User.query.filter(User.username.like("%"+username+"%")).first()
        # username = request.json.get("username", None)
        if not user:
            user = User()
            user.username = username
            user.todos = json.dumps([{"label": "Sample task", "done": False}])
            user.save()
            return jsonify(user.serialize()), 201
        else:
           return jsonify({"error": "Username already exists"}), 400
    if request.method == 'PUT':
        user = User.query.filter(User.username.like(""+username+"%")).first()
        username = request.json.get("username", None)
        todos = request.json.get("todos", None)
        if not username:
            return jsonify({"error": "Username is required"}), 400
        if not todos: 
            return jsonify({"error": "Add some to dos"}), 400            
        if not user:
            return jsonify({"msg": "User not found"}), 404
        user.username = username
        user.todos = json.dumps(todos) 
        user.update()
        return jsonify(user.serialize()), 200
    if request.method == 'DELETE':
        user = User.query.filter(User.username.like(""+username+"%")).first()
        if not user:
            return jsonify({"msg": "User not found"}), 404
        user.delete()
        return jsonify({"success": "User was deleted"}), 200


if __name__ == "__main__":
    manager.run()