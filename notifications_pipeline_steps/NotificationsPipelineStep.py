from datetime import datetime
import pytz, logging

class NotificationsPipelineStep(object):
    @staticmethod
    def process_message(notifications_message):
        logging.warning(notifications_message.current_step + " has received " + notifications_message.name + " " + str(notifications_message.id))
        if pytz.utc.localize(datetime.utcnow()) > notifications_message.expiration_time:
            logging.warning(notifications_message.name + " " + str(notifications_message.id) + " has expired. It will be dropped." )# Dropping unimplemented
        else:
            logging.warning(notifications_message.name + " " + str(notifications_message.id) + " has not expired. It will be forwarded.")
