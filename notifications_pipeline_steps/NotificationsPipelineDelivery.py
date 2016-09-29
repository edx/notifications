from datetime import datetime
import NotificationsPipelineStep
class NotificationsPipelineDelivery(NotificationsPipelineStep.NotificationsPipelineStep):
    @staticmethod
    def process_message(message):
        print message.current_step + " has received " + message.name + " " + str(message.id)
        if datetime.utcnow() > message.expiration_time:
            print message.name + " " + str(message.id) + " has expired. It will be dropped."
        else:
            log_file = open("logs/"+str(message.id)+".txt","w")
            log_file.write(str(vars(message)))
            log_file.close()
