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

    def __init__(self, username='anomEco2018@gmail.com', password='anomEco@123'):
        self.username='anomEco2018@gmail.com'
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
            self.remove(recipient_email)
            saveObject('location_to_emails.p',location_to_emails)

    def getMessage(self, alert):
        message=alert.getMessage()
        message['From']=self.username
        message['To']=','.join(list(self.location_to_emails[alert.location]))
        return message

    def sendAlert(self, alert):
        message=self.getMessage(alert)
        if len(message['To'])==0:
            return
        self.server.sendmail(self.username, message['To'], message.as_string())

if __name__=='__main__':
    als=AlertSystem()
    als.addRecipient(location='Hyderabad',recipient_email=als.username)
    als.startServer()
    alert=Alert(datestring='10/06/2018',location='Hyderabad',fields=['fares'],field_notifications=['Total fares is going down!'])
    als.sendAlert(alert)
    als.stopServer()
