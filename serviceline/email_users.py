import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def connect():
    import hpcsnow_key 
    server = smtplib.SMTP(host="smtp.soton.ac.uk", port=25)
    server.starttls()
    server.login(hpcsnow_key.username, hpcsnow_key.password)
    return server

def send_lyceum_email(sender_email = "hpc-noreply@soton.ac.uk", receiver_email = "dwh1d17@soton.ac.uk", full_name="David Hempston"):
    with connect() as server:
        msg = lyceum_welcome_email(sender_email, receiver_email, full_name)
        server.sendmail(sender_email, [receiver_email, "dwh1d17@soton.ac.uk"], msg.as_string())
 
def lyceum_welcome_email(sender_email = "hpc-noreply@soton.ac.uk", receiver_email = "dwh1d17@soton.ac.uk", full_name="David Hempston"):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Welcome to Lyceum'

    msgText = MIMEText("""
        <p>Dear {},</p>
        <p>You now have access to the Lyceum service which runs on the Iridis cluster hardware. You should be able to login to one of the login nodes using your university username and password.
        Help and support can be found on our wiki pages: https://hpc.soton.ac.uk/redmine/projects/lyceum-support/wiki. If you are new to Linux we recommend the Linkedin learning course. For any questions on how to use the cluster please put a new message on the apropiate Iridis forum. </p>
        <p>https://hpc.soton.ac.uk/redmine/projects/iridis-4-support/boards</p>
        <p>https://hpc.soton.ac.uk/redmine/projects/iridis-5-support/boards</p>
        <p></p>
        <p>You are entitled to use Lyceum as long as you are a student of the University. When you leave the University, <strong>all your data on Lyceum will be removed following grace period of three months.</strong></p>
        <p>
        Kind regards,<br>
        HPC team
        </p>
        """.format(full_name), 'html')
    msg.attach(msgText)
    return msg

if __name__ == "__main__":
    sender_email = "hpc-noreply@soton.ac.uk"
    receiver_email = "dwh1d17@soton.ac.uk"
    with connect() as server:
        server.sendmail(sender_email, receiver_email, lyceum_welcome_email().as_string())
