#!/usr/bin/python

import cgi,cgitb
import os,commands
cgitb.enable()


print "content-type:text/html"
print ""

v=cgi.FieldStorage()
var=v.getvalue("h")

if var=="manual":
	print "please wait to launch the manual setup"
	print "<meta http-equiv='refresh' content='1;url=http://localhost/cgi-bin/dev.py'>"
elif var=="auto":
	print "please wait to launch the automatic setup"
	print "<meta http-equiv='refresh' content='1;url=http://localhost/auto.html'>"
elif var=="docker":
	print "please wait to launch the automation setup"
	print "<meta http-equiv='refresh' content='1;url=http://localhost/cgi-bin/dock.html'>"
else:
	print "Please select some option in the previous menu"
