from django.conf import settings
from twilio.rest import Client
import random

class MessageHandler:
    phone_number = None
    otp = None
    def __init__(self,phone_number,otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp(self):
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(body=f'Your otp is {self.otp}',to=self.phone_number, from_=settings.TWILIO_NUMBER)
            return True
        except Exception as e:
            print(e)
            return False