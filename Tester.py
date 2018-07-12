from Model import Model
import threading
import os
from copy import deepcopy
from datetime import date,timedelta
import json
import requests

class RunThread(threading.Thread):

    def __init__(self, location, date):
        threading.Thread.__init__(self)
        self.location=location
        self.date=date
        self.location_id=self.getLocationId(location)

    def readYabTemplate(self, filename='yab_data_template.json'):
        with open(filename,'r') as f:
            d=json.load(f)
            return d

    def getLocationId(self, location, filename='locations.json'):
        with open(filename, 'r') as f:
            d=json.load(f)['body']['result']
            for loc in d:
                if loc['name']==location:
                    return str(int(loc['id'])+1000)
            return None

    def getYabCommand(self):
        yab_template=self.readYabTemplate()
        startDate=yab_template['tripEconomicsRequest']['startDate']
        endDate=yab_template['tripEconomicsRequest']['endDate']
        startDate['day']=date.day
        startDate['month']=date.month
        startDate['year']=date.year
        edate=date+timedelta(days=1)
        endDate['day']=edate.day
        endDate['month']=edate.month
        endDate['year']=edate.year
        yab_template['tripEconomicsRequest']['locationIdentifiers'].append(self.location_id)
        yab_template['tripEconomicsRequest']['aggType']='DAILY'
        null_keys=['linesOfBusiness','products','currency','uuid','emailID','ledgerLineItems','dashboard','locationVersion']
        for key in null_keys:
            yab_template['tripEconomicsRequest'].pop(key)
        yab_command="yab -s ueconomics -m Ueconomics::getTripEconomics -t /usr/share/uber-idl/code.uber.internal/finance/ueconomics/ueconomics.thrift --caller yab-sohan.desarkar --request '"
        yab_command+=json.dumps(yab_template)
        yab_command+="' --header 'x-uber-uuid:b091e5dc-954b-4603-b224-531522ef19a3' --header 'x-uber-source:studio' --timeout=30000 -p 127.0.0.1:5437"
        pipe_command=' > "newdata/'+self.location+'"'
        return yab_command+pipe_command

    def run(self):
        os.system(self.getYabCommand())
        with open('newdata/'+self.location+,'r') as f:
            data=json.load(f)
            requests.post("http://127.0.0.1:5000/addData/"+location,data=data)

class Tester:

    def __init__(self, model):
        self.model=model

    def getDataForAllLocations(self, locations, date):
        threads=[]
        thread_count_limit=50
        loc_index=0
        while loc_index<len(locations):
            while len(threads)<thread_count_limit and loc_index<len(locations):
                thread=RunThread(locations[loc_index],date)
                threads.append(thread)
                thread.start()
                loc_index+=1
            for thread in threads:
                thread.join()
            threads=[]

def getLocations():
	with open('locations.json','r') as f:
		d=json.load(f)['body']['result']
		return [loc['name'] for loc in d]

tester=Tester(None)
locations=getLocations()
date=date(2018,2,1)
tester.getDataForAllLocations(locations,date)