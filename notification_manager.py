from twilio.rest import Client
import os


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(os.environ['TW_ACCOUNT_SID'], os.environ['TW_AUTH_TOKEN'])

    def send_sms(self, message_body):
        message = self.client.messages.create(
            from_=os.environ['TWILIO_NUMBER'],
            body=message_body,
            to=os.environ['MY_NUMBER']
        )
        # Prints if successfully sent.
        print(message.sid)
