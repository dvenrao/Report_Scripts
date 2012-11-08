#!/usr/bin/python
#
import os, os.path, sys, subprocess, datetime, time, logging, aniLogging, signal, re, string
from subprocess import PIPE
class afwConnect:
#---------------------------------------arlogcall function-----------------------------------------------------
# arlogcall connects to the live pop machines and re-applies the poutput and the filters


	def writetofile(self,temp):
	     print temp
             col=temp[0].split('\n')
             for i in range(1,len(col)-1):
          	col[i]=col[i].strip()
          	z=re.search(r'(\d) (\d)',col[i])
          	col[i]=re.sub(r'\d \d',z.group(1)+'--'+z.group(2),col[i])
		print col[i]
             t=""
             for j in range(0, len(col[0].split())):
            		for i in range(0,len(col)-1):
               			t=t+col[i].split()[j]+(30-len(col[i].split()[j]))*" "
            		t=t+'\n'


	def writetofile3(self,temp):
	    self.file_handle.write(t)
	    self.file_handle.flush()


	def writetofile2(self,temp):
            col=temp[0].split('\n')
            index=col[0:len(col)-1]
            col[0]=col[0].strip().split()
            for i in range(1,len(col)-1):
              z=re.search(r'(\d) (\d)',col[i])
              if z:
                  col[i]=re.sub(r'\d \d',z.group(1)+'--'+z.group(2),col[i])
            for k in range(1,len(col)-1):
                j=0
                column=[]
                for i in range(0,len(col[0])):
                    st=string.find(index[0],col[0][i])
                    if i==len(col[0])-1:
                        en=len(index[0])-1
                    else:
                        en=string.find(index[0],col[0][i+1])
                    gap=en-st
                    s= index[k][st:en-gap/2]
                    if re.search('[0-9]|[a-z]',s):
                        column.append(col[k].split()[j])
                        j=j+1
                    else:
                        column.append("\t")
                col[k]=column
            t="\n"
            for j in range(0, len(col[0])):
##                print "row=",j
                for i in range(0,len(col)-1):
                   t=t+col[i][j]+(30-len(col[i][j]))*" "
                t=t+'\n'
            t=t+"\n\n"
	    self.file_handle.write(t)
	    self.file_handle.flush()



	def arlogcall(self,option):

		ha_manager_str="  arlog -n ha_manager " +str(option)
		controller_str="  arlog -n controller "+str(option)
		ipsec_str="  arlog -n ipsec "+str(option)
		for pns in self.pnslist:
		    self.ha_man= "ssh " +  str(pns) + " \"" + ha_manager_str +"\""
            self.control_pns="ssh " +  str(pns)+" \"" + controller_str +"\""
            self.ipsec="ssh " +  str(pns) +" \"" + ipsec_str +"\""

		temp=subprocess.Popen(self.ha_man,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.control_pns,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.ipsec,  shell=True)
		temp.wait()

        for pss in self.psslist:
                self.control_pss="ssh " +  str(pss) +" \"" + controller_str +"\""
                temp=subprocess.Popen(self.control_pss,  shell=True)
		temp.wait()


        for customer in customerlist:
               	self.pnsb_str= "ssh " + str(self.p[customer]["bpop"][0]) +" \"" + "  arlog -n pns"+str(self.p[customer]["ni"][0])+" " +str(option)+" \""
                self.pnsh_str="ssh " + str(self.p[customer]["hpop"][0]) + " \"" + "  arlog -n pns"+str(self.p[customer]["ni"][1])+" " +str(option)+" \""
                self.pssb_str="ssh " + str(self.p[customer]["bpop"][1]) + " \"" + " arlog -n pss"+str(self.p[customer]["ni"][0])+" " +str(option)+" \""
                self.pssh_str="ssh " + str(self.p[customer]["hpop"][1]) + " \"" + " arlog -n pss"+str(self.p[customer]["ni"][1])+" " +str(option)+" \""
                temp=subprocess.Popen(self.pnsb_str,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.pnsh_str,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.pssb_str,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.pssh_str,  shell=True)
		temp.wait()

