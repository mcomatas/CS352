# Authors:
# Michael Comatas (netID: mac776)
# Umar Khattak (netID: uk50)

import argparse
from sys import argv
import socket

import struct
import binascii


def send_udp_message(message, address, port): #THIS FUNCTION WAS RECIEVED FROM https://routley.io/posts/hand-writing-dns-messages/
    """send_udp_message sends a message to UDP server

    message should be a hexadecimal encoded string
    """
    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")

def format_hex(hex): # #THIS FUNCTION WAS RECIEVED FROM https://routley.io/posts/hand-writing-dns-messages/
    octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
    pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
    return "\n".join(pairs)

def create_hex_string( data ):
    decoded = data.decode( 'utf-8' ) # decode the data that is sent in from client
    decoded = decoded.split( '.' ) # split to get rid of the . in the URLs
    hex_string = ""
    i = 0
    while i < len(decoded):
        if len(decoded[i]) <= 15:
            hex_string = hex_string + "0" + format(len( decoded[i] ), '0') + decoded[i].encode( 'utf-8' ).hex()
        else:
            hex_string = hex_string + format(len( decoded[i] ), '0') + decoded[i].encode( 'utf-8' ).hex()
        i += 1
    return hex_string # then consturct the hex string message to send to DNS server

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
    print( data )

    hex_string = create_hex_string( data ) # use the function to create the hex string

    hex_string = "AA AA 01 00 00 01 00 00 00 00 00 00 " + hex_string + " 00 00 01 00 01" # THE FORMAT TO CREATE THE HEX STRING WAS TAKEN FROM https://routley.io/posts/hand-writing-dns-messages/
    response = send_udp_message( hex_string, '8.8.8.8', 53 ) # send the udp message using the helper function from the routley blog

    k = (6*4) # start after the header
    sent = 0 # how many IPs have we sent for this website
    data_to_send = "" # one big string for the data we need to send over
    while response[k:k+2] != "00": #check if it is at the termination byte
        to_skip = int( response[k:k+2], 16 )
        k += ( to_skip + 1 ) * 2 # skip past all the name stuff
    k += 8 * 2 #once it gets to termination byte is skips past QTYPE, QCLASS, and NAME to read the TYPE
    while k < len(response):
        if response[k:k+2] != "01": # If it is not an A record it won't have type 01
            # print( response[k:k+2] )
            # print( "other" )
            if sent == 0:
                data_to_send = data_to_send + "other"
                sent += 1
            else:
                data_to_send = data_to_send + "," + "other"
                sent += 1
            k += 7 * 2 # skip to the RDLENGTH
            to_skip = int( response[k:k+4], 16 ) # skip past all the RD length that we don't need 
            k += ( to_skip + 2 ) * 2
        else:
            k += 7 * 2 # skip to RDLENGTH since we know it is an A record
            data_length = int( response[k:k+4], 16 )
            ip_address_hex = response[k+4:k+4+(data_length*2)]
            int_ip = int( ip_address_hex, 16 ) # THIS LINE WAS TAKEN FROM https://stackoverflow.com/questions/2197974/convert-little-endian-hex-string-to-ip-address-in-python
            # print( socket.inet_ntoa(struct.pack(">L", int_ip)) )
            if sent == 0:
                data_to_send = data_to_send + socket.inet_ntoa(struct.pack(">L", int_ip)) # socket.inet_ntoa(struct.pack(">L", int_ip) WAS TAKEN FROM https://stackoverflow.com/questions/2197974/convert-little-endian-hex-string-to-ip-address-in-python
                sent += 1
            else:
                data_to_send = data_to_send + "," + socket.inet_ntoa(struct.pack(">L", int_ip))
                sent += 1
            k += ( data_length + 2 ) * 2
        k += 3 * 2 # we are always ending at the beginner of name, so increment past name to get to the next TYPE for the next IP

    data_to_send = data_to_send.encode( 'utf-8' ) # encode the data_to_send (The IP addresses)
    conn.sendall(data_to_send) # send the IP addresses to client

conn.close() #close the connection gracefully