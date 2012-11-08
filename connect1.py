#!/usr/bin/python
#
import os, os.path, sys, subprocess, datetime, time, logging, aniLogging, signal, re, string
from subprocess import PIPE
class afwConnect:
#---------------------------------------arlogcall function-----------------------------------------------------
# arlogcall connects to the live pop machines and re-applies the poutput and the filters


	def write2file(self,temp):
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
            t=""
            for j in range(0, len(col[0])):
##                print "row=",j
                for i in range(0,len(col)-1):
                   t=t+col[i][j]+(30-len(col[i][j]))*" "
                t=t+'\n'
            print t
	    self.file_handle.write(t)



	def arlogcall(self,option):

		ha_manager_str="  arlog -n ha_manager " +str(option)
		controller_str="  arlog -n controller "+str(option)
		ipsec_str="  arlog -n ipsec "+str(option)
               	self.pnsb_str= "ssh " + str(self.b_pop_pns) +" \"" + "  arlog -n pns"+str(self.b_nexus_id)+" " +str(option)+" \""
                self.pnsh_str="ssh " + str(self.h_pop_pns) + " \"" + "  arlog -n pns"+str(self.h_nexus_id)+" " +str(option)+" \""
                self.pssb_str="ssh " + str(self.b_pop_pss) + " \"" + " arlog -n pss"+str(self.b_nexus_id)+" " +str(option)+" \""
                self.pssh_str="ssh " + str(self.h_pop_pss) + " \"" + " arlog -n pss"+str(self.h_nexus_id)+" " +str(option)+" \""

                self.ha_man_b= "ssh " +  str(self.b_pop_pns) + " \"" + ha_manager_str +"\""
                self.ha_man_h="ssh " +  str(self.h_pop_pns) + " \"" + ha_manager_str +"\""
                self.control_bpns="ssh " +  str(self.b_pop_pns)+" \"" + controller_str +"\""
                self.control_hpns="ssh " +  str(self.h_pop_pns) +" \"" + controller_str +"\""
                self.control_bpss="ssh " +  str(self.b_pop_pss) +" \"" + controller_str +"\""
                self.control_hpss="ssh " +  str(self.h_pop_pss) +" \"" + controller_str +"\""
                self.ipsec_b="ssh " +  str(self.b_pop_pns) +" \"" + ipsec_str +"\""
                self.ipsec_h="ssh " +  str(self.h_pop_pns) +" \"" + ipsec_str +"\""

		print self.ha_man_b,"\n", self.ha_man_h,"\n", self.control_bpns,"\n", self.control_hpns,"\n",self.control_bpss,"\n", self.control_hpss,"\n", self.ipsec_b, "\n",self.ipsec_h,"\n", self.pnsb_str,"\n",self.pnsh_str, "\n",self.pssb_str ,"\n", self.pssh_str


		temp=subprocess.Popen(self.ha_man_b,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.ha_man_h,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.control_bpns,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.control_hpns,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.control_bpss,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.control_hpss,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.ipsec_b,  shell=True)
		temp.wait()
                temp=subprocess.Popen(self.ipsec_h,  shell=True)
		temp.wait()
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

#		self.pnsb_str= "ssh " + str(self.b_pop_pns) +" \"" + "  arlog -f warn -D"+str(self.b_nexus_id)+" -r\""



