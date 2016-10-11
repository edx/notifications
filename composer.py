""" Mimics composer. Composes and enqueues the message onto the pipeline."""
from message import NotificationsMessage
from pipeline_manager import Pipeline

# TODO: Modify to add __main__ method here later
message = NotificationsMessage("edx.notifications.forums.post.created") # Create NotificationsMessage object
# Call NotificationsPipeline with NotificationsMessage object as input
np_object = Pipeline()
np_object.pipeline_process(message)
