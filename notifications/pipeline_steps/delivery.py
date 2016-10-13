"""
Implements the delivery step of the notifications pipeline.
"""

import logging

from .base import PipelineStep


class PipelineDelivery(PipelineStep):
    """Deliver the NotificationsMessage to the appropriate delivery channels."""

    @staticmethod
    def process_message(message):
        """
        Deliver the message to a log file if it has not expired.

        Args:
            message: NotificationsMessage object received from the previous step in the pipeline.
        """
        super(PipelineDelivery, PipelineDelivery).process_message(message)
        logging.info(str(vars(message)))
