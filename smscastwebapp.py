from flask import Flask, jsonify, render_template, request, json
from mocksmscast import LibSMSCast
from libaddrbook import LibAddrBook
app = Flask(__name__)

@app.route('/send')
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
def get_people_in_groups():
	addr = LibAddrBook()
	groupliststr = request.args.get('grouplist')
	grouplist = [int(x) for x in json.loads(groupliststr)]
	ppl = addr.get_people_in_groups(grouplist)
	return jsonify(result=ppl)

@app.route('/_get_people')
def get_people():
	addr = LibAddrBook()
	people = addr.get_everyone()
	return jsonify(people=people)

@app.route('/_get_groups')
def get_groups():
	addr = LibAddrBook()
	groups = addr.get_groups()
	return jsonify(groups=groups)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=42069, debug=True)
	#app.run(host='10.9.8.1', port=42069, debug=True)
