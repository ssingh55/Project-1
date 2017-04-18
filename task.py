#!/usr/bin/env python

import cgi,cgitb
import os,commands
cgitb.enable()

print "content-type:text/html"
print ""

x=cgi.FieldStorage()
y=x.getlist("tt")

#print "Inserting namenode ip"
f=open("nip.txt")
ip=f.read()
f.close()

#print "creating xml "
xml="""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
"""

#print "creating coresite "
corest="""
<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>
</property>
</configuration>
""".format(ip)

f=open("core-site.xml","w")
f.write(xml)
f.write("\n")
f.write("\n")
f.write(corest)
f.close()

for i in y:
	commands.getoutput("sudo sshpass -predhat scp -o StrictHostKeyChecking=no hadoop-1.2.1-1.x86_64.rpm jdk-7u79-linux-x64.rpm root@"+i+":/root/")
	commands.getoutput("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" rpm -i hadoop-1.2.1-1.x86_64.rpm --replacefiles")
	commands.getoutput("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" rpm -i jdk-7u79-linux-x64.rpm")
	
	
#print "creating mapred-site "
	mapred="""
<configuration>
<property>
<name>mapred.job.tracker</name>
<value>{}:9001</value>
</property>
</configuration>
""".format(i)
	
	
	f=open("mapred-site.xml","w")
	f.write(xml)
	f.write("\n")
	f.write("\n")
	f.write(mapred)
	f.close()

	os.system("sudo sshpass -predhat scp core-site.xml  root@"+i+":/etc/hadoop/")
	os.system("sudo sshpass -predhat scp mapred-site.xml root@"+i+":/etc/hadoop/")
	os.system("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" setenforce 0")
	#os.system("sshpass -predhat ssh "+i+" hadoop namenode -format")
	commands.getoutput("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" hadoop-daemon.sh start tasktracker")

for i in y:
	print "IP running process"+i
	print "</br>"
	print commands.getoutput("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" /usr/java/jdk1.7.0_79/bin/jps")

#print "<meta http-equiv='refresh' content='4;http://localhost/cgi-bin/tas.py'>"
