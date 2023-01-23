# in todos.py
from flask import Blueprint, jsonify, request
from .models import db, Todo

todos_blueprint = Blueprint('todos', __name__)

@todos_blueprint.route('/todos', methods=['GET'])
def get_todos():
    """
    Get all todos
    This endpoint returns all todos in the database
    ---
    responses:
      200:
        description: Returns all todos
    """
    todos = Todo.query.all()
    return jsonify([todo.text for todo in todos])

@todos_blueprint.route('/todos', methods=['POST'])
def add_todo():
    """
    Add a new todo
    This endpoint allows you to add a new todo to the database
    ---
    parameters:
      - name: todo
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Adds a new todo to the database
    """
    todo = request.form.get('todo')
    new_todo = Todo(todo)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(message="Todo added successfully")

@todos_blueprint.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """
    Delete a todo
    This endpoint allows you to delete a todo from the database
    ---
    parameters:
      - name: todo_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Deletes a todo from the database
    """
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify(message="Todo deleted successfully")
