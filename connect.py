#!/usr/bin/python
#
import os, os.path, sys, subprocess, datetime, time, logging, aniLogging, signal, re, string, ignore_list
from subprocess import PIPE
class afwConnect:
#---------------------------------------arlogcall function-----------------------------------------------------
# arlogcall connects to the live pop machines and re-applies the poutput and the filters

	def Connect(self):

		nexus_string=' nxctl status'


                for loc in self.loclist:
                        for pop in ['pns', 'pss']:
                        	for i in ignore_list.ignlist:
                                   cmd = 'grep -v %s ./asn_files/controller_%s_%s.log > ./asn_files/controller1_%s_%s.log'%(i,loc,pop,loc,pop)
                                   subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()        
                                   cmd = 'cat ./asn_files/controller1_%s_%s.log > ./asn_files/controller_%s_%s.log'%(loc,pop,loc,pop)
                                   subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()
                                   cmd = 'grep -v %s ./asn_files/ha_manager_%s_%s.log > ./asn_files/ha_manager1_%s_%s.log'%(i,loc,pop,loc,pop)
                                   subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()
                                   cmd = 'cat ./asn_files/ha_manager1_%s_%s.log > ./asn_files/ha_manager_%s_%s.log'%(loc,pop,loc,pop)
                                   subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()
                        for i in ignore_list.ignlist:
                             cmd = 'grep -v %s ./asn_files/ipsec_%s.log > ./asn_files/ipsec1_%s.log'%(i,loc,loc)
                             subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()
                             cmd = 'cat ./asn_files/ipsec1_%s.log > ./asn_files/ipsec_%s.log'%(loc,loc)
                             subprocess.Popen(cmd, shell=True, cwd='/root/bkp/ASN_Report_Scripts').communicate()



                        

#---------------------------------------__init__ function-----------------------------------------------------
#	function called by afw_report.py
#	function identifies the ips and the nexus ids and exits

	def __init__(self):
		now = datetime.datetime.now()
                self.file_name="/root/bkp/ASN_Report_Scripts/log/Live_POP_Report_" \
                                + str(now.year) + str(now.month) + str(now.day)+"-"+ \
                                str(now.hour) + str(now.minute) + ".log"
		self.file_name= os.path.join(os.getcwd(), 'log', self.file_name)
		self.file_handle=open(self.file_name,'a')
		self.log=aniLogging.aniLogging(str(self.file_name))
                self.pnslist=['10.0.2.11','10.0.3.11','10.0.4.11','10.0.5.11','10.0.6.11','10.0.7.11' \
                ,'10.0.8.11','10.0.9.11','10.0.10.11','10.0.11.11','10.0.12.11','10.0.13.11','10.0.14.11']
                self.psslist=['10.0.2.21','10.0.3.21','10.0.4.21','10.0.5.21','10.0.6.21','10.0.7.21' \
                ,'10.0.8.21','10.0.9.21','10.0.10.21','10.0.11.21','10.0.12.21','10.0.13.21','10.0.14.21']
                self.loclist=['sjc3']
                self.ip2loc={'10.0.12.11':'sjc3'}
                self.customerlist=['aryaka','gluster','massivedynamics','tavant' \
                ,'rallp','globallogic','unstudio','cloud','accept360','trident','symphony','appliedmicro','bendpak','allianceglobal','keane']
                self.p={'aryaka':{'ni':['4553','4519'],'bnap':0,'bpop':['10.0.12.11','10.0.12.22'],'hpop':['10.0.5.11','10.0.5.21'],'hnap':0 } \
                ,'gluster':{'ni':['715','690'],'bnap':0,'bpop':['10.0.12.11','10.0.12.21'],'hpop':['10.0.7.11','10.0.7.21'],'hnap':0 } \
                ,'massivedynamics':{'ni':['3735','3791'],'bnap':0,'bpop':['10.0.6.11','10.0.6.21'],'hpop':['10.0.4.11','10.0.4.21'],'hnap':0 } \
                ,'tavant':{'ni':['1575','1657'],'bnap':0,'bpop':['10.0.2.11','10.0.2.21'],'hpop':['10.0.5.11','10.0.5.21'],'hnap':0 } \
                ,'rallp':{'ni':['997','1516'],'bnap':0,'bpop':['10.0.12.11','10.0.12.21'],'hpop':['10.0.7.11','10.0.7.21'],'hnap':0 } \
                ,'globallogic':{'ni':['3735','3791'],'bnap':0,'bpop':['10.0.6.11','10.0.6.21'],'hpop':['10.0.4.11','10.0.4.21'],'hnap':0 } \
                ,'unstudio':{'ni':['2945','3394'],'bnap':0,'bpop':['10.0.13.11','10.0.13.21'],'hpop':['10.0.9.11','10.0.9.21'],'hnap':0 } \
                ,'cloud':{'ni':['2148','2212'],'bnap':0,'bpop':['10.0.12.11','10.0.12.21'],'hpop':['10.0.7.11','10.0.7.21'],'hnap':0 } \
                ,'accept360':{'ni':['4265','4299'],'bnap':0,'bpop':['10.0.12.11','10.0.12.21'],'hpop':['10.0.7.11','10.0.7.21'],'hnap':0 } \
                ,'trident':{'ni':['4765','4799'],'bnap':0,'bpop':['10.0.7.11','10.0.7.21'],'hpop':['10.0.12.11','10.0.12.21'],'hnap':0 } \
                ,'symphony':{'ni':['6647','6681'],'bnap':0,'bpop':['10.0.12.11','10.0.12.21'],'hpop':['10.0.5.11','10.0.5.22'],'hnap':0 } \
                ,'appliedmicro':{'ni':['6805','6839'],'bnap':0,'bpop':['10.0.7.11','10.0.7.21'],'hpop':['10.0.12.11','10.0.12.22'],'hnap':0 } \
                ,'bendpak':{'ni':['6884','6920'],'bnap':0,'bpop':['10.0.12.11','10.0.12.21'],'hpop':['10.0.9.11','10.0.9.21'],'hnap':0 } \
                ,'allianceglobal':{'ni':['7054','7021'],'bnap':0,'bpop':['10.0.11.11','10.0.11.22'],'hpop':['10.0.5.11','10.0.5.22'],'hnap':0 } \
                ,'keane':{'ni':['7211','7244'],'bnap':0,'bpop':['10.0.11.11','10.0.11.22'],'hpop':['10.0.5.11','10.0.5.22'],'hnap':0 } \
                }
                #self.ignorelist=['997','6839','1424']
                #self.ignorelist=['1424','997','1424','6839']
 
