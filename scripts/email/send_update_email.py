import argparse
from dotenv import load_dotenv
from email_sender import EmailSender
from git_update_notifier import GitUpdateNotifier
import os
from typing import List
from scripts.email.config.email_recipients import RECIPIENTS, DEBUG_RECIPIENTS

def send_mail(recipients: List[str]):
    # Load environment variables
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not gmail_user or not gmail_password:
        print("Error: Gmail credentials not found in environment variables")
        print("Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables")
        return

    # Initialize services
    email_sender = EmailSender(gmail_user, gmail_password)
    notifier = GitUpdateNotifier(email_sender)
    
    # Send the notification
    notifier.send_update_notification(recipients)


def send_prod_mail():
    recipients = RECIPIENTS
    send_mail(recipients)

def send_debug_mail():
    recipients = DEBUG_RECIPIENTS
    send_mail(recipients)

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        send_debug_mail()
    else:
        send_prod_mail()
