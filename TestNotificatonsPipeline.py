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
        self.assertIsInstance(message.id, uuid.UUID)

    def test_complete_pipeline(self):
        message = nm.NotificationsMessage()
        np_object = np.NotificationsPipeline()
        np_object.on_enter(message)
        # Check the vars of the message.
        self.assertIsInstance(message.id, uuid.UUID)
        self.assertEqual( len(message.history), (len(np_object.pipeline_step_list)-1)*2 )
        history_list = message.history
        for i in history_list:
            self.assertIsInstance(i,nm.NotificationsPipelineHistory)
            self.assertEqual(type(i.timestamp), type(pytz.utc.localize(datetime.utcnow())) )
            # self.assertEqual(message.current_step,np_object.pipeline_step_list[-1]) # Testing if there are two instance for each pipeline step
if __name__ == '__main__':
    unittest.main()
