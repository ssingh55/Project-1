#!/usr/bin/python

import os,cgi,cgitb
cgitb.enable()

print "content-type:text/html"
print ""

for i in  os.listdir("/sys/class/net/"):
	print i+" && ",

print "<form action=\"/cgi-bin/ipsc.py\">"
print "Enter device name <input type=\"text\" name=\"d\" >"
print "<input type=\"submit\" value =\"Submit\" >"
print "</form>"
