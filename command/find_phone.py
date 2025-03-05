from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

client = Client(account_sid, auth_token)

def make_call():

    from_phone_number = "+12406604160"  
    to_phone_number = "+84914620279"   

    call = client.calls.create(
        to=to_phone_number,
        from_=from_phone_number,
        url="http://demo.twilio.com/docs/voice.xml" 
    )

    print(f"Cuộc gọi đang được thực hiện. SID: {call.sid}")
    return call.sid
