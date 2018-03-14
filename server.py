# TODO server listens on localhost:port
# TODO client handler, accept connection and receive data
# TODO client sender, send buffer over socket connection
# TODO run command, send commands to CLIENT over socket NOT SERVER

import socket, sys, argparse, threading, subprocess, getopt
from server import serv_mod
import settings

def usage():

    print "Usage: netcat.py -t target_host -p port"
    print "-l --listen  			- listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run - execute given file upon receiving a connection"
    print "-c --command				- initialize a command shell"
    print "-u --upload-destination	- upon receiving connection upload file"

    print
    print
    print "Examples: "
    print "netcat.py -t 192.168.0.1 -p SSSS -l -c"
    print "netcat.py -t 192.168.0.1 -p SSSS -l -u=c:\\target.exe"
    print "netcat.py -t 192.168.0.1 -p SSSS -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./netcat.py -t 192.168.11.12 -p 135"
    sys.exit(0)

def main():

	if not len(sys.argv[1:]):
		usage()
	
	#read the commandline options
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help",
															   "listen",
															   "execute",
															   "target",
															   "port",
															   "command",
															   "upload"])
	except getopt.GetoptError as err:
		print str(err)
		usage()
	
	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in ("-l","--listen"):
			settings.listen = True
		elif o in ("-e","--execute"):
			settings.execute = a
		elif o in ("-c","--command"):
			settings.command = True
		elif o in ("-u","--upload"):
			settings.upload_destination = a
		elif o in ("-t","--target"):
			settings.target = a
		elif o in ("-p","--port"):
			settings.port = int(a)
		else:
			assert False,"Unhandled Option"
	
	if not settings.listen and len(settings.target) and settings.port > 0:
		
		print "Reaching out to %s:%d" % (settings.target, settings.port)
		
		buffer = sys.stdin.read()
			
		serv_mod.client_sender(buffer)	
		
	if settings.listen:
		serv_mod.server_loop()

main()
