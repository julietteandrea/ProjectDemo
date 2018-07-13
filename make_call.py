# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os


# Your Account Sid and Auth Token from twilio.com/console
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

call = client.calls.create(record=True,
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+13474568702',
                        from_='+16692717646'
                    )

print(call.sid)