from flask import Flask, request, jsonify
from models import Project, db
from decouple import config

app = Flask(__name__)

from db import configure_database
configure_database(app)
with app.app_context():
    db.create_all()


app.config['SECRET_KEY'] = config('SECRET_KEY')


@app.route('/')
def home():
    return jsonify({"message": "Server is running", "status": "OK"})


@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    project_list = [{"id": project.id, "title": project.title, "description": project.description, "completed": project.completed, "created_at": project.created_at} for project in projects]
    return jsonify(project_list)

@app.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.get(id)
    if project:
        return jsonify({"id": project.id, "title": project.title, "description": project.description, "completed": project.completed, "created_at": project.created_at})
    else:
        return jsonify({"error": "Project not found"}, 404)

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project = Project(title=data['title'], description=data['description'], completed=data['completed'])
    db.session.add(project)
    db.session.commit()
    return jsonify({"id": project.id, "title": project.title, "description": project.description, "completed": project.completed, "created_at": project.created_at})

@app.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"error": "Project not found"}, 404)

    data = request.get_json()
    project.title = data['title']
    project.description = data['description']
    project.completed = data['completed']
    db.session.commit()
    return jsonify({"id": project.id, "title": project.title, "description": project.description, "completed": project.completed, "created_at": project.created_at})

@app.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"error": "Project not found"}, 404)

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)