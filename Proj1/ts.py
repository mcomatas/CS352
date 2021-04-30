import socket as socky
import pdb
import argparse

argparse = argparse.ArgumentParser()
argparse.add_argument('tsListenPort', type=int, help='tsListenPort')
argument = argparse.parse_args()
ListenPort = argument.tsListenPort
listDNS = {}

def help(tsHostname):
    tsHostname = tsHostname.lower()
    if tsHostname in listDNS:
        if listDNS[tsHostname][1] == "A": 
            return tsHostname + " " + listDNS[tsHostname][0] + " " + listDNS[tsHostname][1]
    else: #this'll be an error
        return "Hostname - Error:HOST NOT FOUND"

def help2():
    DNSTS_file = open("PROJI-DNSTS.txt", "r")
    file_read = DNSTS_file.readlines()
    for x in file_read:
        string = x.split()
        listDNS[string[0].lower()] = [string[1], string[2]]

def function():
    try:
        sockey = socky.socket(socky.AF_INET, socky.SOCK_STREAM)
    except socky.error as error: #error
        print('{} \n'.format("Hostname - Error:HOST NOT FOUND", error))
    socky_bind = ('', ListenPort)
    sockey.bind(socky_bind)
    sockey.listen(10)
    csockid, addr = sockey.accept()
    while 1:
        givenInput = csockid.recv(1024)
        output = givenInput.decode('utf-8')

        if(output.strip() == "we've gone through it all, close now"): #message got sent from client to close
            sockey.close()
            exit()
        else:
            data = help(output)
            csockid.sendall(data.encode('utf-8'))

    sockey.close()
    exit()

help2()
function()