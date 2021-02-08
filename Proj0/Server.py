# Author: Michael Comatas (netID: mac776)

import argparse
from sys import argv
import socket

HOST = socket.gethostname() # get the name of the machine that is the host

PORT = int( argv[1] ) #get the port arg and convert it into an int

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) # creating the server socket
s.bind( (HOST, PORT) )
s.listen(1) #listens for 1 connection
conn, addr = s.accept()
print( 'Connected by, ', addr ) # prints where the connection came from
while True:
    data = conn.recv(1024) #receives the Key from the Client
    if not data:
        break
    with open( 'Pairs.txt', 'r' ) as f: #reads line by line from the Pairs.txt file
        for line in f:
            line = line.strip() #trim to avoid anything weird
            key_value_pair =  line.split(':') # makes a list separated by : and store it into key_value_pair
            not_found = 0 # a variable to tell if the key was found at all or not, if it stays 0, the key is not found
            if data in key_value_pair[0]:   # if we find the key
                conn.sendall(key_value_pair[1]) #send the value to the Client
                not_found = 1 #we found the key so set not_found to 1
                break 
        if not_found == 0:
            conn.sendall( 'NOT FOUND' ) #send 'NOT FOUND' to client since the key was never found
conn.close() #close the connection gracefully