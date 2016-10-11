from datetime import datetime
import pytz, logging
from base import PipelineStep
class PipelineDelivery(PipelineStep):
    @staticmethod
    def process_message(message):
        logging.warning(message.current_step + " has received " + message.name + " " + str(message.id))
        if pytz.utc.localize(datetime.utcnow()) > message.expiration_time:
            logging.warning(message.name + " " + str(message.id) + " has expired. It will be dropped.")
        else:
            logging.info(str(vars(message)))
