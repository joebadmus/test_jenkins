import os, argparse, datetime, smtplib, ssl, socket, sys
from sendEmail import send_mail

## This is a simple python script to check certificate expiry.
## It sends Notification to users when a server certicate will expire based on a threshold set
## Default notification period set is 5days
## This makes use of ssl module in the python standard library to connect to the server 

def main():
    if sendNotification and (email_address is None or smtp_address is None or smpt_port is None):
        print("To send email Notifications provide smtpaddress, smptport and emailaddress\n")
        print("checkCert.py --help for more information\n")
        sys.exit(1)
    else:
        check_cert_expiry()


def check_cert_expiry():
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((server_address, server_port)) as sock:
            with context.wrap_socket(sock, server_side=False, server_hostname=server_address) as ssock:
                cert = ssock.getpeercert(binary_form=True)
        pem_cert = ssl.DER_cert_to_PEM_cert(cert)
        with open('cert_test.pem', 'w') as file:
            file.write(pem_cert)
        output = ssl._ssl._test_decode_cert('cert_test.pem')
        print("Certicate info: \n{}".format(output['subject']))
        print("Certificate was generated on {}".format(output['notBefore']))
        print("Certificate will expiry on {} ".format(output['notAfter']))
        expiry_value = output['notAfter']
        os.remove('cert_test.pem')
        expiry_date = datetime.datetime.strptime(expiry_value, '%b %d %H:%M:%S %Y %Z')
        today = datetime.date.today()
        alert_period = datetime.timedelta(days=5)
        days_left = expiry_date.date() - today  
        if today  >= (expiry_date.date() - alert_period) :
            if days_left.days < 0:
                print("Certificate has expired for {} days. Please renew Certificate".format(abs(days_left.days)))
                if sendNotification:
                    print("Sending email Notification")
                    message = "Certificate has expired for {} days for Server {}. Please renew Certificate".format(abs(days_left.days), server_address)
                    send_mail(days_left.days, message, email_address, smtp_address, smpt_port)
                    print("Email Notification sent Successfully")
            else:
                print("Certificate will expire in {} days. Please renew Certificate".format(abs(days_left.days)))
                if sendNotification:
                    print("Sending email Notification")
                    message = "Certificate will expire in {} days for Server {}. Please renew Certificate".format(abs(days_left.days), server_address)
                    send_mail(days_left.days, message, email_address, smtp_address, smpt_port)
                    print("Email Notification sent Successfully")
    
    except Exception as e:
        print("timeout occured Exception: {}".format(e))


if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required = True, help = "Url of the server, without the protocol (e.g https or https)")
    parser.add_argument("-p", "--port", required= True, type = int, help="port the server listens on, e.g 443")
    parser.add_argument("-S", "--sendemail", help="Enables sending email notification", action="store_true")
    parser.add_argument("-s", "--smtpaddress",help = "Address of smtp server")    
    parser.add_argument("-e", "--email", help= "Email address to delivery notification and alerts")
    parser.add_argument("-P" ,"--eport", help="port of the smtp server", type = int)
    args = parser.parse_args()
    server_address = args.url
    server_port = args.port
    email_address = args.email
    smtp_address = args.smtpaddress
    smpt_port = args.eport
    sendNotification = args.sendemail
    main()
