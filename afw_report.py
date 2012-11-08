#!/usr/bin/python
from optparse import OptionParser
from connect import afwConnect
import os, os.path, sys, time
from afwEmail import afwEmail #email module
from pingreport import *
import time
def main(verbose = False):
	print "Collecting Live POP info..... "
	usage = "%prog [options] [<mnemonic|*> [<mnemonic>] ...]"
	typeChoice =('aryaka', 'gluster')
	parser = OptionParser(usage = usage)
        parser.add_option("-v", action = "store_true", dest = "verbose", \
		default = True, help = "Verbose mode")
        parser.add_option("-c",  dest = "customer",type='choice', choices=typeChoice, help = "Choose a customer choose 'aryaka' for Aryaka and 'gluster' for gluster")
        #parser.add_option("-g", action = "store_true", dest = "gluster", \
        #        default = False, help = "Verbose mode")
	(options, args) = parser.parse_args()
#	customer =options.customer
#        customer_list=['aryaka','gluster']
#        for customer in customer_list:
        tmp = afwConnect()
        tmp.Connect()
#	tmp.applylog()

if __name__ == "__main__": 
        main()
#	Ping_Report()
#	time.sleep(60)
#        obj = afwEmail()
#        obj.send_mail()


