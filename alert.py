import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class AlertSystem:

    def __init__(self, username='anomEco2018@gmail.com', password='anomEco@123'):
        self.username='anomEco2018@gmail.com'
        self.password='anomEco@123'
        self.setDefaultMessage()

    def startServer(self):
        self.server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        self.server.starttls()
        self.server.login(self.username, self.password)

    def stopServer(self):
        self.server.quit()

    def setDefaultMessage(self, subject=None, body=None):
        self.default_message=MIMEMultipart()
        if subject is None:
            subject='Alert'
        self.default_message['Subject']=subject
        if body is None:
            body='Anomaly detected!'
        self.default_message.attach(MIMEText(body, 'plain'))

    def getDefaultMessage(self):
        return self.default_message

    def sendAlert(self, to, message=None, _from=None):
        if _from is None:
            _from = self.username
        if message is None:
            message=self.getDefaultMessage()
            message['From']=_from
            message['To']=to
            text=message.as_string()
        else:
            text=message

        self.server.sendmail(_from, to, text)

if __name__=='__main__':
    als=AlertSystem()
    als.startServer()
    als.sendAlert(to=als.username)
    als.stopServer()
