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
        server.sendmail(sender_email, receiver_email, msg.as_string())
 
def lyceum_welcome_email(sender_email = "hpc-noreply@soton.ac.uk", receiver_email = "dwh1d17@soton.ac.uk", full_name="David Hempston"):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Welcome to Lyceum'

    msgText = MIMEText("""
        <p>Dear {},</p>
<p>You now have access to the Lyceum service which runs on the Iridis cluster hardware. To connect, ssh to one of the login nodes using your university username and password. </p>
<p>The Iridis 4 login nodes are:<br>
<br>
Iridis4_a.soton.ac.uk   # The busiest<br>
Iridis4_b.soton.ac.uk   # The quietest<br>
Iridis4_c.soton.ac.uk   # For long downloads<br>
<br>
Help and support can be found on our wiki pages: https://hpc.soton.ac.uk/redmine/projects/getting-started/wiki/Iridis_Welcome<br>
</p>
<p>If you not on the university network (not on campus or in halls) you will need to first connect to the university VPN. If you are on Windows or mac please follow the steps below/</p>
<p>
1) Open https://globalprotect.soton.ac.uk in a browser and login using your University account. <br>
2) Select the version of the agent relevant to your OS (e.g. Windows 64 bit for windows 10).<br>
3) The installer will download. Once complete, launch the installer and follow the wizard through the installation process.<br>
4) Once installed a globe shaped icon will appear in the Notification area (Windows).<br>
5) Click on the globe icon and enter the portal address 'globalprotect.soton.ac.uk'. Click 'Connect'. Enter user credentials when prompted.<br>
6) You will now be connected to the University's VPN service. To disconnect, press 'Disconnect'. The GlobalProtect icon will always appear in the Notification area, regardless of the status of the connection.</p>

<p>If you are new to Linux, then a good place to start is with Linux Basics on the wiki or follow the Linkedin learning course.</p>

<p>You are entitled to use Lyceum as long as you are a student of the University. 
When you leave the University, all your data on Lyceum will be removed following 
grace period of three months.</p>

<p>Kind regards,<br>
HPC team</p>
        """.format(full_name), 'html')
    msg.attach(msgText)
    return msg

if __name__ == "__main__":
    sender_email = "hpc-noreply@soton.ac.uk"
    receiver_email = "dwh1d17@soton.ac.uk"
    with connect() as server:
        server.sendmail(sender_email, receiver_email, lyceum_welcome_email().as_string())
