import json
import os.path
import datetime
from alert import Alert

def saveObject(filename, obj):
    f=open(filename,'w')
    cPickle.dump(obj,f)
    f.close()

def readObject(filename):
    f=open(filename,'r')
    obj=cPickle.load(f)
    return obj

class Model:

    def __init__(self):
        if not os.path.exists('data'):
            os.makedirs('data')

    def addData(self, location, data):
        keys=data.keys()
        filename='data/'+location+'.p'
        if not os.path.exists(filename):
            for k in keys:
                data[k]=[data[k]]
            saveObject(filename,data)
        else:
            existing_data=readObject(filename)
            for k in keys:
                existing_data[k].append(data[k])
            saveObject(filename,existing_data)

    def isAnomaly(self, data):                  # returns if last data point is anonaly
        return False

    def run(self, data, location):
        keys=data.keys()
        alert=Alert(datestring=str(datetime.datetime.now()),location=location)
        for k in keys:
            if self.isAnomaly(data[k]):
                alert.addField(k,'Something is wrong. Value: '+str(data[k]))
        return alert

    def runOnLocation(self, location):
        filename='data/'+location+'.p'
        data=readObject(filename)
        return self.run(data)



