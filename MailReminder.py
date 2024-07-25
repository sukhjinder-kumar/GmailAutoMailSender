import smtplib
import email.utils
from email.mime.text import MIMEText
import os
import csv
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Configuration for the Gmail account
load_dotenv()
sender_email = os.getenv('SenderId')
sender_password = os.getenv('Password')

# Read the CSV file
csv_file = 'ProfContacts.csv'
contacts = []

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        contacts.append(row)

# Check each contact for reminder criteria
current_time = datetime.now()
reminder_contacts = []

for contact in contacts:
    if contact['Replied'] == 'No':
        time_of_first_contact = datetime.strptime(contact['TimeOfFirstContact'], '%Y-%m-%d %H:%M:%S')
        if current_time - time_of_first_contact > timedelta(days=8) and contact['ReminderSent'] == 'No':
            reminder_contacts.append(contact)

# Send reminder emails
for contact in reminder_contacts:
    recipient_email = contact['EmailId']
    original_msg_id = contact['MsgId']

    # Compose the reminder email
    if contact['Gender'] == 'Male':
        msg = MIMEText('A gentle reminder Sir.')
    elif contact['Gender'] == 'Female':
        msg = MIMEText("A gentle reminder Ma'am.")
    msg['To'] = recipient_email
    msg['From'] = sender_email
    msg['Subject'] = 'RE: Research Opportunity in Mathematics'
    msg['Message-ID'] = email.utils.make_msgid()
    msg['In-Reply-To'] = original_msg_id
    msg['References'] = original_msg_id

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())

    # Update the CSV file
    contact['ReminderSent'] = 'Yes'
    print(f"Reminder sent for {contact['EmailId']}.")

# Write the updated contacts back to the CSV file
with open(csv_file, 'w', newline='') as f:
    fieldnames = ['EmailId', 'Gender', 'TimeOfFirstContact', 'MsgId', 'Replied', 'ReminderSent']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(contacts)

print('CSV File updated for above emails')
