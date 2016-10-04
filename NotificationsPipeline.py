from datetime import datetime
import pytz
import NotificationsMessage as nm
import importlib
# Imports for all the pipeline steps
from notifications_pipeline_steps.NotificationsPipelineUserTargeting import NotificationsPipelineUserTargeting
from notifications_pipeline_steps.NotificationsPipelineUserPolicy import NotificationsPipelineUserPolicy
from notifications_pipeline_steps.NotificationsPipelinePresentation import NotificationsPipelinePresentation
from notifications_pipeline_steps.NotificationsPipelineDelivery import NotificationsPipelineDelivery

class NotificationsPipeline(object):
    pipeline_step_list = [
    "NotificationsPipelineComposer",
        "notifications_pipeline_steps.NotificationsPipelineUserTargeting",
            "notifications_pipeline_steps.NotificationsPipelineUserPolicy",
                "notifications_pipeline_steps.NotificationsPipelinePresentation",
                    "notifications_pipeline_steps.NotificationsPipelineDelivery"
    ]
    def __init__(self):
        pass
    @staticmethod
    def str2Class(module_name, class_name):
        # Remove during refactoring
        return getattr(importlib.import_module(module_name), class_name)
    @staticmethod
    def on_enter(message, pipeline_step_list = pipeline_step_list):
        # Identify first time
        if message.current_step == pipeline_step_list[0]:
            message.history = [nm.NotificationsPipelineHistory() for i in range(len(pipeline_step_list) - 1)] # Initialize list of history objects
            message.history[0].enter_timestamp = pytz.utc.localize(datetime.utcnow()) # Assign the entry timestamp
            message.current_step = pipeline_step_list[1] # Update the current step
            NotificationsPipeline.str2Class(message.current_step,message.current_step.split(".")[-1]).process_message(message) # Current step processes the message
            message.history[0].exit_timestamp = pytz.utc.localize(datetime.utcnow())
            # exit()
            NotificationsPipeline.on_enter(message)
        # Identify last time
        elif message.current_step == pipeline_step_list[-1]:
            print message.name + " " + str(message.id) + " has been delivered."
        else:
            pipeline_step_pointer = pipeline_step_list.index(message.current_step)
            message.history[pipeline_step_pointer].enter_timestamp = pytz.utc.localize(datetime.utcnow())
            pipeline_step_pointer += 1
            message.current_step = pipeline_step_list[pipeline_step_pointer] # Update the current step
            NotificationsPipeline.str2Class(pipeline_step_list[pipeline_step_pointer],pipeline_step_list[pipeline_step_pointer].split(".")[-1]).process_message(message) # Current step processes the message
            message.history[pipeline_step_pointer-1].exit_timestamp = pytz.utc.localize(datetime.utcnow())
            NotificationsPipeline.on_enter(message)
