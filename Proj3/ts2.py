# Authors:
# Michael Comatas (netID: mac776)
# Umar Khattak (netID: uk50)

import argparse
from sys import argv
import socket

import struct
import binascii

import dns.name
import dns.message
import dns.query
import dns.flags

from collections import OrderedDict

def get_type(type): # THIS FUNCTION WAS TAKEN FROM https://gist.github.com/mrpapercut/92422ecf06b5ab8e64e502da5e33b9f7 it was to help build the DNS request message better than what I had in project 2
    types = [
        "ERROR", # type 0 does not exist
        "A",
        "NS",
        "MD",
        "MF",
        "CNAME",
        "SOA",
        "MB",
        "MG",
        "MR",
        "NULL",
        "WKS",
        "PTS",
        "HINFO",
        "MINFO",
        "MX",
        "TXT"
    ]

    return "{:04x}".format(types.index(type)) if isinstance(type, str) else types[type]


def build_message(type, address): # THIS FUNCTION WAS TAKEN FROM https://gist.github.com/mrpapercut/92422ecf06b5ab8e64e502da5e33b9f7 it was to help build the DNS request message better than what I had in project 2
    ID = 43690  # 16-bit identifier (0-65535) # 43690 equals 'aaaa'

    QR = 0      # Query: 0, Response: 1     1bit
    OPCODE = 0  # Standard query            4bit
    AA = 0      # ?                         1bit
    TC = 0      # Message is truncated?     1bit
    RD = 1      # Recursion?                1bit
    RA = 0      # ?                         1bit
    Z = 0       # ?                         3bit
    RCODE = 0   # ?                         4bit

    query_params = str(QR)
    query_params += str(OPCODE).zfill(4)
    query_params += str(AA) + str(TC) + str(RD) + str(RA)
    query_params += str(Z).zfill(3)
    query_params += str(RCODE).zfill(4)
    query_params = "{:04x}".format(int(query_params, 2))

    QDCOUNT = 1 # Number of questions           4bit
    ANCOUNT = 0 # Number of answers             4bit
    NSCOUNT = 0 # Number of authority records   4bit
    ARCOUNT = 0 # Number of additional records  4bit

    message = ""
    message += "{:04x}".format(ID)
    message += query_params
    message += "{:04x}".format(QDCOUNT)
    message += "{:04x}".format(ANCOUNT)
    message += "{:04x}".format(NSCOUNT)
    message += "{:04x}".format(ARCOUNT)

    # QNAME is url split up by '.', preceded by int indicating length of part
    addr_parts = address.split(".")
    for part in addr_parts:
        addr_len = "{:02x}".format(len(part))
        addr_part = binascii.hexlify(part.encode())
        message += addr_len
        message += addr_part.decode()

    message += "00" # Terminating bit for QNAME

    # Type of request
    QTYPE = get_type(type)
    message += QTYPE

    # Class for lookup. 1 is Internet
    QCLASS = 1
    message += "{:04x}".format(QCLASS)

    return message


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

name_dict = {} # create a dictionary to hold names we have seen in case we see them again

HOST = socket.gethostname() # get the name of the machine that is the host

PORT = int( argv[1] ) #get the port arg and convert it into an int

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) # creating the server socket
print( '[S]: Server socket created for client' )
s.bind( (HOST, PORT) )
s.listen(1) #listens for 1 connection
conn, addr = s.accept()
print( 'Connected by, ', addr ) # prints where the connection came from
while True:
    data = conn.recv(1024) #receives the Key from the Client
    if not data:
        break
    # print( data )

    data_to_send = '' # what we will send over to ls

    if data.decode('utf-8') in name_dict:
        data_to_send = name_dict[data.decode('utf-8')]
    else:
        hex_string = build_message( 'A', data.decode('utf-8') ) # Using the funciton taken from https://gist.github.com/mrpapercut/92422ecf06b5ab8e64e502da5e33b9f7 to help build the DNS request message
        # print( hex_string )

        response = send_udp_message( hex_string, '8.8.8.8', 53 ) # send the udp message using the helper function from the routley blog
        # print( response )

        k = (6*4) # start after the header
        sent = 0 # how many IPs have we sent for this website
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
        name_dict[data.decode('utf-8')] = data_to_send
    # print( data_to_send )
    data_to_send = data_to_send.encode( 'utf-8' ) # encode the data_to_send (The IP addresses)
    conn.sendall(data_to_send) # send the IP addresses to client

conn.close() #close the connection gracefully