import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import cPickle
import os.path
from alert import Alert

def saveObject(filename, obj):
    f=open(filename,'w')
    cPickle.dump(obj,f)
    f.close()

class AlertSystem:

    def __init__(self, username='anomeco0@gmail.com', password='anomEco@123'):
        self.username=username
        self.password='anomEco@123'
        self.loadLocationToEmails()

    def startServer(self):
        self.server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        self.server.starttls()
        self.server.login(self.username, self.password)

    def stopServer(self):
        self.server.quit()

    def loadLocationToEmails(self, path='location_to_emails.p'):
        if os.path.exists(path):
            f=open(path,'r')
            self.location_to_emails=cPickle.load(f)
            f.close()
        else:
            self.location_to_emails={}

    def addRecipient(self, location, recipient_email):
        if location not in self.location_to_emails:
            self.location_to_emails[location]=set()
        self.location_to_emails[location].add(recipient_email)
        saveObject('location_to_emails.p',self.location_to_emails)

    def removeRecipient(self, location, recipient_email):
        if recipient_email in self.location_to_emails[location]:
            self.location_to_emails[location].remove(recipient_email)
            saveObject('location_to_emails.p',self.location_to_emails)

    def getRecipients(self, location):
        return self.location_to_emails.get(location,[])

    def getMessage(self, alert):
        message=alert.getMessage()
        message['From']=self.username
        return message

    def sendAlert(self, alert):
        if alert.getAnomalyCount()==0:
            return
        message=self.getMessage(alert)
        for recipient in list(self.getRecipients(alert.location)):
            message['To']=recipient
            print 'Sending email to ',message['To']
            self.server.sendmail(self.username, recipient, message.as_string())

    def sendAlerts(self, alerts):
        for alert in alerts:
            sendAlert(alert)

if __name__=='__main__':
    als=AlertSystem()
    als.addRecipient(location='Hyderabad',recipient_email=als.username)
    als.startServer()
    alert=Alert(datestring='10/06/2018',location='Hyderabad',fields=['fares'],field_notifications=['Total fares is going down!'])
    als.sendAlert(alert)
    als.stopServer()
