from datetime import datetime, timedelta
import uuid

class NotificationsPipelineHistory(object): # Pipeline History Object
    def __init__(self):
        self.enter_timestamp = None
        self.exit_timestamp = None
    def onEnter(self):
        """
        Update timestamp for enter.
        """
        self.enter_timestamp = datetime.utcnow()
    def onExit(self):
        """
        Update timestamp for exit.
        """
        self.exit_timestamp = datetime.utcnow()

'''
class NotificationsRecipientsBase(object):
    pass

class NotificationsRecipientsList(NotificationsRecipientsBase):
    def __init__(self):
        self.user_list = []

class NotificationsRecipients(NotificationsRecipientsBase):
    def __init__(self, resolver_id):
        self.user_query = {}
        self.resolver_id = resolver_id # unique id for the user-targeting resolver


class NotificationsPresentationData(object):
    pass

class NotificationsDeliveryData(object):
    pass
'''
class NotificationsMessage(object):

    def __init__ (self, name="edx.notifications.forums.post.created", fields=None, recipients=None):
        self.fields = fields
        self.recipients = recipients
        self.name = name
        self.id = uuid.uuid4()
        self.expiration_time = datetime.utcnow() + timedelta(minutes = 5) # Message expires five minutes after the current time
        self.history = [] # list of NotificationsPipelineHistory
        self.current_step = "NotificationsPipelineComposer" # Indicates the current step in the pipeline

''' TODO: Replace with Smarter Objects '''
