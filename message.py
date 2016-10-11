from datetime import datetime, timedelta
import pytz, uuid

class PipelineHistory(object):
    def __init__(self, step, event):
        self.step = step
        self.event = event
        self.timestamp = pytz.utc.localize(datetime.utcnow())

    def __repr__(self):
        return '<%s %s: %s>' %(self.step, self.event, self.timestamp)

class NotificationsMessage(object):

    def __init__ (self, name, fields=None, recipients=None):
        self.fields = fields
        self.recipients = recipients
        self.name = name
        self.id = uuid.uuid4()
        self.expiration_time = pytz.utc.localize(datetime.utcnow()) + timedelta(minutes = 5) # Message expires five minutes after the current time
        self.history = [] # list of PipelineHistory
        self.current_step = "PipelineComposer" # Indicates the current step in the pipeline
