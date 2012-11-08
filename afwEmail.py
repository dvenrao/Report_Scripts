import smtplib
import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import subprocess

class afwEmail:

##        def __init__(self):
##		EMAIL_SMTP_SERVER
##		EMAIL_SMTP_PORT
##		EMAIL_SENDER
##		EMAIL_SUBJECT
##		EMAIL_RECIPIENTS
##
##                try:
##                        self.smtp = smtplib.SMTP(self.EMAIL_SMTP_SERVER, self.EMAIL_SMTP_PORT)
##                except:
##			print "Could not connect to server "
##        def send(self, gv, mailbody):
##                """     function that sends mail to designated recipients       """
##
##                S_TOADDR = string.join(self.EMAIL_RECIPIENTS, ",")
##                MSG= "To: %s\nFrom: %s\nSubject: %s\n%s" % (S_TOADDR, self.EMAIL_SENDER, self.EMAIL_SUBJECT, mailbody)
##                try:
##                        self.smtp.sendmail(self.EMAIL_SENDER,self.EMAIL_RECIPIENTS,MSG)
##                        self.LogText = 'Email sent to', self.EMAIL_RECIPIENTS
##                        self.Log.WriteLog('info', self.LogText)
##                except:
##                        self.LogText = 'Could not send email'
##                        self.Log.WriteLog('error', self.LogText)



        def __init__(self):
#    		self.EMAIL_SMTP_SERVER="172.16.1.24"
                self.EMAIL_SMTP_SERVER="10.0.1.4"
    		self.EMAIL_SMTP_PORT=25
		self.SMTPUSER = "rmb-popreports"
		self.SMTPPASS = "Aryaka@p0p"
    		self.EMAIL_SENDER="pop-reports@aryaka.com"
    		self.EMAIL_SUBJECT="LIVE REPORT"
    		self.EMAIL_RECIPIENTS=["aunindo@aryaka.com","harish@aryaka.com","lokesh@aryaka.com","venkateshwar@aryaka.com","anu@aryaka.com","kavi@aryaka.com","sridhar@aryaka.com","ankit@aryaka.com","hemant@aryaka.com","manzoor@aryaka.com","vishnu@aryaka.com","deepak@aryaka.com"]
#                self.EMAIL_RECIPIENTS=["gandhi@aryaka.com","venkateshwar@aryaka.com"]

        def send_mail(self):
          cmd1="ls /root/bkp/ASN_Report_Scripts/log -tr | tail -1"
          temp=subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
          out=temp.communicate()
          logfilename=out[0].split()[0]
          flog=open("/root/bkp/ASN_Report_Scripts/log/%s" %logfilename, "r")

          TEXT=flog.read()

          cmd2="ls  *gz"
          temp=subprocess.Popen(cmd2, shell=True, cwd='/root/bkp/ASN_Report_Scripts', stdout=subprocess.PIPE)
          out=temp.communicate()

          FILES=out[0].split()
##	  FILES=["aryaka.tgz" , 'gluster.tgz',  'pop_aryaka.tgz']
##          cmd3 ='tar cvzf logfiles.tgz ./asn_files'
##          cmd =  'tar cvzf x.tgz ./asn_files/*%s* ./asn_files/*%s*' %()
##          subprocess.Popen(cmd3, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()

          assert type(self.EMAIL_RECIPIENTS)==list

          msg = MIMEMultipart()
          msg['From'] = self.EMAIL_SENDER
          msg['To'] = COMMASPACE.join(self.EMAIL_RECIPIENTS)
          msg['Date'] = formatdate(localtime=True)
          msg['Subject'] = self.EMAIL_SUBJECT + " : " + msg['Date']

          msg.attach( MIMEText(TEXT) )

          for f in FILES:
##          f="/root/bkp/ASN_Report_Scripts/logfiles.tgz"
              f="/root/bkp/ASN_Report_Scripts/"+f
              part = MIMEBase('application', "octet-stream")
              part.set_payload( open(f,"rb").read() )
              Encoders.encode_base64(part)
              part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
              msg.attach(part)

          smtp = smtplib.SMTP(self.EMAIL_SMTP_SERVER, self.EMAIL_SMTP_PORT)
#	  smtp.login(self.SMTPUSER, self.SMTPPASS)
#          smtp.set_debuglevel(True)
	  smtpresult = smtp.sendmail(self.EMAIL_SENDER, self.EMAIL_RECIPIENTS, msg.as_string())
          smtp.close()


