"""
Unit tests for the notifications pipeline.
"""

from datetime import datetime
import unittest
from uuid import UUID

from .message import NotificationsMessage, PipelineHistory
from .pipeline_manager import Pipeline


class TestPipeline(unittest.TestCase):
    """
    Implements the unit tests for the notifications pipeline.
    """

    def test_composer(self):
        message = NotificationsMessage("edx.notifications.forums.post.created")
        self.assertIsInstance(message.uuid, UUID)

    def test_complete_pipeline(self):
        message = NotificationsMessage("edx.notifications.forums.post.created")
        pipeline = Pipeline()
        pipeline.process(message)
        # Check the vars of the message
        self.assertIsInstance(message.uuid, UUID)
        self.assertEqual(len(message.history), (len(pipeline.pipeline_step_list)-1)*2)
        history_list = message.history
        for i in history_list:
            self.assertIsInstance(i, PipelineHistory)
            self.assertIsInstance(i.timestamp, datetime)
if __name__ == '__main__':
    unittest.main()
