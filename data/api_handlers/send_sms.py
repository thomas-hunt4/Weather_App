# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv
from features.alerts import SMS_Alerts

load_dotenv()
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)
TWILIO_TOLLFREE = os.getenv("TWILIO_TOLLFREE")



def twilio_sms(alert):
    body = alert
    message = client.messages.create(
        body=body,
        from_=f"+{TWILIO_TOLLFREE}",
        to="+15415958129",
    )

    print(message.body)



