
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()


def send_mail(to_email, message, subject):
    message = Mail(
        from_email='17debo01@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=message)
    # html_content='<strong>and easy to do anywhere, even with Python</strong>')

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        # print(response.status_code)
        print(response)
        # print(response.headers)
    except Exception as e:
        print(e)
