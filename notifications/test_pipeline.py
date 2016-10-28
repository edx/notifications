"""
Unit tests for the notifications pipeline.
"""

from datetime import datetime, timedelta
import unittest
from uuid import UUID

from mock import patch
import pytz

from .message import NotificationsMessage, PipelineHistory
from .pipeline_manager import Pipeline


class TestPipeline(unittest.TestCase):
    """
    Implements the unit tests for the notifications pipeline.
    """

    @patch('notifications.pipeline_manager.logging')
    def test_complete_pipeline(self, mock_logging):
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
        # Check logging
        self.assertEqual(len(mock_logging.info.call_args_list), 9)  # Successful delivery means 9 calls to logging info
        self.assertEqual(len(mock_logging.warning.call_args_list), 0)

    @patch('notifications.pipeline_manager.logging')
    def test_expiry(self, mock_logging):
        message = NotificationsMessage(
            name="edx.notifications.forums.post.created",
            expiration_time=pytz.utc.localize(datetime.utcnow()) - timedelta(minutes=5)
        )
        pipeline = Pipeline()
        # self.assertRaises(ValueError, pipeline.process, message)
        pipeline.process(message)
        # Check the vars of the message
        self.assertIsInstance(message.uuid, UUID)
        self.assertEqual(len(message.history), 0)  # Dropped before queued to pipeline
        history_list = message.history
        for i in history_list:
            self.assertIsInstance(i, PipelineHistory)
            self.assertIsInstance(i.timestamp, datetime)
        # Check logging
        self.assertEqual(len(mock_logging.info.call_args_list), 0)  # Not received by pipeline steps
        self.assertEqual(len(mock_logging.warning.call_args_list), 1)  # Dropped message


if __name__ == '__main__':
    unittest.main()
