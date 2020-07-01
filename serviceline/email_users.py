import smtplib

server = smtplib.SMTP(host="smtp.soton.ac.uk", port=25)
server.set_debuglevel(True)

server.starttls()
server.login("dwh1d17", "<removed>")


msg = """From: Support <serviceline@soton.ac.uk
To: David Hempston <dwh1d17@soton.ac.uk>
MIME-Version: 1.0
Content-type: text/html
Subject: Welcome to Lyceum

Dear User,<br>
<p>You now have access to the Lyceum service which runs on the Iridis cluster hardware. You should be able to login to one of the login nodes using your university username and password.</p>
<p>Help and support can be found on our wiki pages: https://hpc.soton.ac.uk/redmine/projects/lyceum-support/wiki</p>
<p>For any questions on how to use the cluster please put a new message on the Iridis forum. If you are new to Linux, start with Linux Basics on wiki or follow the Linkedin learning course.</p>
<p>You are entitled to use Lyceum as long as you are a student of the University. When you leave the University, <strong>all your data on Lyceum will be removed following grace period of three months.</strong></p>
<p>
Kind regards,<br>
HPC team
</p>
"""

server.sendmail("serviceline@soton.ac.uk", "dwh1d17@soton.ac.uk", msg)
