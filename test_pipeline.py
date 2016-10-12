import unittest, pytz
from message import NotificationsMessage, PipelineHistory
from pipeline_manager import Pipeline
from uuid import UUID
from datetime import datetime

class TestPipeline(unittest.TestCase):

    def test_composer(self):
        message = NotificationsMessage("edx.notifications.forums.post.created")
        self.assertIsInstance(message.id, UUID)

    def test_complete_pipeline(self):
        message = NotificationsMessage("edx.notifications.forums.post.created")
        np_object = Pipeline()
        np_object.pipeline_process(message)
        # Check the vars of the message.
        self.assertIsInstance(message.id, UUID)
        self.assertEqual( len(message.history), (len(np_object.pipeline_step_list)-1)*2 )
        history_list = message.history
        for i in history_list:
            self.assertIsInstance(i,PipelineHistory)
            self.assertEqual(type(i.timestamp), type(pytz.utc.localize(datetime.utcnow())) )
            # self.assertEqual(message.current_step,np_object.pipeline_step_list[-1]) # Testing if there are two instance for each pipeline step
if __name__ == '__main__':
    unittest.main()
