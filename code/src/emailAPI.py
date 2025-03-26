import imaplib
import email
from email.header import decode_header

def get_recent_email(username, password):
    try:
        # Connect to the Gmail IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)

        # Select the inbox
        mail.select("inbox")

        # Search for all emails in the inbox
        status, messages = mail.search(None, 'X-GM-RAW "category:primary"')
        message_ids = messages[0].split()

        # Get the most recent email
        latest_email_id = message_ids[-1]

        # Fetch the email
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]

        # Parse the email content
        msg = email.message_from_bytes(raw_email)

        # Extract email details
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        from_ = msg.get("From")
        print(f"Subject: {subject}")
        print(f"From: {from_}")

         # Extract the email body (both plain text and HTML)
        body = None
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()
                break
            elif content_type == "text/html" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()

        if body:
            print(f"\nBody: {body}")
        else:
            print("No readable content found.")

        # Logout
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

# Usage
username = "" # Use email address here
password = "" # Use app password here
get_recent_email(username, password)
