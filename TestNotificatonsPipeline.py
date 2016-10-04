import unittest
import sys
import os
sys.path.append(os.path.abspath('..'))
import NotificationsMessage as nm
import NotificationsPipeline as np
import uuid
from datetime import datetime
import pytz

class TestNotificationsPipeline(unittest.TestCase):

    def test_composer(self):
        message = nm.NotificationsMessage()
        self.assertEqual(type(message.id),type(uuid.uuid4()))

    def test_complete_pipeline(self):
        message = nm.NotificationsMessage()
        np.NotificationsPipeline.on_enter(message)
        # Check the vars of the message.
        self.assertEqual(type(message.id),type(uuid.uuid4()))
        self.assertEqual(len(message.history),len(np.NotificationsPipeline.pipeline_step_list) - 1)
        history_list = message.history
        for i in history_list:
            self.assertEqual(type(i),type( nm.NotificationsPipelineHistory() ) )
            self.assertEqual(type(i.enter_timestamp),type(pytz.utc.localize(datetime.utcnow())))
            self.assertEqual(type(i.exit_timestamp),type(pytz.utc.localize(datetime.utcnow())))
        self.assertEqual(message.current_step,np.NotificationsPipeline.pipeline_step_list[-1])
if __name__ == '__main__':
    unittest.main()
