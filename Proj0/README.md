# Project 0: Simple Server Client Programs
## Michael Comatas (netID: mac776)
## 10 February 2021

# Known Issues:

As far as I know there are no major problems with my code / project. I did a couple of test cases and it seemed to pass them all. I started with the test cases given to me and I tried test cases with key value pairs like: String:Number, and String:String with both of those working no problem. I believe that if this works most cases should work as well (about 75%). One thing that could be an issue is that my server is only listening for one connection (s.listen(1) line 13 in Server.py). I noticed that when the client connected to the server it would write to results.txt quickly and close out almost instantly. To me it seemed fine to have the server take one client connection and write to results.txt.

# Problems I had:


I didn't have too many issues with this project as it is pretty straight forward. I had a bit of trouble getting the connection between client and server right away, but I figured it out pretty quickly. Then the only other problem I had was figuring out how to interpret the data sent over from the client and seeing if it is a key in the Pairs.txt file. Again that didn't take me too long to figure out, but a decent amount of time. Other than that there were not any huge problems for this project. I probably spent about 4 hours max on this project when thinking, coding or researching on the topic.
