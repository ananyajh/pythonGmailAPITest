from main import get_service
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def create_message(to, subject, body, attachment):
    if not attachment:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
    else:
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        message.attach(MIMEText(body))
        for file in attachment:
            with open(file, 'rb') as readfile:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(readfile.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {file}",
            )
            message.attach(part)
    new_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    return new_message


def send_email(to, subject, body, attachment):
    """
    :param to: Receiver email address
    :param message: message body
    :param subject: message subject
    """

    service = get_service()
    email = create_message(to, subject, body, attachment)
    try:
        # call the Gmail API messages list function using query parameters
        results = service.users().messages().send(userId='me', body=email).execute()
        print(results)
    except Exception as error:
        print(f"Error while sending email: {error}")


to = input("Enter receiver email address: ")
subject = input("Enter email subject: ")
body = input("Enter message body: ")
attachment = list(map(str, input("Enter path to attachments(space separated): ").split(' ')))

send_email(to, subject, body, attachment)
