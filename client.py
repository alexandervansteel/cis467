import keras
import socket
import threading
import sys
import os
import signal

BUFF_SIZE = 1500

class Quit(Exception):
    pass


class Killed(Exception):
    pass


def exit_signal(signal, frame):
    raise Quit


def killed_signal(signal, frame):
    raise Killed


def main():
    value = True
    while value:
        server_ip = get_input("IP: ")
        port_num = get_input("Port: ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, int(port_num)))
        signal.signal(signal.SIGUSR1, exit_signal)
        signal.signal(signal.SIGUSR2, killed_signal)

        messaging = threading.Thread(target=server_handler, args=(s,))
        messaging.daemon = True
        messaging.start()

        try:
            while True:
                msg = get_input("[]$ ")
                s.send(("msg" + msg).encode('utf-8'))
                # this output goes to UI to be printed

                if msg[3:7] == "exit" or not msg:
                    os.kill(os.getpid(), signal.SIGUSR1)

        except Quit:
            value = False
        except Killed:
            pass
        finally:
            s.close()

def server_handler(sock):
    while True:
        encodedmsg = sock.recv(BUFF_SIZE)
        msg = encodedmsg.decode('utf-8')
        if msg[:3] == 'msg':
            print('\n' + msg[3:])
            sys.stdout.flush()
            sys.stdout.write("[]$ ")
            sys.stdout.flush()
            # this output goes to UI to be printed

        if msg[:3] == 'lst':
            print('\n' + msg[3:])
            sys.stdout.flush()
            sys.stdout.write("[]$ ")
            sys.stdout.flush()

        if msg[:3] == 'emo':
            # interface with the UI to display image
            print("emo: " + msg)

        if msg[3:7] == "exit":
            sock.send(("msg" + msg).encode('utf-8'))
            print('\n')
            os.kill(os.getpid(), signal.SIGUSR2)
            return

        
def get_input(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()
    input = sys.stdin.readline()
    return input

if __name__ == "__main__":
    main()
