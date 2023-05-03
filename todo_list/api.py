import json
from flask import Flask
from flask_restful import Resource, Api, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///todo_list.db'
api = Api(app)

sql_db = SQLAlchemy(app)

class ToDoModel(sql_db.Model):
    task_id = sql_db.Column(sql_db.Integer, primary_key=True)
    task = sql_db.Column(sql_db.String(200))
    details = sql_db.Column(sql_db.String(200))

    def __init__(self, task_id, task, details):
            self.task_id = task_id
            self.task = task
            self.details = details

    def get_id(self):
          return self.task_id

class AllTask(Resource):
    def get(self):
        todos = ToDoModel.query.all()
        todo_tasks = {}
        for task in todos:
            todo_tasks[task.task_id] = {"task": task.task, "details": task.details}
        return todo_tasks


args_post = reqparse.RequestParser()
args_post.add_argument('task', type=str, required=True, help="Add Task Title")
args_post.add_argument('details', type=str, required=True, help="Add Task Details")


args_put = reqparse.RequestParser()
args_put.add_argument('task', type=str)
args_put.add_argument('details', type=str)

todo_resource_fields = {
    "task_id": fields.Integer,
    "task": fields.String,
    "details": fields.String
}
class ToDo(Resource):
    @marshal_with(todo_resource_fields)
    def get(self, task_id):
        todo_task = ToDoModel.query.filter_by(task_id=task_id).first()
        if todo_task:
            return todo_task
        abort(404, message="Task not found")
    
    @marshal_with(todo_resource_fields)
    def post(self, task_id):
        args = args_post.parse_args()
        todo_task = ToDoModel.query.filter_by(task_id=task_id).first()
        if todo_task:
            abort(400, message="Task already exists")

        task = args['task']
        details = args['details']
        new_task = ToDoModel(task_id=task_id, details=details, task=task)
        sql_db.session.add(new_task)
        sql_db.session.commit()
        return new_task, 201
    
    @marshal_with(todo_resource_fields)
    def put(self, task_id):
        args = args_put.parse_args()
        todo_task = ToDoModel.query.filter_by(task_id=task_id).first()
        if not todo_task:
            abort(404, message="Task not found")
        
        if args.get('task'):
            todo_task.task = args['task']

        if args.get("details"):       
            todo_task.details = args['details']
        
        sql_db.session.commit()
        return todo_task
    
    def delete(self, task_id):
        todo_task = ToDoModel.query.filter_by(task_id=task_id).first()
        if not todo_task:
            abort(404, message="Task not found")
        sql_db.session.delete(todo_task)
        sql_db.session.commit()
        return "Task deleted successfully", 204
    

api.add_resource(ToDo, '/todos/<int:task_id>')
api.add_resource(AllTask, '/todos/')

if __name__ == '__main__':
    app.run(debug=True)