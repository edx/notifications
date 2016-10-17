"""
Mimics the composer step. Composes and enqueues the message onto the pipeline.
"""

from .message import NotificationsMessage
from .pipeline_manager import Pipeline


def main():
    """
    Create the NotificationsMessage and send it to the pipeline.
    """
    message = NotificationsMessage("edx.notifications.forums.post.created")
    pipeline = Pipeline()
    pipeline.process(message)

if __name__ == '__main__':
    main()
