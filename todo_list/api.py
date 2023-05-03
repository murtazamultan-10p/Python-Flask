from flask import Flask
from flask_restful import Resource, Api, abort, reqparse


app = Flask(__name__)
api = Api(app)

args_post = reqparse.RequestParser()
args_post.add_argument('task', type=str, required=True, help="Add Task Title")
args_post.add_argument('details', type=str, required=True, help="Add Task Details")


args_put = reqparse.RequestParser()
args_put.add_argument('task', type=str)
args_put.add_argument('details', type=str)

todo_list = {1: {"task": "Flask-Restful", "details": "Demo program to get hands-on with flask-restful"}}

class AllTask(Resource):
    def get(self):
        return todo_list

class ToDo(Resource):

    def get(self, task_id):
        if task_id in todo_list:
            return todo_list[task_id]
        abort(404, message="Task not found")
    
    def post(self, task_id):
        args = args_post.parse_args()
        if task_id in todo_list:
            abort(400, message="Task already exists")

        task = args['task']
        details = args['details']
        new_task = {'task': task, 'details': details}
        todo_list[task_id] = new_task
        return todo_list[task_id]
    
    def put(self, task_id):
        args = args_put.parse_args()

        if task_id not in todo_list:
            abort(404, message="Task not found")
        
        if args.get('task'):
            task = args['task']
            todo_list[task_id]['task'] = task

        if args.get("details"):       
            details = args['details'] 
            todo_list[task_id]['details'] = details
        
        return todo_list[task_id]
    
    def delete(self, task_id):
        if task_id not in todo_list:
            abort(404, message="Task not found")
        del todo_list[task_id]
        return todo_list
    

api.add_resource(ToDo, '/todos/<int:task_id>')
api.add_resource(AllTask, '/todos/')



if __name__ == '__main__':
    app.run(debug=True)