import smtplib
from getpass import getpass

## This is a simple python script to check certificate expiry.
## It sends Notification to users when a server certicate will expire based on a threshold set
## Default notification period set is 5days
## This makes use of ssl module in the python standard library to connect to the server 


def send_mail(day, body, email_address, smtp_address, smpt_port):
    try:

        email_password = getpass('Enter email passowrd\n')
        with smtplib.SMTP(smtp_address, smpt_port) as smtp:
            #smtp.set_debuglevel(9)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
        
            smtp.login(email_address, email_password)
            subject = 'Certificate Expiry Notification'
            msg = f'Subject:{subject}\n\n{body}'
            smtp.sendmail(email_address, email_address, msg)
    
    except Exception as e:
        print("Error occured while Sending email Notification Exception: {}".format(e))