#---------------------------------------Connect function-----------------------------------------------------
# copyfiles connects to all tan and pan machines and collects the log files.
# log files are created by arlog running on each of those machines.
# copyfiles function, copies the files over and calls apply logs function

	def copyfiles(self,customer):
		bpop_pns_controller_log="scp root@" + str(self.b_pop_pns) +":/var/aryaka/controller/*_controller_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		bpop_pss_controller_log="scp root@" + str(self.b_pop_pss) +":/var/aryaka/controller/*_controller_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		hpop_pns_controller_log="scp root@" + str(self.h_pop_pns) +":/var/aryaka/controller/*_controller_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		hpop_pss_controller_log="scp root@" + str(self.h_pop_pss) +":/var/aryaka/controller/*_controller_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		bpop_pns_pns_log="scp root@" + str(self.b_pop_pns) +":/var/aryaka/nexus/pns_"+ str(self.b_nexus_id) +"/*_pns_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		hpop_pns_pns_log="scp root@" + str(self.h_pop_pns) +":/var/aryaka/nexus/pns_"+ str(self.h_nexus_id) +"/*_pns_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		bpop_pss_pss_log="scp root@" + str(self.b_pop_pss) +":/var/aryaka/nexus/pss_"+ str(self.b_nexus_id) +"/*_pss_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		hpop_pss_pss_log="scp root@" + str(self.h_pop_pss) +":/var/aryaka/nexus/pss_"+ str(self.h_nexus_id) +"/*_pss_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		bpop_pns_ha_manager_log="scp root@" + str(self.b_pop_pns) +":/var/aryaka/ha_manager/*_ha_manager_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		bpop_pns_ipsec_log="scp root@" + str(self.b_pop_pns) +":/var/aryaka/nexus/racoon/*_ipsec_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		hpop_pns_ha_manager_log="scp root@" + str(self.h_pop_pns) +":/var/aryaka/ha_manager/*_ha_manager_*.log /root/bkp/ASN_Report_Scripts/asn_files/"
		hpop_pns_ipsec_log="scp root@" + str(self.h_pop_pns) +":/var/aryaka/nexus/racoon/*_ipsec_*.log /root/bkp/ASN_Report_Scripts/asn_files/"

		bpop_pns_controller_log_del="ssh root@" + str(self.b_pop_pns) +" mv /var/aryaka/controller/*_controller_*.log /tmp/"
		bpop_pss_controller_log_del="ssh root@" +str(self.b_pop_pss) +" mv /var/aryaka/controller/*_controller_*.log /tmp/"
		hpop_pns_controller_log_del="ssh root@" +str(self.h_pop_pns)+" mv /var/aryaka/controller/*_controller_*.log /tmp/"
		hpop_pss_controller_log_del="ssh root@" +str(self.h_pop_pss) +" mv /var/aryaka/controller/*_controller_*.log /tmp/"
		bpop_pns_pns_log_del="ssh root@" + str(self.b_pop_pns) +" mv /var/aryaka/nexus/pns_"+ str(self.b_nexus_id) +"/*_pns_*.log /tmp/"
		bpop_pss_pss_log_del="ssh root@" +  str(self.h_pop_pss) +" mv /var/aryaka/nexus/pss_"+ str(self.h_nexus_id) +"/*_pss_*.log /tmp/"
		bpop_pns_ha_manager_log_del="ssh root@" + str(self.b_pop_pns) +" mv /var/aryaka/ha_manager/*_ha_manager_*.log  /tmp/"
		bpop_pns_ipsec_log_del="ssh root@" + str(self.b_pop_pns) +" mv /var/aryaka/nexus/racoon/*_ipsec_*.log /tmp/"
		hpop_pns_ha_manager_log_del="ssh root@" +  str(self.h_pop_pns) +" mv /var/aryaka/ha_manager/*_ha_manager_*.log /tmp/"
		hpop_pns_ipsec_log_del="ssh root@" + str(self.h_pop_pns) +" mv /var/aryaka/nexus/racoon/*_ipsec_*.log /tmp/"


		print "Copying ", bpop_pns_controller_log, "...."
		temp=subprocess.Popen(str(bpop_pns_controller_log), shell=True, stdout=self.file_handle)
		temp.wait()
		print "Copying ",bpop_pss_controller_log, "...."
		temp=subprocess.Popen(str(bpop_pss_controller_log), shell=True, stdout=self.file_handle)
		temp.wait()
		print "Copying ",hpop_pns_controller_log, "...."
		temp=subprocess.Popen(str(hpop_pns_controller_log), shell=True, stdout=self.file_handle)
		temp.wait()
		print "Copying ",hpop_pss_controller_log, "...."
		temp=subprocess.Popen(str(hpop_pss_controller_log), shell=True, stdout=self.file_handle)
		temp.wait()
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
		print "Copying ",bpop_pns_ha_manager_log, "...."
		temp=subprocess.Popen(str(bpop_pns_ha_manager_log), shell=True, stdout=self.file_handle)
		temp.wait()
		print "Copying ",bpop_pns_ipsec_log, "...."
		temp=subprocess.Popen(str(bpop_pns_ipsec_log), shell=True, stdout=self.file_handle)
		temp.wait()
		print "Copying ",hpop_pns_ha_manager_log, "...."
		temp=subprocess.Popen(str(hpop_pns_ha_manager_log), shell=True, stdout=self.file_handle)
		temp.wait()
		print "Copying ",hpop_pns_ipsec_log, "...."
		temp=subprocess.Popen(str(hpop_pns_ipsec_log), shell=True, stdout=self.file_handle)
		temp.wait()

		temp=subprocess.Popen(str(bpop_pns_controller_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(bpop_pss_controller_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(hpop_pns_controller_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(hpop_pss_controller_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(bpop_pns_pns_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(bpop_pss_pss_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(bpop_pns_ha_manager_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(bpop_pns_ipsec_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(hpop_pns_ha_manager_log_del), shell=True)
		temp.wait()
		temp=subprocess.Popen(str(hpop_pns_ipsec_log_del), shell=True)
		temp.wait()



		self.applylog()

#---------------------------------------Connect function-----------------------------------------------------
# Connect function is called by afw_report after __init__ is called.
# This function connects to the pops and collects cli information
# After collecting cli information, it calls copyfiles function to collect the log files

	def Connect(self):

		nexus_string=' nxctl status'
		connect_string_bpns="ssh " + str(self.b_pop_pns) + nexus_string
		connect_string_hpns="ssh " + str(self.h_pop_pns) + nexus_string
		connections_hpop="ssh " + str(self.h_pop_pss) + " \""+ " asn_cli.py -n pss_"+str(self.h_nexus_id)+" -c 'show tcp conntable'| awk '/Total Intercepted/ {print $4}'" +"\""
		connections_bpop="ssh " + str(self.b_pop_pss) + " \"" + " asn_cli.py -n pss_"+str(self.b_nexus_id)+" -c 'show tcp conntable'| awk '/Total Intercepted/ {print $4}'" +"\""
		arstatus_bpns="ssh " + str(self.b_pop_pns) + " \"" + " arstatus -t " + str(self.b_nexus_id) + "\""
		arstatus_hpns="ssh " + str(self.h_pop_pns) + " \"" + " arstatus -t " + str(self.h_nexus_id) + "\""
		arstatus_bpss="ssh " + str(self.b_pop_pns) + " \"" + " arstatus -p " + str(self.b_nexus_id) + "\""
		arstatus_hpss="ssh " + str(self.h_pop_pns) + " \"" + " arstatus -p " + str(self.h_nexus_id) + "\""
		arstatus_bipsec="ssh " + str(self.b_pop_pns) + " \"" + " arstatus -i "+ "\""
		arstatus_hipsec="ssh " + str(self.h_pop_pns) + " \"" + " arstatus -i "  + "\""
		total_bnap_pss="ssh " + str(self.b_nap_ip) + " \"" + " /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show tcp conntable'| awk '/Total Intercepted/ {print $4}'" + "\""
		current_bnap_pss="ssh " + str(self.b_nap_ip) + " \"" + "  /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show tcp conntable'| awk '/Current Intercepted/ {print $4}'" + "\""
		arr_bnap_pss="ssh " + str(self.b_nap_ip) + " \"" + "  /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show arr nexus-fsm'| awk '/State/ {print $2}'" + "\""
		total_hnap_pss="ssh " + str(self.h_nap_ip) + " \"" + "  /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show tcp conntable'| awk '/Total Intercepted/ {print $4}'" + "\""
		current_hnap_pss="ssh " + str(self.h_nap_ip) + " \"" + " /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show tcp conntable'| awk '/Current Intercepted/ {print $4}'" + "\""
		arr_hnap_pss="ssh " + str(self.h_nap_ip) + " \"" + " /opt/aryaka/asn/scripts/asn_cli.py -n pss " + " -c 'show arr nexus-fsm'| awk '/State/ {print $2}'" + "\""

#		self.log.WriteLog('info',"LIVE ARYAKA POP REPORT\n")
#		self.log.WriteLog('info', "SJC POP INFO ")
		self.file_handle.write('\n'+20*'#'+"SJC POP INFO "+20*'#'+'\n')
		temp=subprocess.Popen(str(connect_string_bpns), shell=True, stdout=self.file_handle)
		temp.wait()
#		self.log.WriteLog('info','SJC TAN_NI INFO')
		self.file_handle.write('\n'+10*'-'+"SJC TAN_NI INFO"+10*'-'+'\n')
		temp=subprocess.Popen(str(arstatus_bpns), shell=True, stdout=PIPE).communicate()
        	self.writetofile2(temp)
#		self.log.WriteLog('info','SJC PAN_NI INFO')
		self.file_handle.write('\n'+10*'-'+"SJC PAN_NI INFO"+10*'-'+'\n')
		temp=subprocess.Popen(str(arstatus_bpss), shell=True, stdout=PIPE).communicate()
        	self.writetofile2(temp)
#		self.log.WriteLog('info','SJC IPSEC INFO')
		self.file_handle.write('\n'+10*'-'+'SJC IPSEC INFO'+10*'-'+'\n')
		temp=subprocess.Popen(str(arstatus_bipsec), shell=True, stdout=self.file_handle)
        	temp.wait()
#		self.log.WriteLog('info',"MUM POP INFO ")
		self.file_handle.write('\n'+20*'#'+"MUM POP INFO "+20*'#'+'\n')
		temp=subprocess.Popen(str(connect_string_hpns), shell=True, stdout=self.file_handle)
	        temp.wait()
#               self.log.WriteLog('info','MUM TAN_NI INFO')
                self.file_handle.write('\n'+10*'-'+"MUM TAN_NI INFO"+10*'-'+'\n')
                temp=subprocess.Popen(str(arstatus_hpns), shell=True, stdout=PIPE).communicate()
        	self.writetofile2(temp)
#                self.log.WriteLog('info','MUM PAN_NI INFO')
                self.file_handle.write('\n'+10*'-'+"SJC PAN_NI INFO"+10*'-'+'\n')
                temp=subprocess.Popen(str(arstatus_hpss), shell=True, stdout=PIPE).communicate()
        	self.writetofile2(temp)
#                self.log.WriteLog('info','MUM IPSEC INFO')
                self.file_handle.write('\n'+10*'-'+"SJC MUM IPSEC INFO"+10*'-'+'\n')
                temp=subprocess.Popen(str(arstatus_hipsec), shell=True, stdout=self.file_handle)
		temp.wait()
      

##		self.log.WriteLog('info',"LIVE ARYAKA POP REPORT\n")
##		self.log.WriteLog('info', "SJC POP INFO ")
##		temp=subprocess.Popen(str(connect_string_bpns), shell=True, stdout=self.file_handle)
##		temp.wait()
##		self.log.WriteLog('info','SJC TAN_NI INFO')
##		temp=subprocess.Popen(str(arstatus_bpns), shell=True, stdout=self.file_handle)
##		temp.wait()
##		self.log.WriteLog('info','SJC PAN_NI INFO')
##		temp=subprocess.Popen(str(arstatus_bpss), shell=True, stdout=self.file_handle)
##		temp.wait()
##		self.log.WriteLog('info','SJC IPSEC INFO')
##		temp=subprocess.Popen(str(arstatus_bipsec), shell=True, stdout=self.file_handle)
##		temp.wait()
##		self.log.WriteLog('info',"MUM POP INFO ")
##		temp=subprocess.Popen(str(connect_string_hpns), shell=True, stdout=self.file_handle)
##		temp.wait()
##                self.log.WriteLog('info','MUM TAN_NI INFO')
##                temp=subprocess.Popen(str(arstatus_hpns), shell=True, stdout=self.file_handle)
##                temp.wait()
##                self.log.WriteLog('info','MUM PAN_NI INFO')
##                temp=subprocess.Popen(str(arstatus_hpss), shell=True, stdout=self.file_handle)
##                temp.wait()
##                self.log.WriteLog('info','MUM IPSEC INFO')
##                temp=subprocess.Popen(str(arstatus_hipsec), shell=True, stdout=self.file_handle)
##                temp.wait()
##		self.log.WriteLog('info',"@anap.sjc1")
		temp=subprocess.Popen(str(total_bnap_pss), shell=True, stdout=self.file_handle)
		temp.wait()
		temp=subprocess.Popen(str(current_bnap_pss), shell=True, stdout=self.file_handle)
		temp.wait()
		temp=subprocess.Popen(str(arr_bnap_pss), shell=True, stdout=self.file_handle)
		temp.wait()
##		self.log.WriteLog('info',"@anap.mum1")#'s data not collected because connectivity not available")
		temp=subprocess.Popen(str(total_hnap_pss), shell=True, stdout=self.file_handle)
		temp.wait()
		temp=subprocess.Popen(str(current_hnap_pss), shell=True, stdout=self.file_handle)
		temp.wait()
		temp=subprocess.Popen(str(arr_hnap_pss), shell=True, stdout=self.file_handle)
		temp.wait()
		self.copyfiles(self.connect_customer)

        	cmd =  'tar cvzf pop.tgz ./asn_files/*controller* ./asn_files/*manager*  ./asn_files/*ipsec*'
        	subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()

        	cmd =  'tar cvzf %s.tgz ./asn_files/*%d* ./asn_files/*%d*' %(self.connect_customer, self.b_nexus_id,self.h_nexus_id)
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
#		self.log=aniLogging.aniLogging(str(self.file_name))
		self.connect_customer =customer
##                self.b_nexus_id=579
##                self.h_nexus_id=554

		if self.connect_customer=='aryaka':
			self.b_nexus_id=579
			self.h_nexus_id=554
		elif self.connect_customer=='gluster':
			self.b_nexus_id=715
			self.h_nexus_id=690
		self.b_pop_pns='10.0.2.11'
		self.b_pop_pss='10.0.2.21'
		self.h_pop_pns='10.0.4.11'
		self.h_pop_pss='10.0.4.21'
		self.b_nap_ip='172.18.2.100'
		self.h_nap_ip='172.19.2.191'

