"""
Implements the NotificationsMessage object and smart objects contained within it.
"""

from datetime import datetime, timedelta
import uuid

import pytz


class PipelineHistory(object):
    """
    Timestamp used to track the time spent in each step of the pipeline.
    """

    def __init__(self, step, event):
        """
        Initialize the smart PipelineHistory object.

        Args:
            step (str): Current step in the pipeline.
            event (str): "Started" or "Completed" based on the event associated with step.

        Attributes:
            timestamp: Machine localized timestamp.
        """
        self.step = step
        self.event = event
        self.timestamp = pytz.utc.localize(datetime.utcnow())

    def __repr__(self):
        """
        Create a human-readable representation of the object.
        """
        return '<%s %s: %s>' % (self.step, self.event, self.timestamp)


class NotificationsMessage(object):
    """
    Initialize the NotificationsMessage object containing various attributes required by steps in the pipeline.
    """

    def __init__(self, name, fields=None, recipients=None, expiration_time = pytz.utc.localize(datetime.utcnow()) + timedelta(minutes=5)):
        """
        Initialize the NotificationsMessage object with the object name.

        Args:
            name (str): Namespaced string corresponding to the type of notifications message.
            fields (optional): Fields that may be optionally required by steps in the pipeline.
            recipients (optional list): List of recipients that can be specified on creation.

        Attributes:
            uuid (UUID): Universally unique identified for the message.
            expiration_time (datetime): Time of expiry of message.
            history (list): List of PipelineHistory objects.
            current_step: Indicates the current step in the pipeline.
        """
        self.fields = fields
        self.recipients = recipients
        self.name = name
        self.uuid = uuid.uuid4()
        self.expiration_time = expiration_time
        self.history = []
        self.current_step = "PipelineComposer"
