# All of the functions needed to run server.py

import socket, sys, threading, subprocess
import settings

settings.init()

def server_loop():

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#if no settings.target is defined, listen on all interfaces
	if settings.target == None:
	   settings.target = "0.0.0.0"

	server.bind((settings.target,settings.port))
	server.listen(5)
	print "[*] Listening on %s:%d" % (settings.target, settings.port)

	while True:
		client_socket, addr = server.accept()

		#thread to handle client
		client_thread = threading.Thread(target=client_handler, args=(client_socket,))
		client_thread.start()

		print "listening..."
		print settings.port
		if settings.command == True:
			print "commanding..."

def client_handler(client_socket):

	#check for upload dest
	if len(settings.upload_destination):

		#read all of the bytes, write to dest
		file_buffer = ""

		#receive until all data is read
		while True:
			data = client_socket.recv(1024)

			if data == None:
				break
			else:
				file_buffer += data

		#take data and try to write it out
		try:
			file_writer = open(settings.upload_destination,"w")
			file_writer.write(file_buffer)
			file_writer.close()

			#acknowledge file was written
			client_socket.send("Successfully saved file to %s\r\n" % settings.upload_destination)
		except:
			client_socket.send("Failed to save file to %s\r\n" % settings.upload_destination)

	#command to execute
	if len(settings.execute):
		
		#run command
		output = run_command(settings.execute)

		client_socket.send(output)

	#loop if command shell is requested
	if settings.command:

		while True:
			#prompt
			client_socket.send("<SHELL:#>")

			#receive until new line received
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)
			  
			#gather command output
			response = run_command(cmd_buffer)
			
			#send response
			client_socket.send(response)                 

def client_sender(buffer):

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

						   
	try:
		client.connect((settings.target,settings.port))
		print "Connected"
		
		if len(buffer):
			client.send(buffer)
			
		while True:
			
			recv_len = 1
			response = ""
			
			while recv_len:
				
				data = client.recv(4096)
				recv_len = len(data)
				response += data
				
				if recv_len < 4096:
					break
					
			print response,
			
			buffer = raw_input("")
			buffer += "\n"
			
			client.send(buffer)
			
	except:
		
		print "[*] Exception! Exiting."
		
		client.close()

def run_command(command):
	#trim the newline
	command = command.rstrip()

	#run the command and get the output back
	try:
		output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
	except:
		output = "Failed to execute command.\r\n"

	#send the output back to the client
	return output

