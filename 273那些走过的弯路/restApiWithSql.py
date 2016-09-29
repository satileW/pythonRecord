#!flask/bin/python
from flask import Flask, request, flash, url_for, redirect, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///MySQL.sqlite3'
app.config['SECRET_KEY']="random string"
db = SQLAlchemy(app)

class orders(db.Model):
	id = db.Column('student_id', db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(50))
	category = db.Column(db.String(200))
	description = db.Column(db.String(10))
	link = db.Column(db.String(10))
	estimated_costs = db.Column(db.String(10))
	submit_date = db.Column(db.String(10))
	status = db.Column(db.String(10))
	decision_date = db.Column(db.String(10))

	def __init__(self, name, email, category, description, link, estimated_costs, submit_date, status, decision_date):
		self.name = name
		self.email = email
		self.category = category
		self.description = description
		self.link = link
		self.estimated_costs = estimated_costs
		self.submit_date = submit_date
		self.status = status
		self.decision_date = decision_date        


@app.route('/v1/expenses')
def show_all():
    resp = make_response(render_template('show_all.html', orders=orders.query.all()), 200)
    return resp

# @app.route('/v1/expenses/<int:expense_id>', methods=['GET'])
# def get_order(expense_id):
#     if expense_id < 0:
#         abort(404)
#     orders=orders.query.all())

#     order = filter(lambda t: t['id'] == expense_id, orders)
#     if len(order) == 0:
#         abort(404)
#     return jsonify({'order': order[0]}),200,OK

# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/v1/expenses', methods=['POST'])
def create_order():
    # if not request.json or not 'title' in request.json:
    #     abort(400)
    if request.method == 'POST':
		if not request.form['name'] or not request.form['email'] or not request.form['category']or not request.form['description'] or not request.form['link'] or not request.form['estimated_costs'] or not request.form['submit_date']:
			flash('Please enter all the fields', 'error')
		else:
			new_order = orders(request.form['name'],
							   request.form['email'],
							   request.form['category'],
							   request.form['description'],
                               request.form['link'],
                               request.form['estimated_costs'],
                               "pending|approved|rejected|overbudget",
                               request.form[''])
			db.session.add(new_order)
			db.session.commit()
			flash('Record was successfully added')
    

    return jsonify({'order': new_order}), 201

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)