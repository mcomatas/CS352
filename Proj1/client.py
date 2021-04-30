import socket as socky
import pdb
import argparse

argparse = argparse.ArgumentParser()
argparse.add_argument('RSHostname', type=str, help='RSHostname')
argparse.add_argument('rsListenPort', type=int, help='rsListenPort')
argparse.add_argument('tsListenPort', type=int, help='tsListenPort')


argument = argparse.parse_args()
RSHostname = argument.RSHostname
rsListenPort = argument.rsListenPort
tsListenPort = argument.tsListenPort

def function():
    try:  
        rsSocky = socky.socket(socky.AF_INET, socky.SOCK_STREAM)
    except socky.error as sockyError: #error
        print('{} \n'.format("Hostname - Error:HOST NOT FOUND", sockyError))

    try:
        tsSocky = socky.socket(socky.AF_INET, socky.SOCK_STREAM)
    except socky.error as sockyError: #error
        print('{} \n'.format("Hostname - Error:HOST NOT FOUND", sockyError))

    socky_bind = (socky.gethostbyname(RSHostname), rsListenPort)
    rsSocky.connect(socky_bind)
    rsSocky.sendall("test".encode('utf-8'))
    tsHostname = (rsSocky.recv(1024).decode('utf-8').split())[0]
    socky_bind = (socky.gethostbyname(tsHostname), tsListenPort)
    tsSocky.connect(socky_bind)

    HNS_file = open("PROJI-HNS.txt", "r")
    RESOLVED_file = open("RESOLVED.txt", "w")
    HNS_read = HNS_file.readlines()

    for i in HNS_read:
        givenInput = i
        rsSocky.sendall(givenInput.rstrip().encode('utf-8'))
        output = rsSocky.recv(1024).decode('utf-8')
        if output.split()[2] == "NS":
            tsSocky.sendall(givenInput.rstrip().encode('utf-8'))
            output = tsSocky.recv(1024).decode('utf-8')
        RESOLVED_file.write(output + '\n')

    rsSocky.sendall("we've gone through it all, close now".encode('utf-8')) #send these messages so we know when to close
    tsSocky.sendall("we've gone through it all, close now".encode('utf-8')) #do an if statement for these to close in rs andts
    
    HNS_file.close()
    RESOLVED_file.close()
    rsSocky.close()
    tsSocky.close()
    exit()

function()