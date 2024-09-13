import os
import mimetypes
import smtplib
import aiosmtplib

from email.message import EmailMessage

from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os.path import basename

from settings import config_parameters


async def send_email(subject: str, recipient: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = config_parameters.EMAIL_SENDER
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        a = await aiosmtplib.send(
            msg,
            hostname=config_parameters.SMTP_HOSTNAME,
            port=config_parameters.SMTP_PORT,
            username=config_parameters.SMTP_USERNAME,
            password=config_parameters.SMTP_PASSWORD,
            use_tls=False,
            start_tls=True
        )
        print(a)

        return True

    except Exception as e:
        print(f"Failed to send email: {e}")

        return False


async def send_email_with_file(subject: str, recipient: str, body: str,
                                file: str):
    mime_type, _ = mimetypes.guess_type(file)
    mime_type, mime_subtype = mime_type.split('/')

    with open(file, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    message = EmailMessage()
    message['From'] = config_parameters.EMAIL_SENDER
    message['To'] = recipient
    message['Subject'] = subject

    message.add_attachment(file_data, maintype=mime_type, subtype=mime_subtype,
                            filename=os.path.basename(file_name))
    message.attach(MIMEText(body, 'html'))

    await aiosmtplib.send(
        message,
        hostname=config_parameters.SMTP_HOSTNAME,
        port=config_parameters.SMTP_PORT,
        username=config_parameters.SMTP_USERNAME,
        password=config_parameters.SMTP_PASSWORD,
        start_tls=True,
    )