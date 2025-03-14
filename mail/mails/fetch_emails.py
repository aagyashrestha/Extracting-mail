import imaplib
import email
import re
from email.header import decode_header
from django.utils.timezone import now
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail.settings')
django.setup()

from mails.models import Transaction

# Gmail IMAP Configuration
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL_USER = "aagya.shrestha12@gmail.com"  
EMAIL_PASS = "kown eqan rtly bvqv"  

def fetch_emails():
    print("Fetching emails...")
    """Connect to Gmail and fetch transaction emails from a specific sender."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    # Search for emails from the specific sender (donot_reply@nimb.com.np)
    status, messages = mail.search(None, 'FROM "donot_reply@nimb.com.np"')
    email_ids = messages[0].split()

    print(f"Found {len(email_ids)} emails from the specified sender.")
    for email_id in email_ids[-100:]:  # Fetch last 5 emails for testing
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                # Extract email content
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode("utf-8")
                            process_email(body)
                else:
                    body = msg.get_payload(decode=True).decode("utf-8")
                    process_email(body)

    print("Finished fetching emails.")
    mail.logout()

def process_email(body):
    print(f"Processing email body: {body}")  # Debugging statement
    """Extract transaction amount and description from the email body."""
    # Regex to extract the transaction amount (e.g., NPR 2,165.00)
    amount_match = re.search(r"Debited by NPR ([\d,]+\.?\d*)", body)
    amount = amount_match.group(1) if amount_match else None

    # Regex to extract the transaction description (after "transaction detail is")
    desc_match = re.search(r"detail is .*?,\s*(.*?)(?:\s|$)", body)
    description = desc_match.group(1).strip() if desc_match else None

    if amount and description:
        print(f"Extracted amount: {amount}, description: {description}")  # Debugging statement
def save_to_db(amount, description):
    """Save extracted transaction data to the database."""
    transaction = Transaction(amount=float(amount.replace(",", "")), description=description, date=now())
    transaction.save()
    print(f"Saved transaction: {amount} - {description}")

if __name__ == "__main__":
    fetch_emails()
