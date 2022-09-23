#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def handleClient(s, conn, addr):
    payload = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)

    full_data = b""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sGoogle:
        remote_ip = get_remote_ip("www.google.com")

        sGoogle.connect((remote_ip, 80))
        
        #send the data and shutdown
        send_data(sGoogle, payload)
        sGoogle.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        while True:
            data = sGoogle.recv(4096)
            if not data:
                break
            full_data += data

    conn.send(full_data)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            process = Process(target=handleClient, args=(s, conn, addr))
            process.start()
            print("Connected by", addr)
            conn.close()

if __name__ == "__main__":
    main()
