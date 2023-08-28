from flask import Blueprint, jsonify, make_response, request, session
from flask_login import login_required, logout_user, current_user
from pytz import timezone
from classes.errorhandler import ErrorHandler
from classes.models.User import User
from classes.requesthandler import Requesthandler
from setup import db, tz, login_manager

bp = Blueprint('auth', __name__)
handler = Requesthandler(db, tz)


@login_manager.user_loader
def load_user(user_id):
    return handler.fetch_user(user_id)

# * error handler for error codes.


@bp.errorhandler(Exception)
def internal_server_error(e):
    return ErrorHandler().handle(e)


@bp.errorhandler(500)
def internal_server_error_500(e):
    return make_response(jsonify({
        'msg': 'unknown internal server error'
    }), 500)


@bp.route('/')
def index():
    return jsonify({'msg': 'hello world'}), 200


@bp.post('/register', strict_slashes=False)
def register():
    result = handler.register(request.json)
    return jsonify(result), 200


@bp.post('/login/', strict_slashes=False)
def login():
    result = handler.login(request.json)
    return jsonify(result), 200


@bp.route('/logout/', strict_slashes=False)
@login_required
def logout():
    handler.logout()
    return jsonify({"msg": "logged user out"}), 200

# * creates the required tables in the database.

# * migrates stage(s) from a json file to the database. Also adds the project if it doesn't exist.


@bp.post('/migrate/project:<project_name>')
@login_required
def migrate_stages(project_name):
    handler.migrate_stages(project_name, request.json)
    return 'migration successful', 200


# * migrates all projects and stages from a json file to the database.
@bp.post('/migrate/projects')
@login_required
def migrate_projects():
    handler.migrate_projects(request.json)
    return 'migration successful', 200


@bp.post('/create_project')
@login_required
def create_project():
    # * adds a project to the database
    project = handler.create_project(request.json, current_user)
    return jsonify(project), 200


# * gets all projects names and ids from the database.
@bp.get('/projects:all')
@login_required
def get_projects():
    results = handler.get_projects(current_user)
    return results, 200



# * gets all stages from a project
@bp.get('/project:<project_id>/stages:all')
@login_required
def get_stages(project_id):
    result = handler.get_stages(project_id, current_user)
    return result, 200


@bp.post('/project:<project_id>/create_stage')
@login_required
def create_stage(project_id):
    result = handler.create_stage(request.json, project_id, current_user)
    return result, 200


@bp.route('/project:<project_id>/stage:<stage_id>', methods=['GET'])
@login_required
def get_stage(project_id, stage_id):
    # * gets information about a stage from a project
    result = handler.get_stage(project_id, stage_id, current_user)
    return result, 200


@bp.put('/project:<project_id>/stage:<stage_id>')
@login_required
def update_stage(project_id, stage_id):
    # TODO handler.update_stage(project_id, stage_id, request.json)
    # TODO implement this method. It should take a json and update all listed properties.
    # TODO Implement a route that allows the user to rename a stage in the database.
    # TODO Implement a route that allows the user to update a price of a stage in the database
    # TODO implement a route that allows the user to update the days & hours spent on a stage. This should automatically update the last update value of the stage.
    return 'stage updated', 200


@bp.put('/project:<project_id>')
def update_project(project_id):
    # TODO handler.update_project(project_id, request.json)
    # TODO implement this method. It should take a json and rename the project.
    return 'project updated', 200


@bp.delete('/project:<project_id>/stage:<stage_id>')
def delete_stage(project_id, stage_id):
    # TODO handler.delete_stage(project_id, stage_id)
    # TODO implement this method. It should delete the stage from the database.
    return 'stage deleted', 200


@bp.delete('/project:<project_id>')
def delete_project(project_id):
    # TODO handler.delete_project(project_id)
    # TODO implement this method. It should delete the project from the database.
    return 'project deleted', 200


# TODO Add user authentication and authorization so only an admin can migrate projects and stages.
# TODO Add user authentication so each user can only create edit and remove their own projects and stages.
