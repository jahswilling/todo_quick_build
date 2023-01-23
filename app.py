from flask import Flask, jsonify, request
from flasgger import Swagger
from .models import db, Todo
from .auth import auth_blueprint
from .todos import todos_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(todos_blueprint)

swagger = Swagger(app)

if __name__ == '__main__':
    app.run(debug=True)
