#!/usr/bin/env python

import cgi,cgitb
import os, commands
cgitb.enable()

print "content-type:text/html"
print ""

f=open("ip.txt")
x=f.read()
f.close()
os.system("sudo setenforce 0")
fip=x.split("\n")
#print fip
l=len(fip)
print '<form action="/cgi-bin/nn.py"  >'
for i in fip[0:l-1]:
	print "<input type=\"radio\" name=\"nn\" value=\""+i+"\">"+i
	mem=commands.getoutput("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" cat /proc/meminfo | grep MemTo | awk '{print $2}'")
	cpu=commands.getoutput("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" lscpu | grep '^CPU(s)' | awk '{print $2}'")
	#print mem
	#print cpu
	sdss=str(round(int(mem)/1024.0/1024))
	#print sdss
	print "<html>&nbsp</html>"+"Ram is " +sdss+" GB and CPU is "+cpu+" core"
	print "</br>"

print "<input type=\"submit\" value=\"Submit\">"
print "</form>"



"""	a=commands.getoutput("ssh "+i+" cat /proc/meminfo | grep Mem ")
		for i in a:
			print i,
			"""
