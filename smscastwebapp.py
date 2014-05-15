from flask import Flask, jsonify, render_template, request, json, redirect, url_for
from mocksmscast import LibSMSCast
from libaddrbook import LibAddrBook
from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager
import user

app = Flask(__name__)
app.secret_key = 'abcdgfkfdhgslkjh' # lol

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route('/send')
@login_required
def send():
	client = LibSMSCast()
	addr = LibAddrBook()

	msg = request.args.get('msg')
	tostr = request.args.get('to')
	to = [int(x) for x in json.loads(tostr)]
	print to

	dest = addr.get_nums_with_ids(to)
	print dest
	howmany = len(dest)
	client.send(dest, msg)
	return jsonify(result="sent {} to {} numbers(s)".format(msg, howmany))

@app.route('/_get_people_in_groups')
@login_required
def get_people_in_groups():
	addr = LibAddrBook()
	groupliststr = request.args.get('grouplist')
	grouplist = [int(x) for x in json.loads(groupliststr)]
	ppl = addr.get_people_in_groups(grouplist)
	return jsonify(result=ppl)

@app.route('/_get_people')
@login_required
def get_people():
	addr = LibAddrBook()
	people = addr.get_everyone()
	return jsonify(people=people)

@app.route('/_get_groups')
@login_required
def get_groups():
	addr = LibAddrBook()
	groups = addr.get_groups()
	return jsonify(groups=groups)

@app.route('/')
@login_required
def index():
	return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated() and current_user.is_active():
		return redirect(url_for('index'))

	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		if(username and password):
			# do login because username and password have been specified
			uid = user.authenticate(username, password)
			if uid != None:
				login_user(user.get(uid))
				return redirect(url_for('index'))
	return render_template('login.html')

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))
	
@login_manager.user_loader
def load_user(userid):
	return user.get(userid)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=42069, debug=True)
	#app.run(host='10.9.8.1', port=42069, debug=True)