#---------------------------------------applylog function-----------------------------------------------------
# applylog function is called by copylog function
# this function deletes the filters and the outputs that are used by log_settings on the live pops so that the new error/warn/alert messages can be written into the files.
# This function calls arlogcall

	def applylog(self):
                ha_manager_str=" arlog -n ha_manager -r"
                controller_str=" arlog -n controller -r"
                ipsec_str=" arlog -n ipsec -r"
		option="-f warn -D; "
		print "arlog is being called ...", option, "\n"
		self.arlogcall(option)
		option="-f error -D"
		print "arlog is being called ...", option, "\n"
		self.arlogcall(option)
		option="-f alert -D"
		print "arlog is being called ...", option, "\n"
		self.arlogcall(option)
		option="-o warn -D"
		print "arlog is being called ...", option, "\n"
		self.arlogcall(option)
		option="-o error -D"
		print "arlog is being called ...", option, "\n"
		self.arlogcall(option)
		option="-o alert -D"
		print "arlog is being called ...", option, "\n"
		self.arlogcall(option)
		option="-r"
		print "arlog is being called ...", option, "\n"
		self.arlogcall(option)

#		self.pnsb_str= "ssh " + str(self.p[customer]["bpop"][0]) +" \"" + "  arlog -f warn -D"+str(self.p[customer]["ni"][0])+" -r\""



