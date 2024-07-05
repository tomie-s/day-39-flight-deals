from twilio.rest import Client
from smtplib import SMTP
import os


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.twilio_client = Client(os.environ['TW_ACCOUNT_SID'], os.environ['TW_AUTH_TOKEN'])
        self.smtp_connection = SMTP('smtp.gmail.com', port=587)

    def send_sms(self, message_body):
        message = self.twilio_client.messages.create(
            from_=os.environ['TWILIO_NUMBER'],
            body=message_body,
            to=os.environ['MY_NUMBER']
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_emails(self, email_list, message):
        with self.smtp_connection:
            self.smtp_connection.starttls()
            self.smtp_connection.login(user=os.environ['SMTP_EMAIL'], password=os.environ['SMTP_PASSWORD'])

            for email in email_list:
                self.smtp_connection.sendmail(
                    from_addr=os.environ['SMTP_EMAIL'],
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}"
                )
