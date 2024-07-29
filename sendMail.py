import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()
sendGridKey = os.getenv('SENDGRID_APIKEY')

def mail(messages):
    """
    """
    message = Mail(
        from_email='gwunonfwsnotifier@gmail.com',
        to_emails=['bhoomika.nanjaraja@gwu.edu','krswathi2012@gmail.com','vaibhav25vemula23@gmail.com','sreevaishnavirao.bommena@gwmail.gwu.edu','manoj.srinivasa@gwu.edu','murudeshwar.2021@gmail.com'],
        subject='Test Subject',
        html_content="#####".join(map(str, messages))
    )


    try:
        sg = SendGridAPIClient(sendGridKey)
        response = sg.send(message)
        print(f"Status code: {response.status_code}")
        print(response.body)
        print(response.headers)
        if(response.status_code == '202'):
            return("Successfully sent the messages")
        else:
            return("Didn't send the messages")
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
    except Exception as e:
        print(f"Error: {str(e)}")
