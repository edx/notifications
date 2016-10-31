"""
Base class for all the pipeline steps.
"""

import logging


class PipelineStep(object):
    """
    Implement base functionality which all the pipeline steps inherit.
    """

    @staticmethod
    def process_message(message):
        """
        Base functionality used by all pipeline steps.

        Args:
            message: NotificationsMessage object received from the previous step in the pipeline.
        """
        logging.info("%s has received %s %s", message.current_step, message.name, message.uuid)
