import socket as socky
import pdb
import argparse

argparse = argparse.ArgumentParser()
argparse.add_argument('rsListenPort', type=int, help='rsListenPort')
argument = argparse.parse_args()
ListenPort = argument.rsListenPort
listDNS = {}

def help(rsHostname):
    rsHostname = rsHostname.lower()
    if rsHostname in listDNS:
        if listDNS[rsHostname][1] == "A":
            return rsHostname + " " + listDNS[rsHostname][0] + " " + listDNS[rsHostname][1]
        elif listDNS[rsHostname][1] == "NS":
            return rsHostname + " " + listDNS[rsHostname][1]
    else:
        return x + " - NS"

def help2():
    DNSRS_file = open("PROJI-DNSRS.txt", "r")
    file_read = DNSRS_file.readlines()
    for x in file_read:
        string = x.split()
        listDNS[string[0].lower()] = [string[1], string[2]]
        if string[2] == "NS":
            x = string[0]
    return x

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
            message = help(output)
            csockid.sendall(message.encode('utf-8'))

    sockey.close()
    exit()

x = help2()
function()