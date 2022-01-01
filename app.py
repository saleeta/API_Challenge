from flask import Flask, request
from app_service import AppService
import json

app = Flask(__name__)
appService = AppService();


@app.route('/')
def home() -> str:
    """[summary]

    Returns:
        str: [description]
    """
    return "App Works!!!"


@app.route('/api/tasks')
def tasks():
    return appService.get_tasks()


@app.route('/api/task', methods=['POST'])
def create_task():
    # a= request.json
    # print(a,'okay')
    request_data = request.get_json(force=True)
    print(request_data, "okay")
    task = request_data['task']
    return appService.create_task(task)


@app.route('/api/task', methods=['PUT'])
def update_task():
    request_data = request.get_json()
    return appService.update_task(request_data['task'])


@app.route('/api/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    return appService.delete_task(id)
