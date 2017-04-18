#!/usr/bin/python

import os,cgi,cgitb
import commands
cgitb.enable()

print "content-type:text/html"
print ""

x=cgi.FieldStorage()
dev=x.getvalue("d")

print "Creating ip.txt file"
f=open("ip.txt","w")
f.close()
#os.system("nmap -n 192.168.2.0/24 -sS | grep -i report | cut -d" " -f5 >ip.txt")
print "Scanning your system ip on the selected interface"
x=commands.getoutput("ifconfig "+dev+" | grep \"inet \" | awk -F\" \" '{print $2}'")

ips=".".join(x.split(".")[0:3])
#print ips
print "Scanning all the ip in your range"
z=os.system("for i in {1..253} ; do (arping "+ips+".$i -c 2 -I "+dev+" -w 5 &>/dev/null && echo "+ips+".$i >>ip.txt &) done")
#print z

if z==0:
        print "Redirecting to select the namenode ip"
	print "<meta http-equiv='refresh' content='1;url=http://127.0.0.1/cgi-bin/ipd.py'>"
else:
	print "there is some error in scanning please check your system ip "
