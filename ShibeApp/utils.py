from twilio.rest import Client

def send_sms(to, message):

    # Twilio credentials (replace these with your actual values)
    account_sid = 'AC13018433dc694daaeed4707e6b99c0d2'  # Replace with your Twilio Account SID
    auth_token = 'fc01a85ffb17679e96e7a4ac67b63117'    # Replace with your Twilio Auth Token
    twilio_number = '+12164806401'  # Replace with your Twilio phone number

    # Initialize the Twilio client
    client = Client(account_sid, auth_token)

    # Send the SMS message
    client.messages.create(
        body=message,     # The text of the message
        from_='+12164806401',  # Your Twilio phone number
        to='+255745989250'            # Recipient's phone number
    )
