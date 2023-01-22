from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

todos = []

@app.route('/todos', methods=['GET'])
def get_todos():
    """
    Get all todos
    This endpoint returns all todos in the list
    ---
    responses:
      200:
        description: Returns all todos
    """
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    """
    Add a new todo
    This endpoint allows you to add a new todo to the list
    ---
    parameters:
      - name: todo
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Adds a new todo to the list
    """
    todo = request.form.get('todo')
    todos.append(todo)
    return jsonify(todos)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """
    Delete a todo
    This endpoint allows you to delete a todo from the list
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Deletes a todo from the list
    """
    del todos[todo_id]
    return jsonify(todos)
