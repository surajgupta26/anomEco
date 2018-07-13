from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
file1 = open("features.txt",'r')
feature_names = file1.read()
feature_names = feature_names.split("\n")

def createPlot(current_feature_name, location_name):
    file_name = location_name + "_" + current_feature_name + ".png"
    return file_name


@app.route('/plot/<location_name>')
def build_plot(location_name):
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "net_bookings"

    file_name = createPlot(current_feature_name, location_name)

    return render_template('plot.html',  feature_names=feature_names,  
        current_feature_name=current_feature_name, location_name = location_name, 
        file_name = file_name)

if __name__ == '__main__':
    app.debug = True
    app.run(port=2500)