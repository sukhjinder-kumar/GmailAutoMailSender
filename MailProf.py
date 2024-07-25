#####################################
## 2. Mailing Professors
#####################################

import csv
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid 
from dotenv import load_dotenv
import markdown

# Configuration for the Gmail account
load_dotenv()
gmail_user = os.getenv('SenderId')
gmail_password = os.getenv('Password')

# File name for the CSV
csv_file = 'ProfContacts.csv'

# Function to send email
def send_email(to_email, subject, body, msg_id):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['Message-ID'] = msg_id

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, to_email, text)
        server.close()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {str(e)}")
        return False

# Function to update the CSV file
def update_csv_file(email_id, new_time_of_first_contact, msg_id):
    rows = []
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['EmailId'] == email_id:
                row['TimeOfFirstContact'] = new_time_of_first_contact
                row['MsgId'] = msg_id
            rows.append(row)

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV file updated for {email_id}")

# Function to process the CSV file
def process_csv():
    if not os.path.isfile(csv_file):
        print(f"{csv_file} does not exist.")
        return

    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row['TimeOfFirstContact']:
                email_id = row['EmailId']
                subject = "Research Opportunity in Mathematics"

                # Read the Markdown file
                with open('MailBody.md', 'r') as file:
                    md_content = file.read()

                gender = row['Gender']
                if gender == "Male":
                    preBody = "Good Evening Sir,"
                elif gender == "Female":
                    preBody = "Good Evening Ma'am,"

                # Convert Markdown to HTML
                body = markdown.markdown(preBody + "\n\n" + md_content)

                # Generate msgid
                msg_id = make_msgid()

                if send_email(email_id, subject, body, msg_id):
                    new_time_of_first_contact = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    update_csv_file(email_id, new_time_of_first_contact, msg_id)

if __name__ == '__main__':
    process_csv()

