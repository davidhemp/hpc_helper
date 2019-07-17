import smtplib                                                                               
from email.message import EmailMessage     
import subprocess

def email_ops(content, subject):
    msg = EmailMessage()                                                                         
    msg.set_content(content + "\n kind regards,\n David H")                                                         
    msg['Subject'] = subject                                                      
    msg['From'] = "hpc-admin@lists.soton.ac.uk"                    
    msg['To'] = "socibm@soton.ac.uk"                                                            
    s = smtplib.SMTP('smtp.soton.ac.uk')                                                         
    s.send_message(msg)

raw_disks = subprocess.check_output('/usr/bin/ssh violet12 "/usr/lpp/mmfs/bin/mmlspdisk all --not-ok"', shell=True)
raw_disks = raw_disks.decode().split("\n") 

if raw_disks.count("pdisk:") > 1:
    message = "Dear Ops,\n We have {} failed disks on Iridis 4. I have attached the log outs below.\n\n".format(raw_disks.count("pdisk:"))
else:
    message = "Dear Ops,\n We have a failed disk on Iridis 4. I have attached the log outs below.\n\n"
subject = "Failed disks: "
n = 0
while n < raw_disks.count("pdisk:"):
    i = 0 + 30*n
    j = 30*(n+1)
    message += "\n".join(raw_disks[i:j]) + "\n\n"
    name = raw_disks[i:j][2].split('"')[1]
    rgroup = raw_disks[i:j][4].split('"')[1]
    cmd = '/usr/bin/ssh violet12 "/usr/lpp/mmfs/bin/mmlsrecoverygroupevents {} --long-term CEW --days=7 | grep {} | tail -3"'.format(rgroup, name)
    logs = subprocess.check_output(cmd, shell=True)
    message += logs.decode() + "\n"
    subject += " " + name
    print (name, rgroup)
    n += 1
    
email_ops(message, subject)