#---------------------------------------Connect function-----------------------------------------------------
# copyfiles connects to all tan and pan machines and collects the log files.
# log files are created by arlog running on each of those machines.
# copyfiles function, copies the files over and calls apply logs function

	def copyfiles(self,customer):

        for pns in self.pnslist:
    		pop_pns_controller_log =      "scp root@" + str(pns) +":/var/aryaka/controller/*_controller_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
    		pop_pns_controller_log_del =  "ssh root@" + str(pns) +" mv /var/aryaka/controller/*_controller_*.log /tmp/"
            pop_pns_ha_manager_log =      "scp root@" + str(pns) +":/var/aryaka/ha_manager/*_ha_manager_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
            pop_pns_ha_manager_log_del =  "ssh root@" + str(pns) +" mv /var/aryaka/ha_manager/*_ha_manager_*.log /tmp/"
    		pop_pns_ipsec_log =           "scp root@" + str(pns) +":/var/aryaka/nexus/racoon/*_ipsec_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
    		pop_pns_ipsec_log_del =       "ssh root@" + str(pns) +" mv /var/aryaka/nexus/racoon/*_ipsec_*.log /tmp/"
        print "Copying ", pop_pns_controller_log, "...."
	    temp=subprocess.Popen(str(pop_pns_controller_log), shell=True, stdout=self.file_handle)
	    temp.wait()
        temp=subprocess.Popen(str(pop_pns_controller_log_del), shell=True)
		temp.wait()
		print "Copying ",pop_pns_ha_manager_log, "...."
		temp=subprocess.Popen(str(pop_pns_ha_manager_log), shell=True, stdout=self.file_handle)
		temp.wait()
		temp=subprocess.Popen(str(pop_pns_ha_manager_log_del), shell=True)
		temp.wait()
		print "Copying ",bpop_pns_ipsec_log, "...."
		temp=subprocess.Popen(str(pop_pns_ipsec_log), shell=True, stdout=self.file_handle)
		temp.wait()
		temp=subprocess.Popen(str(pop_pns_ipsec_log_del), shell=True)
		temp.wait()



        for pss in self.psslist:
    		pop_pss_controller_log =     "scp root@" + str(pss) +":/var/aryaka/controller/*_controller_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
            pop_pss_controller_log_del = "ssh root@" +str(pss) +" mv /var/aryaka/controller/*_controller_*.log /tmp/"
		print "Copying ",pop_pss_controller_log, "...."
		temp=subprocess.Popen(str(pop_pss_controller_log), shell=True, stdout=self.file_handle)
		temp.wait()
		temp=subprocess.Popen(str(pop_pss_controller_log_del), shell=True)
		temp.wait()



        for customer in customerlist:
        bpop_pns_pns_log =      "scp root@" + str(self.p[customer]["bpop"][0]) +":/var/aryaka/nexus/pns_"+ str(self.p[customer]["ni"][0]) +"/*_pns_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		hpop_pns_pns_log =      "scp root@" + str(self.p[customer]["hpop"][0]) +":/var/aryaka/nexus/pns_"+ str(self.p[customer]["ni"][1]) +"/*_pns_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		bpop_pss_pss_log =      "scp root@" + str(self.p[customer]["bpop"][1]) +":/var/aryaka/nexus/pss_"+ str(self.p[customer]["ni"][0]) +"/*_pss_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		hpop_pss_pss_log =      "scp root@" + str(self.p[customer]["hpop"][1]) +":/var/aryaka/nexus/pss_"+ str(self.p[customer]["ni"][1]) +"/*_pss_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		bpop_pns_pns_log_del =  "ssh root@" + str(self.p[customer]["bpop"][0]) +" mv /var/aryaka/nexus/pns_"+ str(self.p[customer]["ni"][0]) +"/*_pns_*.log /tmp/"
		bpop_pss_pss_log_del =  "ssh root@" +  str(self.p[customer]["hpop"][1]) +" mv /var/aryaka/nexus/pss_"+ str(self.p[customer]["ni"][1]) +"/*_pss_*.log /tmp/"

		print "Copying ",bpop_pns_pns_log, "...."
		temp=subprocess.Popen(str(bpop_pns_pns_log), shell=True, stdout=self.file_handle)
		temp.wait()
		print "Copying ",hpop_pns_pns_log, "...."
		temp=subprocess.Popen(str(hpop_pns_pns_log), shell=True, stdout=self.file_handle)
		temp.wait()
		print "Copying ",bpop_pss_pss_log, "...."
		temp=subprocess.Popen(str(bpop_pss_pss_log), shell=True, stdout=self.file_handle)
		temp.wait()
		print "Copying ",hpop_pss_pss_log, "...."
		temp=subprocess.Popen(str(hpop_pss_pss_log), shell=True, stdout=self.file_handle)
		temp.wait()
		temp=subprocess.Popen(str(bpop_pns_pns_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(bpop_pss_pss_log_del), shell=True)
		temp.wait()

#		self.applylog()

#---------------------------------------Connect function-----------------------------------------------------
# Connect function is called by afw_report after __init__ is called.
# This function connects to the pops and collects cli information
# After collecting cli information, it calls copyfiles function to collect the log files

	def Connect(self):

		nexus_string=' nxctl status'

		self.file_handle.write("LIVE ARYAKA POP REPORT\n")
		self.file_handle.write( "SJC POP INFO ")
		self.file_handle.flush()

		for pns in self.pnslist:
		    self.file_handle.write('\n'+20*'#'+  pns +" POP INFO "+20*'#'+'\n')
		    self.file_handle.flush()
		    connect_string_pns= "ssh " + str(pns) + nexus_string
		    temp=subprocess.Popen(str(connect_string_pns), shell=True, stdout=self.file_handle)
		    temp.wait()
		    arstatus_ipsec="ssh " + str(pns) + " \"" + " arstatus -i "+ "\""
                self.file_handle.write('\n\n'+10*'-'+ pns +' IPSEC INFO'+10*'-'+'\n')
                self.file_handle.flush()
                temp=subprocess.Popen(str(arstatus_ipsec), shell=True, stdout=self.file_handle)
                temp.wait()




        for customer in self.customerlist:
            self.file_handle.write('\n\n'+10*'-'+ customer +10*'-'+'\n')
            self.file_handle.flush()
    		connections_hpop="ssh " + str(self.p[customer]["hpop"][1]) + " \""+ " asn_cli.py -n pss_"+str(self.p[customer]["ni"][1])+" -c 'show tcp conntable'| awk '/Total Intercepted/ {print $4}'" +"\""
    		connections_bpop="ssh " + str(self.p[customer]["bpop"][1]) + " \"" + " asn_cli.py -n pss_"+str(self.p[customer]["ni"][0])+" -c 'show tcp conntable'| awk '/Total Intercepted/ {print $4}'" +"\""
    		arstatus_bpns="ssh " + str(self.p[customer]["bpop"][0]) + " \"" + " arstatus -t " + str(self.p[customer]["ni"][0]) + "\""
    		arstatus_hpns="ssh " + str(self.p[customer]["hpop"][0]) + " \"" + " arstatus -t " + str(self.p[customer]["ni"][1]) + "\""
    		arstatus_bpss="ssh " + str(self.p[customer]["bpop"][0]) + " \"" + " arstatus -p " + str(self.p[customer]["ni"][0]) + "\""
    		arstatus_hpss="ssh " + str(self.p[customer]["hpop"][0]) + " \"" + " arstatus -p " + str(self.p[customer]["ni"][1]) + "\""
    		total_bnap_pss="ssh " + str(self.p[customer]["bnap"]) + " \"" + " /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show tcp conntable'| awk '/Total Intercepted/ {print $4}'" + "\""
    		current_bnap_pss="ssh " + str(self.p[customer]["bnap"]) + " \"" + "  /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show tcp conntable'| awk '/Current Intercepted/ {print $4}'" + "\""
    		arr_bnap_pss="ssh " + str(self.p[customer]["bnap"]) + " \"" + "  /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show arr nexus-fsm'| awk '/State/ {print $2}'" + "\""
    		total_hnap_pss="ssh " + str(self.p[customer]["hnap"]) + " \"" + "  /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show tcp conntable'| awk '/Total Intercepted/ {print $4}'" + "\""
    		current_hnap_pss="ssh " + str(self.p[customer]["hnap"]) + " \"" + " /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show tcp conntable'| awk '/Current Intercepted/ {print $4}'" + "\""
    		arr_hnap_pss="ssh " + str(self.p[customer]["hnap"]) + " \"" + " /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show arr nexus-fsm'| awk '/State/ {print $2}'" + "\""

    		self.file_handle.write('\n\n'+10*'-'+"SJC TAN_NI INFO"+10*'-'+'\n')
    		self.file_handle.flush()
    		temp=subprocess.Popen(str(arstatus_bpns), shell=True, stdout=PIPE).communicate()
            	self.writetofile2(temp)
    		self.file_handle.write('\n\n'+10*'-'+"SJC PAN_NI INFO"+10*'-'+'\n')
    		self.file_handle.flush()
    		temp=subprocess.Popen(str(arstatus_bpss), shell=True, stdout=PIPE).communicate()
            	self.writetofile2(temp)
    		self.file_handle.write('\n\n'+10*'-'+"SJC POP- TOTAL INTERCEPTED CONNECTIONS"+10*'-'+'\n')
    		self.file_handle.flush()
        	temp=subprocess.Popen(str(connections_bpop), shell=True, stdout=PIPE).communicate()
            	self.writetofile3(temp)
            	if self.p[customer]["bnap"]:
        		self.file_handle.write('\n\n'+10*'-'+"SJC ANAP- TOTAL INTERCEPTED CONNECTIONS"+10*'-'+'\n')
        		self.file_handle.flush()
        		temp=subprocess.Popen(str(total_bnap_pss), shell=True, stdout=PIPE).communicate()
                	self.writetofile3(temp)
                	self.file_handle.write('\n\n'+10*'-'+"SJC ANAP- CURRENT INTERCEPTED CONNECTIONS"+10*'-'+'\n')
                	self.file_handle.flush()
            	temp=subprocess.Popen(str(current_bnap_pss), shell=True, stdout=PIPE).communicate()
                	self.writetofile3(temp)
        		self.file_handle.write('\n\n'+10*'-'+"SJC ANAP ARR-NEXUS-FSM_STATE"+10*'-'+'\n')
        		self.file_handle.flush()
        		temp=subprocess.Popen(str(arr_bnap_pss), shell=True, stdout=PIPE).communicate()
                	self.writetofile3(temp)
        		self.file_handle.write('\n\n'+10*'-'+"BOM TAN_NI INFO"+10*'-'+'\n')
        		self.file_handle.flush()

    		temp=subprocess.Popen(str(arstatus_hpns), shell=True, stdout=PIPE).communicate()
            	self.writetofile2(temp)
    		self.file_handle.write('\n\n'+10*'-'+"BOM PAN_NI INFO"+10*'-'+'\n')
    		self.file_handle.flush()
    		temp=subprocess.Popen(str(arstatus_hpss), shell=True, stdout=PIPE).communicate()
            	self.writetofile2(temp)
    		self.file_handle.write('\n\n'+10*'-'+"BOM POP- TOTAL INTERCEPTED CONNECTIONS"+10*'-'+'\n')
    		self.file_handle.flush()
        	temp=subprocess.Popen(str(connections_hpop), shell=True, stdout=PIPE).communicate()
            	self.writetofile3(temp)
            	if self.p[customer]["hnap"]:
        		self.file_handle.write('\n\n'+10*'-'+"BOM ANAP- TOTAL INTERCEPTED CONNECTIONS"+10*'-'+'\n')
        		self.file_handle.flush()
        		temp=subprocess.Popen(str(total_hnap_pss), shell=True, stdout=PIPE).communicate()
                	self.writetofile3(temp)
                	self.file_handle.write('\n\n'+10*'-'+"BOM ANAP- CURRENT INTERCEPTED CONNECTIONS"+10*'-'+'\n')
                	self.file_handle.flush()
            	temp=subprocess.Popen(str(current_hnap_pss), shell=True, stdout=PIPE).communicate()
                	self.writetofile3(temp)
        		self.file_handle.write('\n\n'+10*'-'+"BOM ANAP ARR-NEXUS-FSM_STATE"+10*'-'+'\n')
        		self.file_handle.flush()
        		temp=subprocess.Popen(str(arr_hnap_pss), shell=True, stdout=PIPE).communicate()
                	self.writetofile3(temp)


		self.copyfiles(self.connect_customer)

        	cmd =  'tar cvzf pop.tgz ./asn_files/*controller* ./asn_files/*manager*  ./asn_files/*ipsec*'
        	subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()

            for customer in self.customerlist:
                cmd =  'tar cvzf %s.tgz ./asn_files/*%d* ./asn_files/*%d*' %(customer, self.p[customer]["ni"][0],self.p[customer]["ni"][1])
            	subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()

#---------------------------------------__init__ function-----------------------------------------------------
#	function called by afw_report.py
#	function identifies the ips and the nexus ids and exits

	def __init__(self, customer):
		now = datetime.datetime.now()
                self.file_name="/root/bkp/ASN_Report_Scripts/log/Live_POP_Report_" \
                                + str(now.year) + str(now.month) + str(now.day)+"-"+ \
                                str(now.hour) + str(now.minute) + ".log"
		self.file_name= os.path.join(os.getcwd(), 'log', self.file_name)
		self.file_handle=open(self.file_name,'a')
		self.log=aniLogging.aniLogging(str(self.file_name))
        self.pnslist['10.0.2.11','10.0.4.11']
        self.psslist['10.0.2.21','10.0.4.21']
        self.customerlist['aryaka','gluster']
		self.p=[{'aryaka':{'nexus_id':['579','554'],'bnap':['172.18.2.100'],'bpop':['10.0.2.11','10.0.2.21'],'hpop':['10.0.4.11','10.0.4.21'],'hnap':['172.19.2.191'] } \
		            {'gluster':{'nexus_id':['715','690'],'bnap':[0],'bpop':['10.0.2.11','10.0.2.21'],'hpop':['10.0.4.11','10.0.4.21'],'hnap':[0] }}}]



