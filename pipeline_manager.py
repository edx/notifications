""" Manages logic for moving the message through the pipeline. """
import importlib, logging
from datetime import datetime
from message import PipelineHistory, NotificationsMessage
# Imports for all the pipeline steps
from pipeline_steps.user_targeting import PipelineUserTargeting
from pipeline_steps.user_policy import PipelineUserPolicy
from pipeline_steps.presentation import PipelinePresentation
from pipeline_steps.delivery import PipelineDelivery

def import_from_string(class_name):
    # TODO: Remove during refactoring
    class_lookup = {
    "PipelineUserTargeting": "pipeline_steps.user_targeting",
    "PipelineUserPolicy": "pipeline_steps.user_policy",
    "PipelinePresentation": "pipeline_steps.presentation",
    "PipelineDelivery": "pipeline_steps.delivery"}
    module_name = class_lookup[class_name]
    return getattr(importlib.import_module(module_name), class_name)

class Pipeline(object):
    def __init__(self):
        self.pipeline_step_list = [
        "PipelineComposer",
        "PipelineUserTargeting",
        "PipelineUserPolicy",
        "PipelinePresentation",
        "PipelineDelivery"
        ]
    def pipeline_process(self, message):
        pipeline_step_pointer = self.pipeline_step_list.index(message.current_step)
        pipeline_step_pointer += 1
        message.current_step = self.pipeline_step_list[pipeline_step_pointer] # Update the current step
        message.history.append(PipelineHistory(message.current_step, 'Started'))
        import_from_string(self.pipeline_step_list[pipeline_step_pointer]).process_message(message)
        message.history.append(PipelineHistory(message.current_step, 'Completed'))
        if message.current_step == self.pipeline_step_list[-1]:
            logging.warning(message.name + " " + str(message.id) + " has been delivered.")
        else:
            self.pipeline_process(message)
