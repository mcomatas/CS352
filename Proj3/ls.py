# Authors:
# Michael Comatas (netID: mac776)
# Umar Khattak (netID: uk50)

import threading
import random
import socket as mysoc
import sys 
import select

import argparse
from sys import argv
# import socket


# server task
def server():
    #argsv::    
    input_sys = sys.argv
    lsListenPort = int(input_sys[1])
    ts1_hostname = (input_sys[2])
    ts1_listenPort = int(input_sys[3])
    ts2_hostname = (input_sys[4])
    ts2_listenPort = int(input_sys[5])


    try:
        clientSocket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created for client")
    except mysoc.error as err:
        print('{} \n'.format("client socket open error ",err))
    #connection with client:
    server_binding=('',lsListenPort)

    clientSocket.bind(server_binding)
    clientSocket.listen(10)
    
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
 
    csockid,addr=clientSocket.accept()
    print ("[S]: Got a connection request from a client at", addr)


    try:
        ts1_Socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created for ts1")
    except mysoc.error as err:
        print('{} \n'.format("ts1 socket open error ",err))

    #connections with ts1:
    
    host_ts1=mysoc.gethostbyname(ts1_hostname)
    server_binding_ts1=(host_ts1,ts1_listenPort)
    ts1_Socket.connect(server_binding_ts1)   
    ts1_Socket.settimeout(5)

    try:
        ts2_Socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created for ts2")
    except mysoc.error as err:
        print('{} \n'.format("ts2 socket open error ",err))    

    host_ts2=mysoc.gethostbyname(ts2_hostname)
    server_binding_ts2=(host_ts2,ts2_listenPort)
    ts2_Socket.connect(server_binding_ts2)
    ts2_Socket.settimeout(5)

    ts = 1 # set initial ts server to send to to 1 before the loop
    dict_ts1 = {} # set dicts to be blank initally before the loop
    dict_ts2 = {}

    while True:
        queryFromClient = csockid.recv(1024).decode('utf-8')       
        if not queryFromClient:     # if data is not received break
            break
        
        queryFromClient = queryFromClient.rstrip().lower()

        print("Received from client: " + str(queryFromClient))

        received_msg=""
    
        if queryFromClient in dict_ts1.keys():
            ts1_Socket.sendall(queryFromClient.encode('utf-8'))
            received_msg = ts1_Socket.recv(1024)
        elif queryFromClient in dict_ts2.keys():
            ts2_Socket.sendall(queryFromClient.encode('utf-8'))
            received_msg = ts1_Socket.recv(1024)
        else:
            if ts == 1:
                # send to ts1
                dict_ts1[queryFromClient] = 'ts1' # put the query Key in the dict for ts1
                ts1_Socket.sendall(queryFromClient.encode('utf-8'))
                received_msg = ts1_Socket.recv(1024)
                ts = 2
            elif ts == 2:
                # send to ts2
                dict_ts2[queryFromClient] = 'ts2' # put the query key in the dict for ts2
                ts2_Socket.sendall(queryFromClient.encode('utf-8'))
                received_msg = ts2_Socket.recv( 1024 )
                ts = 1
        
        # received_msg=""

        # print( received_msg )
        
        if received_msg.decode('utf-8') == 'other' or received_msg == "":
            print( 'got to other' )
            send_msg = queryFromClient + " - Error:HOST NOT FOUND"
            csockid.send(send_msg.encode('utf-8'))
        
        else:
            print("sending to client")
            csockid.send(received_msg)

   # Close the server socket
    clientSocket.close()
    ts1_Socket.close()
    ts2_Socket.close()
    exit()



t1 = threading.Thread(name='server', target=server)
t1.start()

exit()
