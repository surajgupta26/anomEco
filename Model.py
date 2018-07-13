import json
import os.path
import datetime
from alert import Alert
from luminol.anomaly_detector import AnomalyDetector
import numpy as np
import cPickle
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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
                    return True,anomalies
        except:
            return False,[]
        return False,anomalies

    def run(self, data, location):
        keys=data.keys()
        alert=Alert(datestring=str(datetime.datetime.now()),location=location)
        xpoints={}
        ypoints={}
        for k in keys:
            is_anomaly,anomalies=self.isAnomaly(data[k])
            if is_anomaly:
                alert.addField(k,'Something is wrong. Value: '+str(data[k]))
                print 'Anomaly detected: Location =',location,'Field =',k
                xpoints[k]=[anomaly.exact_timestamp for anomaly in anomalies]
                ypoints[k]=[data[k][i] for i in xpoints[k]]
        self.plotAnomalies(keys,data,location,xpoints=xpoints,ypoints=ypoints)
        return alert

    def runOnLocation(self, location):
        filename='data/'+location+'.p'
        data=readObject(filename)
        return self.run(data, location)

    def plotAnomalies(self,keys,data,city='Tulsa',xpoints=None,ypoints=None):  # /plot/<location>_<feature>.png
        n = 0
        d = data
        if not os.path.exists('plot'):
                os.makedirs('plot')
        # print x
        for k in keys:
            n += 1
            plt.figure(n)
            plt.ylabel(k)
            plt.xlabel('time')

            if k not in xpoints:
                xpoints[k]=[]
                ypoints[k]=[]

            # if xpoints is None and ypoints is None: #Anomalies not given (detect using lumninol)
            #     xpoints,ypoints = {} ,{}
            # if k not in xpoints.keys() or k not in ypoints.keys():
            #     xpoints[k],ypoints[k] = [],[]
            #     tmp =
            #     xpoints[k].append(tmp[0])
            #     ypoints[k].append(tmp[1])

            # print n,len(xpoints),d.keys()
            plt.plot(d[k])
            plt.plot(xpoints[k],ypoints[k],'ro')
            plt.savefig('plot/'+city+'_'+k+'.png')



