"""
Base class for all the pipeline steps.
"""

from datetime import datetime
import logging

import pytz


class PipelineStep(object):
    """
    Implement base functionality which all the pipeline steps inherit.
    """

    @staticmethod
    def process_message(message):
        """
        Drop the message if it has expired.

        Args:
            message: NotificationsMessage object received from the previous step in the pipeline.
        """
        logging.info("%s has received %s %s", message.current_step, message.name, message.uuid)
        if pytz.utc.localize(datetime.utcnow()) > message.expiration_time:
            logging.warning("%s %s has expired. It will be dropped.", message.name, message.uuid)
        else:
            logging.info("%s %s has not expired. It will be forwarded.", message.name, message.uuid)
