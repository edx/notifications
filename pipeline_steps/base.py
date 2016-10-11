""" Base class for all the pipeline steps."""
from datetime import datetime
import pytz, logging

class PipelineStep(object):
    @staticmethod
    def process_message(message):
        logging.warning(message.current_step + " has received " + message.name + " " + str(message.id))
        if pytz.utc.localize(datetime.utcnow()) > message.expiration_time:
            logging.warning(message.name + " " + str(message.id) + " has expired. It will be dropped." )# Dropping unimplemented
        else:
            logging.warning(message.name + " " + str(message.id) + " has not expired. It will be forwarded.")
