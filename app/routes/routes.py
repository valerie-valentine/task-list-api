from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, abort, request
from app.helpers import validate_model


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        task = Task.from_dict(request_body)
        db.session.add(task)
        db.session.commit()

        return make_response({"task": task.to_dict()}, 201)

    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body.get("completed_at")

        db.session.commit()

        return make_response({"task": task.to_dict()}, 200)
    
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_book(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

