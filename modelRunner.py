from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import json
import pickle
from alertSystem import AlertSystem
import json
from Model import Model

app = Flask(__name__)
als=AlertSystem()
als.startServer()
model = Model()

def getLocations():
	with open('locations.json','r') as f:
		d=json.load(f)['body']['result']
		return [loc['name'] for loc in d]

locations=getLocations()

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
		return render_template('index.html', locations = locations)

	if request.method == 'POST':
		print request.form
		location = request.form['sel1']
		print location
		return redirect(url_for('updateSubs', location_name = location))


@app.route("/alerts/<location_name>", methods =['GET','POST'])
def updateSubs(location_name):
	if request.method == 'GET':
		return render_template('location.html', location_name = location_name, emails = als.getRecipients(location_name))

	if request.method == 'POST':
		email = request.form['usremail']
		print 'Hello'
		print request.form['submit']
		if request.form['submit']=='Add':
			als.addRecipient(location_name,email)
		elif request.form['submit']=='Remove':
			als.removeRecipient(location_name,email)
		return redirect(url_for('updateSubs', location_name = location_name))


@app.route("/addData/<location_name>", methods = ['GET','POST'])
def addData(location_name):
	if request.method == 'POST':
		data = request.json
		model.addData(location_name, data)
		alerts=model.runOnLocation(location_name)
		als.sendAlert(alert)

@app.route("/runModel/<location_name>", methods = ['POST'])
def runModel(location_name):
	if request.method == 'POST':
		data = request.json
		model.runOnLocation(location_name)

if __name__ == "__main__":
	app.run(debug=True)