''' Mimics composer. Composes and enqueues the message onto the pipeline.'''
import NotificationsMessage as nm
import NotificationsPipeline as np

# Modify to add __main__ method here later
message = nm.NotificationsMessage() # Create NotificationsMessage object
# Call NotificationsPipeline with NotificationsMessage object as input
np.NotificationsPipeline.on_enter(message)
