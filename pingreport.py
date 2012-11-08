from urllib2 import Request, urlopen, URLError, HTTPError
import re
import subprocess

class Ping_Report:
    def __init__ (self):
        self.Bng_Mil=""
        self.Bng_Bom=""
        self.Mil_Sjc=""
        self.Mil_Ash=""
        r=self.downloadReport("http://172.19.1.33/ping_log_status.html")
        self.generateReport(r,0)
        r=self.downloadReport("http://172.16.1.21/NOS/ping_log_status.html")
        self.generateReport(r,1)
        self.generateFiles()


    def downloadReport(self, URL):
        try:
            req = Request(url=URL)
            response=urlopen(req)
        except:
            return "ERROR: Couldn't Connect to URL %s" %(URL)
        try:
            a=response.read()
            return a
        except:
            return "ERROR: Couldn't Download  the Pin report from URL %s" %(URL)



    def generateReport(self,a,j):
	print len(a)
        if not j and len(a) <= 300:
            self.Bng_Mil=self.Bng_Mil+a
            self.Bng_Bom=self.Bng_Mil+a
            print   self.Bng_Mil,self.Bng_Bom, self.Mil_Ash, self.Mil_Sjc
	    	
        elif len(a) <= 300:
            self.Mil_Ash=self.Mil_Ash+a
            self.Mil_Sjc=self.Mil_Sjc+a
	    print   self.Bng_Mil,self.Bng_Bom, self.Mil_Ash, self.Mil_Sjc	

        else:
            b=a.split('-----------------------------=====--------------------')
    #	print len(b)
            for i in range(2,len(b)-2):
    #	     print "i(b)=",i
                 c=b[i].split("~~~~~~~~~~~~~~~~~~[NEXT PING STATUS]~~~~~~~~~~~~~~~~~~~~~~")
                 for i in range(2):
    #		print "i(c)=",i,c[i][1:200]
                    t=re.search('(\d+:\d+:\d+) ',c[i])
                    if t:
                        t=t.group(1)
                    d=re.search(r'rtt min/avg/max/mdev = \d+.\d+/(\d+.\d+)',c[i])
                    if d:
                        d=d.group(1)
                    l=re.search('(\d+) received',c[i])
                    if l:
                        l=str(20 - int(l.group(1)))
                    z1 = re.search('Milpitas -- Ashburn',c[i])
                    z2 = re.search('Milpitas -- San Jose',c[i])
                    z3 = re.search('Bangalore -- Milpitas',c[i])
                    z4 = re.search('Bangalore -- Mumbai POP',c[i])
                    if z1:
                        self.Mil_Ash=self.Mil_Ash+("%s, %s, %s\n" %(t,d,l))
                    if z2:
                        self.Mil_Sjc=self.Mil_Sjc+("%s, %s, %s\n" %(t,d,l))

                    if z3:
                        self.Bng_Mil=self.Bng_Mil+("%s, %s, %s\n" %(t,d,l))
                    if z4:
                        self.Bng_Bom=self.Bng_Bom+("%s, %s, %s\n" %(t,d,l))

    def generateFiles(self):

        fd=open("Bng_Mil.csv","w")
        fd.write(self.Bng_Mil)
        fd.close()

        fd=open("Bng_Bom.csv","w")
        fd.write(self.Bng_Bom)
        fd.close()

        fd=open("Mil_Ash.csv","w")
        fd.write(self.Mil_Ash)
        fd.close()

        fd=open("Mil_Sjc.csv","w")
        fd.write(self.Mil_Sjc)
        fd.close()
        cmd =  'tar cvzf pingreport.tgz ./*csv'
        subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()

