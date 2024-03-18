import imaplib
import email

# Gmail IMAP server details
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Your Gmail credentials
EMAIL = 'faxstoredelivery@gmail.com'
PASSWORD = 'gghh hway csxq gggq'

# Connect to the IMAP server
imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# Login to your account
imap.login(EMAIL, PASSWORD)

# Select the inbox folder
imap.select('INBOX')

# Search for emails
status, messages = imap.search(None, 'ALL')

# Get the list of message IDs
message_ids = messages[0].split()

# Loop through each message ID and fetch the email
for msg_id in message_ids:
    print("msg Id : ",msg_id)
    status, msg_data = imap.fetch(msg_id, '(RFC822)')
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)
    # print("FROM: ", email_message['From'])
    # print("SUBJECT: ", email_message['Subject'])
    message_id = email_message['Message-ID']

    # print("Message ID :" ,message_id)
    email_link = f"https://mail.google.com/mail/u/0/#inbox/{message_id}"
    print("Link to Email Message:", email_message.keys())
    if email_message['Subject'] != 'Test':
        break
    
    # Check if the message has a payload
    if email_message.is_multipart():
        body = ""
        # Loop through each part of the message
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Extract the text content from the email
            if "attachment" not in content_disposition:
                payload = part.get_payload()
                if isinstance(payload, list):
                    # If payload is a list, concatenate each part
                    body += ''.join([p.get_payload(decode=True).decode() for p in payload])
                else:
                    body += payload
        print("Body: ", body)
        with open("output.html", "w", encoding="utf-8") as file:
            # Write the data to the file
            file.write(body)
        
        break
    else:
        # If the message does not have a payload, print a message indicating that
        body = email_message.get_payload(decode=True).decode()
        print("Body: ", body)


# Logout from the server
imap.logout()
