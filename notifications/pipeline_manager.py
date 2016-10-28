"""
Manages logic for moving the message through the pipeline.
"""

from datetime import datetime
import importlib
import logging

import pytz

from .message import PipelineHistory


def import_from_string(class_name):
    """
    Convert a string of the pipeline step name to a class.

    Args:
        message: NotificationsMessage object received from the previous step in the pipeline.

    Attributes:
        class_lookup: A dictionary containing indexed by class name containing the path to the module.

    """
    class_lookup = {
        "PipelineUserTargeting": "notifications.pipeline_steps.user_targeting",
        "PipelineUserPolicy": "notifications.pipeline_steps.user_policy",
        "PipelinePresentation": "notifications.pipeline_steps.presentation",
        "PipelineDelivery": "notifications.pipeline_steps.delivery"}
    module_name = class_lookup[class_name]
    return getattr(importlib.import_module(module_name), class_name)


class Pipeline(object):
    """
    Handle the transfer and processing of NotificationsMessage by each step of the pipeline in sequence.
    """

    def __init__(self):
        """
        Initialize the attributes.

        Attributes:
            pipeline_step_list (list): List of steps in the pipeline.
        """
        self.pipeline_step_list = [
            "PipelineComposer",
            "PipelineUserTargeting",
            "PipelineUserPolicy",
            "PipelinePresentation",
            "PipelineDelivery"
        ]

    def process(self, message):
        """
        Handle the updating of timestamps, checking for expiry of message,
        processing by current step and forwarding to the subsequent step.

        Args:
            message: NotificationsMessage object received from the previous step in the pipeline.

        Attributes:
            pipeline_step_pointer: Index of list pipeline_step_list pointing to the current step in the pipeline
        """
        pipeline_step_pointer = self.pipeline_step_list.index(message.current_step)
        pipeline_step_pointer += 1
        message.current_step = self.pipeline_step_list[pipeline_step_pointer]  # Update the current step
        if pytz.utc.localize(datetime.utcnow()) > message.expiration_time:
            logging.warning(
                "%s %s has expired before step %s. It will be dropped.",
                message.name, message.uuid, message.current_step
                )
        else:
            logging.info(
                "%s %s has not expired before step %s. It will be forwarded.",
                message.name, message.uuid, message.current_step
                )
            message.history.append(PipelineHistory(message.current_step, 'Started'))
            import_from_string(self.pipeline_step_list[pipeline_step_pointer]).process_message(message)
            if pytz.utc.localize(datetime.utcnow()) > message.expiration_time:
                logging.warning(
                    "%s %s has expired after step %s. It will be dropped.",
                    message.name, message.uuid, message.current_step
                    )
                message.history.append(PipelineHistory(message.current_step, 'Expired'))
            else:
                logging.info(
                    "%s %s has not expired after step %s. It will be forwarded.",
                    message.name, message.uuid, message.current_step
                    )
                message.history.append(PipelineHistory(message.current_step, 'Completed'))
                if message.current_step == self.pipeline_step_list[-1]:
                    logging.info("%s %s has been delivered.", message.name, message.uuid)
                else:
                    self.process(message)
