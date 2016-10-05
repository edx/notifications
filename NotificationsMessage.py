from datetime import datetime, timedelta
import pytz
import uuid

class NotificationsPipelineHistory(object): # Pipeline History Object
    def __init__(self):
        self.enter_timestamp = None
        self.exit_timestamp = None
    def __repr__(self):
        return '<Entry Timestamp: %s, Exit Timestamp: %s>' % (self.enter_timestamp, self.exit_timestamp)
    def onEnter(self):
        """
        Update timestamp for enter.
        """
        self.enter_timestamp = pytz.utc.localize(datetime.utcnow())
    def onExit(self):
        """
        Update timestamp for exit.
        """
        self.exit_timestamp = pytz.utc.localize(datetime.utcnow())

class NotificationsMessage(object):

    def __init__ (self, name="edx.notifications.forums.post.created", fields=None, recipients=None):
        self.fields = fields
        self.recipients = recipients
        self.name = name
        self.id = uuid.uuid4()
        self.expiration_time = pytz.utc.localize(datetime.utcnow()) + timedelta(minutes = 5) # Message expires five minutes after the current time
        self.history = [] # list of NotificationsPipelineHistory
        self.current_step = "NotificationsPipelineComposer" # Indicates the current step in the pipeline
