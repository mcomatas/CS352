# Project 2: Extracting IP addresses from responses
## Michael Comatas (netID: mac776)
## Umar Khattak (netID: uk50)
## 23 March 2021

# Known Issues:

We used Python 3.6 for this project.
As far as we know there are no known major issues with my code / project. The biggest possible issue I can think of is that if there are multiple instances of "other" or having "other" then an IP and then another "other" or similar situations. I am pretty confident that it would still work in test cases like this and in situations like this because of the way we looked through the bytes that the DNS server sent back to us. Again I am pretty confident that it should work in most test cases, if not all, since it worked with one "other" and one case of sending multiple IPs back. As far as issue though that is the biggest possible issue I can think of.

# Issues we had:

I think I faced a bit of trouble at every step of the way, getting the response from the DNS server, reading the response, etc. but those issues never stumped me for too long and the routely blog helped me understand this project a lot. The biggest hurdle I encountered with this project was dealing with the non A record IP address that would be returned. I had a very hard time finding where I should look for that and how to deal with that in order to return "other" rather than an IP address. I felt like it was not explained very much so that it took me awhile to figure out what it was and how to deal with it. In total I think we spent around 10-12 hours on this project (give or take a couple hours) in total, and it was a couple days of work once we started working on it.