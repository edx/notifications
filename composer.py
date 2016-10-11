""" Mimics composer. Composes and enqueues the message onto the pipeline."""
from message import NotificationsMessage
from pipeline_manager import Pipeline

# TODO: Modify to add __main__ method here later
message = NotificationsMessage("edx.notifications.forums.post.created")
np_object = Pipeline()
np_object.pipeline_process(message)
