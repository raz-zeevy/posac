import subprocess
from typing import List, Tuple
from email_sender import EmailSender
import re
from datetime import datetime

class GitUpdateNotifier:
    def __init__(self, email_sender: EmailSender):
        """
        Handles git update notification functionality
        
        Args:
            email_sender: EmailSender instance for sending emails
        """
        self.email_sender = email_sender
        self.setup_exe_link = "https://raw.githubusercontent.com/raz-zeevy/posac/main/releases/PosacSetupDebug.exe"

    def get_latest_commit_info(self) -> Tuple[str, str, str]:
        """
        Get the latest commit message and extract version
        Returns:
            Tuple of (full_message, version, commit_hash)
        """
        date_string = datetime.now().strftime("%d/%m/%Y")
        try:
            commit_msg = subprocess.check_output(
                ['git', 'log', '-1', '--pretty=%B'], 
                universal_newlines=True
            ).strip()
            
            commit_hash = subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD'],
                universal_newlines=True
            ).strip()
            
            # Extract version from first line of commit message
            # Expecting format: "Version X.X.X.X: ..."
            version_match = re.match(r"Version (\d+\.\d+\.\d+\.\d+)", commit_msg)
            if version_match:
                version = version_match.group(1)
            else:
                version = f"{date_string}"
            
            return commit_msg, version, commit_hash
        except subprocess.CalledProcessError:
            return "No commit information available", date_string, ""

    def create_update_email_content(self) -> Tuple[str, str]:
        """
        Create the email subject and body for update notification in Hebrew
        
        Returns:
            Tuple of (subject, body)
        """
        commit_msg, version, _ = self.get_latest_commit_info()
        
        # Split commit message into title and body
        commit_lines = commit_msg.split('\n')
        commit_title = commit_lines[0] if commit_lines else ""
        commit_body = '\n'.join(commit_lines[1:]).strip() if len(commit_lines) > 1 else ""
        
        subject = f"עדכון גרסה - Posac {version}"
        
        # Create HTML email with stronger RTL styling
        body = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                * {{
                    font-family: Arial, sans-serif;
                }}
                .email-container {{
                    padding: 20px;
                    max-width: 600px;
                    margin: 0 auto;
                    direction: rtl !important;
                    text-align: right !important;
                }}
                .hebrew-text {{
                    direction: rtl !important;
                    text-align: right !important;
                }}
                .ltr-text {{
                    direction: ltr !important;
                    text-align: left !important;
                    unicode-bidi: embed;
                }}
                .commit-title {{
                    font-size: 16px;
                    font-weight: bold;
                    margin: 20px 0 10px 0;
                    padding-bottom: 5px;
                    border-bottom: 1px solid #ddd;
                }}
                .commit-body {{
                    white-space: pre-wrap;
                    margin: 10px 0;
                    line-height: 1.5;
                }}
                .link {{
                    color: #0366d6;
                    text-decoration: none;
                }}
                .link:hover {{
                    text-decoration: underline;
                }}
                .signature {{
                    margin-top: 20px;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="hebrew-text">התפרסמה גרסה חדשה לתוכנה Posac.</div>
                <div class="hebrew-text" style="margin: 15px 0;">
                    אפשר להוריד את התוכנה בקישור ההורדה הקבוע:<br>
                    <span class="ltr-text"><a class="link" href="{self.setup_exe_link}">{self.setup_exe_link}</a></span>
                </div>
                <div class="commit-title ltr-text">{commit_title}</div>
                <div class="commit-body ltr-text">{commit_body}</div>
                
                <div class="signature hebrew-text">
                    בברכה,<br>
                    רז
                </div>
            </div>
        </body>
        </html>
        """
        
        return subject, body

    def send_update_notification(self, recipients: List[str]) -> bool:
        """
        Send update notification email to recipients using BCC
        """
        subject, body = self.create_update_email_content()
        return self.email_sender.send_email(
            subject=subject,
            body=body,
            to_display_name="Posac Users",
            bcc=recipients,
            sender_name="Posac Updates",
            is_html=True
        ) 