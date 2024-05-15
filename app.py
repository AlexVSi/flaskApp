from flask import Flask, render_template, request, redirect, url_for
import connect
from connect import s

app = Flask(__name__)

def get_orders():
	response = s.query(connect.Orders).all()
	orders =[]
	for r in response:
		name = s.query(connect.Users).where(r.id_user == connect.Users.id).one()
		orders.append({
			'id': r.id,
			'name': f'{name.firstname} {name.lastname} {name.surename}',
			'auto_number': r.auto_number,
			'violation_description': r.violation_description,
			'status': f'{s.query(connect.Status).where(r.status == connect.Status.id).one().status}',
		})
	return orders

@app.route('/')
def index():
	return render_template('index.html', auth_forbidden = False)

@app.route('/auth', methods=['POST'])
def auth():
	login = request.form['login']
	password = request.form['password']
	try:
		s.query(connect.Users).where(login == connect.Users.login, password == connect.Users.password).one()
		return redirect(url_for('orders'))
	except:
		return render_template('index.html', auth_forbidden = True)

@app.route('/registration')
def registration():
	return render_template('registration.html', duplicate_login = False)

@app.route('/reg', methods=['POST'])
def reg():
	login = request.form['login']
	try:
		s.query(connect.Users).where(login == connect.Users.login).one()
		return render_template('registration.html', duplicate_login = True)
	except:
		new_user = connect.Users(
			firstname=request.form['firstname'],
			lastname=request.form['lastname'],
			surename=request.form['surename'],
			phone=request.form['phone'],
			email=request.form['email'],
			login=request.form['login'],
			password=request.form['password'],
			role=1,
		)
		s.add(new_user)
		s.commit()
		return render_template('orders.html', auth_forbidden = True)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
	return render_template('orders.html', orders=get_orders())

@app.route('/add-order')
def add_order():
	return render_template('addOrder.html')

@app.route('/submit-order', methods=['POST'])
def submit_order():
	if request.method == 'POST':
		auto_number = request.form['auto_number']
		violation_description = request.form['violation_description']

		new_order = connect.Orders(
			id_user=1,
			auto_number=auto_number,
			violation_description=violation_description,
			status=1
			)
		s.add(new_order)
		s.commit()
		return redirect(url_for('orders'))

@app.route('/admin')
def admin():
	return render_template('admin.html')

if __name__ == '__main__':
	app.run(port=8000, host='0.0.0.0', debug=True)
