#!/usr/bin/env python

import os,commands
import cgi,cgitb
cgitb.enable()

print "content-type:text/html"
print ""
f=open("ip.txt")
fip=f.read()
f.close()
l=len(fip)
print "<html>"
print "<head>"
print "<title>Jobtracker ip </title>"
print "</head>"
print "<body>"
print "<form action='/cgi-bin/task.py' >"
for i in fip.split("\n")[0:l-1]:
	print "<input type='checkbox' name='tt' value='"+i+"'>"+i
	print "</br>"

print "<input type='submit' value='submit'>"
print "</form>"
print "</body>"
print "</html>"
