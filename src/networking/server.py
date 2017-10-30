import os
import socket
import sys
import threading

BUFF_SIZE = 1500


def main():
    clients = {}

    port_num = get_input("Port: ")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', int(port_num)))
    server_socket.listen(5)

    while (True):
        # address is a tuple: (IP, port). I'm using the port to identify 
	# each client because the IP address
        # of two clients could be the same if they are run from the same machine
        (client_socket, address) = server_socket.accept()
        add_client(client_socket, address, clients)


# Supported commands:
# exit: This will quit the connection, removing the client
# list: This will send a list of client ids to the client
# xxxxx message: This will sent the message to client with id matching xxxxx
def client_handler(address, clients):
    sock = clients[address]

    while True:
        encodedmsg = sock.recv(BUFF_SIZE)
        msg = encodedmsg.decode('utf-8')

        print(str(address[1]) + ": " + msg)
        if msg[:3] == "emo":
            send_to_client(address, clients, msg)
        elif msg[3:7] == "exit" or not msg: break
        elif msg[3:7] == "list":
            send_client_list(sock, address, clients)
        else:
            send_to_client(address, clients, msg)

    sock.close()
    clients.pop(address, None)
    print(str(address[1]) + ": connect closed")


# Sends message to specific client
def send_to_client(address, clients, msg):
    found_client = False
    for client in clients.keys():
        if str(msg[3:8]) == str(client[1]):
            clients[client].send((msg[:3] + msg[8:]).encode('utf-8'))
            found_client = True
    if not found_client:
        clients[address].send(("Client not found: " + str(msg[:7])).encode('utf-8'))


# Sends list of all client ids(ports) to the socket
def send_client_list(sock, address, clients):
    send_msg = ""
    for client in clients:
        print("send list to client " + str(client[1]))
        if address[1] == client[1]: continue;  # Don't add itself
        send_msg += ("lst" + str(client[1]) + '\n')
        print(send_msg)
    sock.send(send_msg.encode('utf-8'))


# Searches through clients for matching id
# Returns id if found, empty string if not found
def get_client(clients, client_id):
    for client in clients:
        if str(client_id) == str(client[1]):
            return client
    return ""


# Add client to dictionary and start new thread to handle it
def add_client(client_socket, address, clients):
    # Start thread to handle client
    clients[address] = client_socket
    print(str(address[1]) + ": connected")
    t = threading.Thread(target=client_handler,
        args=(address, clients))
    t.daemon = True
    t.start()


# Get and return user input from stdout
def get_input(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()
    input = sys.stdin.readline()
    return input


if __name__ == "__main__":
    main()

