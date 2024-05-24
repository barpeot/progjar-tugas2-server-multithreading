from socket import *
import socket
import threading
import logging
from time import gmtime, strftime
import sys

def timeFunc(self):
        message = str("JAM ") + strftime("%H:%M:%S",gmtime()) + str("\r\n")
        self.connection.sendall(message.encode())

def quitFunc(self):
        message = "QUIT MESSAGE BERHASIL DITERIMA\n"
        self.connection.sendall(message.encode())

def unknownFunc(self):
        message = "WARNING: COMMAND TIDAK DIKENAL\n"
        self.connection.sendall(message.encode())

class ProcessTheClient(threading.Thread):
        def __init__(self,connection,address):
                self.connection = connection
                self.address = address
                threading.Thread.__init__(self)

        def run(self):
                while True:
                        try:
                                data = self.connection.recv(32)
                                if data:
                                        d = data.decode().strip()
                                        logging.warning(f"data adalah {d} dari client {self.address}.")
                                        if d[-4:]=='TIME':
                                                logging.warning(f"mendapatkan command TIME dari client {self.address}.")
                                                timeFunc(self)
 
                                        elif d[-4:]=='QUIT':
                                                logging.warning(f"mendapatkan command QUIT dari client {self.address}.")
                                                quitFunc(self)
                                                self.connection.close()
                                        
                                        else:
                                                logging.warning(f"command {d} dari client {self.address} tidak dikenal!")
                                                unknownFunc(self)
                                else:
                                        break
                        except OSError as e:
                                pass
                self.connection.close()

class Server(threading.Thread):
        def __init__(self):
                self.the_clients = []
                self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                threading.Thread.__init__(self)

        def run(self):
                self.my_socket.bind(('0.0.0.0',45000))
                self.my_socket.listen(1)
                while True:
                        self.connection, self.client_address = self.my_socket.accept()
                        logging.warning(f"connection from {self.client_address}")

                        clt = ProcessTheClient(self.connection, self.client_address)
                        clt.start()
                        self.the_clients.append(clt)
                        
def main():
        svr = Server()
        svr.start()

if __name__=="__main__":
        main()

