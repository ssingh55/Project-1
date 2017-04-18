#!/usr/bin/env python

import cgi,cgitb
import os,commands
cgitb.enable()

print "content-type:text/html"
print ""

x=cgi.FieldStorage()
y=x.getlist("dn")

f=open("nip.txt")
ip=f.read()
f.close()

xml="""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
"""

corest="""
<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{}:10001</value>
</property>
</configuration>
""".format(ip)

hdfst="""
<configuration>
<property>
<name>dfs.data.dir</name>
<value>/datanod</value>
</property>
</configuration>
"""

f=open("core-site.xml","w")
f.write(xml)
f.write("\n")
f.write("\n")
f.write(corest)
f.close()

f=open("hdfs-site.xml","w")
f.write(xml)
f.write("\n")
f.write("\n")
f.write(hdfst)
f.close()

for i in y:
	commands.getoutput("sudo sshpass -predhat scp -o StrictHostKeyChecking=no hadoop-1.2.1-1.x86_64.rpm jdk-7u79-linux-x64.rpm root@"+i+":/root/")
	commands.getoutput("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" rpm -i hadoop-1.2.1-1.x86_64.rpm --replacefiles")
	commands.getoutput("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" rpm -i jdk-7u79-linux-x64.rpm")
	
	os.system("sudo sshpass -predhat scp core-site.xml  root@"+i+":/etc/hadoop/")
	os.system("sudo sshpass -predhat scp hdfs-site.xml root@"+i+":/etc/hadoop/")
	os.system("sudo sshpass -predhat ssh root@"+i+" setenforce 0")
	#os.system("sshpass -predhat ssh "+i+" hadoop namenode -format")
	commands.getoutput("sudo sshpass -predhat ssh root@"+i+" hadoop-daemon.sh start datanode")

for i in y:
	print "IP running process"+i
	print "</br>"
	print commands.getoutput("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+i+" /usr/java/jdk1.7.0_79/bin/jps")
	print "</br>"

print "Redirecting to configure jobtracker"
print "<meta http-equiv='refresh' content='4;http://localhost/cgi-bin/jobtracker.py'>"
