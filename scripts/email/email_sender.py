import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
# raz.zeevy@mail.huji.ac.il
# samuel.shye@mail.huji.ac.il
# aviad@openu.ac.il
class EmailSender:
    def __init__(self, gmail_user: str, gmail_password: str):
        """
        Generic email sender class using Gmail SMTP.
        Note: For Gmail, you need to use an App Password, not your regular password.
        Generate one at: https://myaccount.google.com/apppasswords
        """
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password

    def send_email(self, 
                  subject: str, 
                  body: str,
                  to: Optional[List[str]] = None,
                  to_display_name: Optional[str] = None,
                  cc: Optional[List[str]] = None,
                  bcc: Optional[List[str]] = None,
                  sender_name: Optional[str] = None,
                  is_html: bool = False) -> bool:
        """
        Send email with support for To, CC, and BCC fields
        
        Args:
            subject: Email subject
            body: Email body content
            to: List of primary recipients (visible to all)
            cc: List of carbon copy recipients (visible to all)
            bcc: List of blind carbon copy recipients (hidden from all)
            sender_name: Optional sender name to show instead of email
            is_html: Whether the body content is HTML
        """
        if not any([to, cc, bcc]):
            raise ValueError("At least one recipient (to, cc, or bcc) must be specified")

        msg = MIMEMultipart('alternative')
        from_header = f"{sender_name} <{self.gmail_user}>" if sender_name else self.gmail_user
        msg['From'] = from_header
        msg['Subject'] = subject
        
        # Add visible recipients
        if to:
            msg['To'] = ", ".join(to)
        if cc:
            msg['Cc'] = ", ".join(cc)
        if to_display_name:
            msg['To'] = f"{to_display_name} <{to_display_name}>"
            
        # Attach the body with the appropriate type
        content_type = 'html' if is_html else 'plain'
        msg.attach(MIMEText(body, content_type, 'utf-8'))

        try:
            # Combine all recipients for actual sending
            all_recipients = []
            if to:
                all_recipients.extend(to)
            if cc:
                all_recipients.extend(cc)
            if bcc:
                all_recipients.extend(bcc)

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_password)
            server.send_message(msg, to_addrs=all_recipients)
            server.close()
            
            print(f"Email sent successfully to {len(all_recipients)} recipients")
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False 