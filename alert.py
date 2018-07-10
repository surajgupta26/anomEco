import smtplib
# set up the SMTP server

class AlertSystem:

    def __init__(self, username='anomEco2018@gmail.com', password='anomEco@123'):
        self.username='anomEco2018@gmail.com'
        self.password='anomEco@123'

    def startServer(self):
        self.server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        self.server.starttls()
        self.server.login(self.username, self.password)

    def stopServer(self):
        self.server.quit()

    def sendAlert(self, to, msg, _from=None):
        if _from is None:
            _from = self.username
        self.server.sendmail(_from, to, msg)

if __name__=='__main__':
    als=AlertSystem()
    als.startServer()
    als.sendAlert(to=als.username,msg="This is Test!")
    als.stopServer()
