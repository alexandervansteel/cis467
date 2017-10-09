#Server

import socket
import sys

#Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#bind socket to the port
server_address = ('localhost', 20000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
	print >>sys.stderr, 'Send a message: '
	msg = raw_input()
	data, address = sock.recvfrom(4096)
	
	#print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
	print >>sys.stderr, 'Received: %s' % data

	if msg:
		sent = sock.sendto(msg, address)
		#print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address) 
