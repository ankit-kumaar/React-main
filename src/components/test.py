import imaplib
import email
from email.header import decode_header
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GmailClient:
    def __init__(self, username, password, imap_server='imap.gmail.com'):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.mail = None

    def connect_to_gmail(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.username, self.password)
            logger.info('Connected to Gmail')
        except imaplib.IMAP4.error as e:
            logger.error(f'Login failed: {e}')
            raise Exception('Login failed')

    def get_email_body(self, email_id):
        try:
            _, msg = self.mail.fetch(email_id, '(RFC822)')
            raw_message = msg[0][1]
            message = email.message_from_bytes(raw_message)
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode('utf-8')
                    return body
        except Exception as e:
            logger.error(f'Failed to retrieve email body: {e}')
            raise Exception('Failed to retrieve email body')

    def get_all_emails_from_user(self, sender):
        try:
            self.mail.select('inbox')
            _, search_data = self.mail.search(None, f'FROM "{sender}"')
            email_ids = search_data[0].split()
            return email_ids
        except Exception as e:
            logger.error(f'Failed to retrieve emails from {sender}: {e}')
            raise Exception('Failed to retrieve emails')

    def get_all_emails_under_label(self, label):
        try:
            self.mail.select(label)
            _, search_data = self.mail.search(None, 'ALL')
            email_ids = search_data[0].split()
            return email_ids
        except Exception as e:
            logger.error(f'Failed to retrieve emails under {label}: {e}')
            raise Exception('Failed to retrieve emails')

    def fetch_unread_emails(self):
        try:
            self.mail.select('inbox')
            _, search_data = self.mail.search(None, 'UNSEEN')
            email_ids = search_data[0].split()
            return email_ids
        except Exception as e:
            logger.error(f'Failed to retrieve unread emails: {e}')
            raise Exception('Failed to retrieve unread emails')

    def mark_email_as_read(self, email_id):
        try:
            self.mail.store(email_id, '+FLAGS', '\Seen')
            logger.info(f'Marked email {email_id} as read')
        except Exception as e:
            logger.error(f'Failed to mark email {email_id} as read: {e}')
            raise Exception('Failed to mark email as read')

    def delete_email(self, email_id):
        try:
            self.mail.store(email_id, '+FLAGS', '\Deleted')
            self.mail.expunge()
            logger.info(f'Deleted email {email_id}')
        except Exception as e:
            logger.error(f'Failed to delete email {email_id}: {e}')
            raise Exception('Failed to delete email')

    def save_email_attachments(self, email_id, download_folder):
        try:
            _, msg = self.mail.fetch(email_id, '(RFC822)')
            raw_message = msg[0][1]
            message = email.message_from_bytes(raw_message)
            for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if filename:
                    with open(os.path.join(download_folder, filename), 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    logger.info(f'Saved attachment {filename} to {download_folder}')
        except Exception as e:
            logger.error(f'Failed to save attachments for email {email_id}: {e}')
            raise Exception('Failed to save attachments')

# Example usage
if __name__ == '__main__':
    username = 'your_email@gmail.com'
    password = 'your_password'
    client = GmailClient(username, password)
    client.connect_to_gmail()

    # Get email body
    email_id = client.fetch_unread_emails()[0]
    print(client.get_email_body(email_id))

    # Get all emails from a user
    sender = 'sender@example.com'
    email_ids = client.get_all_emails_from_user(sender)
    print(email_ids)

    # Get all emails under a label
    label = 'label_name'
    email_ids = client.get_all_emails_under_label(label)
    print(email_ids)

    # Mark an email as read
    client.mark_email_as_read(email_id)

    # Delete an email
    client.delete_email(email_id)

    # Save email attachments
    download_folder = '/path/to/download/folder'
    client.save_email_attachments(email_id, download_folder)