#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for, json

app = Flask(__name__)

# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})
tasks = json.load(open('obj.json', 'r'))

@app.route('/v1/expenses/<int:expense_id>', methods=['GET'])
def get_task(expense_id):
    task = filter(lambda t: t['id'] == expense_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/v1/expenses', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    fp = open('obj.json', 'w+')
    json.dump(task, fp)
    return jsonify({'task': task}), 201

@app.route('/v1/expenses/<int:expense_id>', methods=['PUT'])
def update_task(expense_id):
    task = filter(lambda t: t['id'] == expense_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/v1/expenses/<int:expense_id>', methods=['DELETE'])
def delete_task(expense_id):
    task = filter(lambda t: t['id'] == expense_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
@app.route('/v1/expenses', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': map(make_public_task, tasks)})
    
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', expense_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task
if __name__ == '__main__':
    app.run(debug=True)

     #{'tasks': tasks}
    #fp = open('obj.json', 'w')
    #json.dump(tasks, fp)
    #return jsonify({'tasks': tasks})