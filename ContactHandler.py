####################################
## 1. Handle Contacts
####################################

import csv
import os
import argparse
from datetime import datetime

# File name for the CSV
csv_file = 'ProfContacts.csv'

# Columns for the CSV
columns = ['EmailId', 'Gender', 'TimeOfFirstContact', 'MsgId', 'Replied', 'ReminderSent']

# Function to create the CSV file if it doesn't exist
def create_csv_file():
    if not os.path.isfile(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
        print(f"{csv_file} created successfully.")
    else:
        print(f"{csv_file} already exists.")

# Function to check for duplicates
def check_duplicate(email_id):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['EmailId'] == email_id:
                return True
    return False

# Function to add a row to the CSV file
def add_row_to_csv(email_id, gender, time_of_first_contact, message_id, replied, reminder_sent):
    if check_duplicate(email_id):
        print(f"Error: Duplicate entry for Email ID {email_id}. Row not added.")
        return

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writerow({
            'EmailId': email_id,
            'Gender': gender,
            'TimeOfFirstContact': time_of_first_contact,
	    'MsgId': message_id,
            'Replied': replied,
            'ReminderSent': reminder_sent
        })
    print("Row added successfully.")

# Setting up the command line interface
def main():
    parser = argparse.ArgumentParser(description='Manage contacts CSV file.')
    parser.add_argument('--email_id', required=True, help='Email ID of the contact')
    parser.add_argument('--gender', default='Male', choices=['Male', 'Female'], help='Gender of the contact (default: Male)')
    parser.add_argument('--time_of_first_contact', help='Time of first contact (format: YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('--message_id', help='RFC2882 compliant string')
    parser.add_argument('--replied', default='No', choices=['Yes', 'No'],help='Has the contact replied? (Yes/No)')
    parser.add_argument('--reminder_sent', default='No', choices=['Yes', 'No'],help='Has a reminder been sent? (Yes/No)')

    args = parser.parse_args()

    # Ensure the CSV file exists
    create_csv_file()

    # Add the new row
    add_row_to_csv(
        email_id=args.email_id,
        gender=args.gender,
        time_of_first_contact=args.time_of_first_contact,
	message_id=args.message_id,
        replied=args.replied,
        reminder_sent=args.reminder_sent
    )

if __name__ == '__main__':
    main()

