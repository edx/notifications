from datetime import datetime
import pytz

class NotificationsPipelineStep(object):
    @staticmethod
    def process_message(notifications_message):
        print notifications_message.current_step + " has received " + notifications_message.name + " " + str(notifications_message.id)
        if pytz.utc.localize(datetime.utcnow()) > notifications_message.expiration_time:
            print notifications_message.name + " " + str(notifications_message.id) + " has expired. It will be dropped." # Dropping unimplemented
        else:
            print notifications_message.name + " " + str(notifications_message.id) + " has not expired. It will be forwarded."
''' TODO: Clean up everything according to PEP-8 standards. '''
