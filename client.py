#client
import socket
import sys

#Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 20000)
message = 'This is the message. It will be repeated.'

while True:
	print >>sys.stderr, 'Please enter a message: '
	msg = raw_input()
	
	if msg == 'Exit':
		print >>sys.stderr, 'Goodbye'
		sock.close()
		break
	else:
		#send data
		print >>sys.stderr, 'sending "%s"' % msg
		sent = sock.sendto(msg, server_address)

		#receive response
		print >>sys.stderr, 'waiting for receive'
		data, server = sock.recvfrom (4096)
		print >>sys.stderr, 'received "%s"' % data

