# Gmail Auto Mail System

NOTE: Before running the following lines of code, make sure the dependencies are met. You can create a virtual environment using, `python3 -m venv <EnvName>` followed by `source <EnvName>/bin/activate`. Now install dependencies using `pip3 install -r requirements.txt`.

NOTE: Please create a .env file and populate the below key-value pair. You can find the app passwords on account security settings (search in the search bar for app passwords, in google account settings). Also create a MailBody.md file, which holds content of the mail.

```.env
SenderId="<id>"
Password="<>"
```

1. Add contacts into ProfContacts.csv via `python3 ContactHandler.py --email_id <id>`, add other flags if neccesary. It appends the contact into the csv file. Be default the gender is set to Male. Gender is used to add Sir and Ma'am in the text.

2. Run the file `python3 MailProf.py`, it mails the professors. It sends the mail and updates TimeOfFirstContact, which is later used to know whether a mail was sent earlier to avoid repeatition. The body of the mail is read from MailBody.md file, and displayed on gmail client in a markdown formatted fashion.

NOTE: You have to manually update 'Replied' to 'Yes' if a reply has come. Default is 'No'. -- See Future Improvements

3. Run the file `python3 MailReminder.py`. It sends a reminder "A gentel reminder {gender}" if the mail is not replied even after 7 days. Once reminder is sent, the column in csv is set to 'Yes'. And no further reminder will be sent if ran again.

## Future Improvements

A file can be created that checks if a reply has come instead of manually updating it. We can then run the entire script in succession on a cron job, say something like runs every week on some particular day at particular time.
