# Project 3: Load Balancing DNS servers
## Michael Comatas (netID: mac776)
## Umar Khattak (netID: uk50)
## 29 April 2021

# How we implemented our LS server:

Our LS server starts by receiving all the arguments and using those to connect to the client socket and then creating two more sockets to connect to the ts1 and ts2 servers. The we declared three different variables: ts, dict_ts1, and dict_ts2. ts is to keep track of which server we want to send new queries too, it is set to either 1 or 2. Then dict_ts1 and dict_ts2 are dictionaries that are to keep track of hostnames that have been seen already. If a hostname is sent to ts1 then it will be added to the dict_ts1 dictionary. When receiving hostnames from the client we first check to see if the hostname is in one of the dictionaries and if it is we can send it to whichever server corresponds to it. If the hostname is not in the dictionary then we check the ts variable and if it is 1 we send to ts1 and change ts to 2 and if ts is 2 then we send to ts2 and change ts to 1. After the sockets are created we use settimeout(5) function to deal with the time out if neither TS responds.

# Known Issues:

The only known in our program is that we did not handle the fact that if one TS server crashes then the LS server continues to send the remaining hostnames to the other TS server. Unfortunatley we ran out of time and this was one of the last things to handle and we did not get around to it. Addtionally we are not 100% sure that the timeout part works either. We found it difficult to test this part since we were dealing with larger bugs in our time working on this project, we tried using the settimeout(5) function after the sockets were created, but again we are not 100% sure that is working. Other than the things mentioned we believe that everything is working.

# Problems we faced:

This project did not give us too much of an issue aside from a couple things. We had some trouble dealing with all of the sockets during this project. At one point we had it so that all of the data being sent from LS to the TS servers was getting jumbled together, although it was an easy fix in the end by making sure that the LS was receving the same amount of times that it was sending, it was something we were unaware of and gave us some problems. Aside from that there were not too many issues since this project was a mix of projects 1 and 2 together. 

# What we learned:

We learned how to deal with many servers in this project by having a client talk to one server and that server to talk with two other servers. Sockets can be tricky to work with as this is both our first class working with them. 