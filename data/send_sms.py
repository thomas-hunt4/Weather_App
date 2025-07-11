# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv
# from features.alerts import SMS_Alerts

load_dotenv()
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)
TWILIO_TOLLFREE = os.getenv("TWILIO_TOLLFREE")


""" Twilio testing and setup """
# message = client.messages.create(
#     body="Do you even lift, Bro?!",
#     from_= f"+{TWILIO_TOLLFREE}",
#     to="+15415958129",
# )

# print(message.body)



def twilio_sms(alert):
    body= (f"{alert['type']} in {alert['location']}, {alert['country']}!\n"
        f"{alert['instruction']}")
    
    message = client.messages.create(
        body=body,
        from_=f"+{TWILIO_TOLLFREE}",
        to="+15415958129",
    )

    print(message.body)



