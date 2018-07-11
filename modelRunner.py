from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import json
import pickle


app = Flask(__name__)

@app.route("/")
def hello():
	return "Welcome to anomEco"

@app.route("/newData", methods=['GET','POST'])
def newData():
	content = requests.json
	with open('data.json', 'w') as outfile:
		json.dump(content, outfile)


@app.route("/alerts", methods =['GET','POST'])
def alertLocation():
	if request.method == 'GET':
		return render_template('index.html')

	if request.method == 'POST':
		location = request.form['sel1']
		print location
		return redirect(url_for('updateSubs', location_name = location))


@app.route("/alerts/<location_name>", methods =['GET','POST'])
def updateSubs(location_name):
	if request.method == 'GET':
		pickle_in = open("/subs/"+location_name+".pickle","rb")
		example_dict = pickle.load(pickle_in)
		return render_template('location.html', location_name = location_name, subscribers = example_dict['subs'])

	if request.method == 'POST':
		subscribers = request.form['subs']
		example_dict = {'subs': subscribers}
		pickle_out = open("/subs/"+location_name+".pickle","wb")
		pickle.dump(example_dict, pickle_out)
		pickle_out.close()


if __name__ == "__main__":
	app.run(debug=True)