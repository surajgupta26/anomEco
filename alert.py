from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Alert:

    def __init__(self, datestring, location, fields=[], field_notifications=[]):
        self.datestring=datestring
        self.location=location
        self.fields=fields
        self.field_notifications=field_notifications

    def addField(self, field, field_notification):
        self.fields.append(field)
        self.field_notifications.append(field_notification)

    def getMessage(self):
        print 'Inside'
        message=MIMEMultipart()
        message['Subject']='Anomlies in '+self.location+" on "+self.datestring
        body='Location: '+self.location+'\nDate: '+self.datestring+'\nList of anomalies:\n'
        for i in range(self.getAnomalyCount()):
            body+='\t'+self.fields[i]+': '+self.field_notifications[i]+'\n'
        message.attach(MIMEText(body, 'plain'))
        return message

    def getAnomalyCount(self):
        return len(self.fields)
