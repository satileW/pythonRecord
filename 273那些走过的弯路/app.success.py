#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for, json

app = Flask(__name__)

@app.route('/v1/expenses/<int:expense_id>', methods=['GET'])
def get_order(expense_id):
    orders = json.load(open('obj.json', 'r'))

    order = filter(lambda t: t['id'] == expense_id, orders)
    if len(order) == 0:
        abort(404)
    return jsonify({'order': order[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/v1/expenses', methods=['POST'])
def create_order():
    if not request.json or not 'title' in request.json:
        abort(400)
    orders = json.load(open('obj.json', 'r'))
    order = {
        'id': orders[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    orders.append(order)

    fp = open('obj.json', 'w+')
    json.dump(orders, fp)
    return jsonify({'order': order}), 201

@app.route('/v1/expenses/<int:expense_id>', methods=['PUT'])
def update_order(expense_id):
    orders = json.load(open('obj.json', 'r'))
    
    order = filter(lambda t: t['id'] == expense_id, orders)
    if len(order) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    order[0]['title'] = request.json.get('title', order[0]['title'])
    order[0]['description'] = request.json.get('description', order[0]['description'])
    order[0]['done'] = request.json.get('done', order[0]['done'])
    
    fp = open('obj.json', 'w+')
    json.dump(orders, fp)
    return jsonify({'order': order[0]})

@app.route('/v1/expenses/<int:expense_id>', methods=['DELETE'])
def delete_order(expense_id):
    orders = json.load(open('obj.json', 'r'))

    order = filter(lambda t: t['id'] == expense_id, orders)
    if len(order) == 0:
        abort(404)
    orders.remove(order[0])
    fp = open('obj.json', 'w+')
    json.dump(orders, fp)
    return jsonify({'result': True})

@app.route('/v1/expenses', methods=['GET'])
def get_orders():
    orders = json.load(open('obj.json', 'r'))  
    return jsonify({'orders': map(make_public_order, orders)})
    
def make_public_order(order):
    new_order = {}
    for field in order:
        if field == 'id':
            new_order['uri'] = url_for('get_order', expense_id=order['id'], _external=True)
        else:
            new_order[field] = order[field]
    return new_order
if __name__ == '__main__':
    app.run(debug=True)