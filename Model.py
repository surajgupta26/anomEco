import json
import os.path
import datetime
from alert import Alert
from luminol.anomaly_detector import AnomalyDetector
import numpy as np
import cPickle

def saveObject(filename, obj):
    f=open(filename,'w')
    cPickle.dump(obj,f)
    f.close()

def readObject(filename):
    f=open(filename,'r')
    obj=cPickle.load(f)
    return obj

class Model:

    def __init__(self, score_threshold=1.0):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists('newdata'):
            os.makedirs('newdata')
        self.score_threshold=score_threshold

    def addData(self, location, data=None):
        if data is None:
            f=open('newdata/'+location,'r')
            data=json.load(f)
            f.close()
        data=data['body']
        if type(data)==list:
            data=data[0]
        data=data['result']['metrics']
        if type(data)==list:
            data=data[0]
        data=data['lineItems']
        keys=data.keys()
        filename='data/'+location+'.p'
        for k in data.keys():
            data[k]=data[k]['value']
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
        length=len(data)
        try:
            detector=AnomalyDetector({i:data[i] for i in range(length)}, score_threshold=self.score_threshold)
            anomalies=detector.get_anomalies()
            for anomaly in anomalies:
                if anomaly.exact_timestamp==length-1:
                    return True
        except:
            return False
        return False

    def run(self, data, location):
        keys=data.keys()
        alert=Alert(datestring=str(datetime.datetime.now()),location=location)
        for k in keys:
            if self.isAnomaly(data[k]):
                alert.addField(k,'Something is wrong. Value: '+str(data[k]))
                print 'Anomaly detected: Location =',location,'Field =',k
        return alert

    def runOnLocation(self, location):
        filename='data/'+location+'.p'
        data=readObject(filename)
        return self.run(data, location)



