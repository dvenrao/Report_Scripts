#!/usr/bin/python
import logging, os, datetime
class aniLogging:
	def __init__(self,gv):

		#now=datetime.datetime.now()
		# set up logging to file - see previous section for more details
		logging.basicConfig(level=logging.DEBUG,
	        	            format='%(name)-12s: %(levelname)-8s %(message)s',
	                	    datefmt='%m-%d %H:%M',
		                    filename=str(gv),
		                    filemode='a')
		# define a Handler which writes INFO messages or higher to the sys.stderr
		console = logging.StreamHandler()
		console.setLevel(logging.INFO)
		# set a format which is simpler for console use
		formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
		# tell the handler to use this format
		console.setFormatter(formatter)
		# add the handler to the root logger
		logging.getLogger('').addHandler(console)
	def WriteLog(self, LogMode, LogText):
		# Now, we can log to the root logger, or any other logger. First the root...
		logger1 = logging.getLogger('TestLogger')
		if LogMode == 'debug':
			logger1.debug(LogText)
		elif LogMode == 'info':
			logger1.info(LogText)
		elif LogMode == 'warning':
			logger1.warning(LogText)
		elif LogMode == 'error':
			logger1.error(LogText)
		else:
			print "Wrong Option"
	
