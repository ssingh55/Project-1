#!/usr/bin/env python

import os,cgi,cgitb,commands
cgitb.enable()

print "content-type:text/html"
print ""

fip=commands.getoutput('nmap  -sS -n   192.168.10.0/24    |   grep -i report | cut -d" " -f5')
#f=open("ip.txt")
#fip=f.read()
#f.close()
print fip
fip=fip.split("\n")
os.system('echo -e "\n\n\n\n\n" | ssh-keygen ')
for i in fip:
	os.system("ssh-copy-id -o StrictHostKeyChecking=no "+i)

"""
for i in fip[0:len(fip)-1]:
	os.system("ssh-copy-id "+i)
"""
