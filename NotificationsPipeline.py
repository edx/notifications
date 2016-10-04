from datetime import datetime
import pytz
import NotificationsMessage as nm
import importlib
# Imports for all the pipeline steps
from notifications_pipeline_steps.NotificationsPipelineUserTargeting import NotificationsPipelineUserTargeting
from notifications_pipeline_steps.NotificationsPipelineUserPolicy import NotificationsPipelineUserPolicy
from notifications_pipeline_steps.NotificationsPipelinePresentation import NotificationsPipelinePresentation
from notifications_pipeline_steps.NotificationsPipelineDelivery import NotificationsPipelineDelivery

def import_from_string(module_name):
    # Remove during refactoring
    class_name = module_name.split(".")[-1]
    return getattr(importlib.import_module(module_name), class_name)

class NotificationsPipeline(object):
    def __init__(self):
        self.pipeline_step_list = [
        "NotificationsPipelineComposer",
        "notifications_pipeline_steps.NotificationsPipelineUserTargeting",
        "notifications_pipeline_steps.NotificationsPipelineUserPolicy",
        "notifications_pipeline_steps.NotificationsPipelinePresentation",
        "notifications_pipeline_steps.NotificationsPipelineDelivery"
        ]
    def on_enter(self, message):
        # Identify first time
        if message.current_step == self.pipeline_step_list[0]:
            message.history = [nm.NotificationsPipelineHistory() for i in range(len(self.pipeline_step_list) - 1)] # Initialize list of history objects
            message.history[0].onEnter() # Assign the entry timestamp
            message.current_step = self.pipeline_step_list[1] # Update the current step
            import_from_string(message.current_step).process_message(message) # Current step processes the message
            message.history[0].onExit()
            # exit()
            self.on_enter(message)
        # Identify last time
        elif message.current_step == self.pipeline_step_list[-1]:
            print message.name + " " + str(message.id) + " has been delivered."
        else:
            pipeline_step_pointer = self.pipeline_step_list.index(message.current_step)
            message.history[pipeline_step_pointer].onEnter()
            pipeline_step_pointer += 1
            message.current_step = self.pipeline_step_list[pipeline_step_pointer] # Update the current step
            import_from_string(self.pipeline_step_list[pipeline_step_pointer]).process_message(message) # Current step processes the message
            message.history[pipeline_step_pointer-1].onExit()
            self.on_enter(message)
