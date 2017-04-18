#!/usr/bin/env python

import cgi,cgitb,time
import os,commands
cgitb.enable()

print "content-type:text/html"
print ""

x=cgi.FieldStorage()
y=x.getvalue("nn")
f=open("nip.txt","w+")
f.write(y)
f.close()
os.system("sed -i '/"+y+"/d' ip.txt")
os.system("sudo sshpass -predhat scp -o StrictHostKeyChecking=no hadoop-1.2.1-1.x86_64.rpm jdk-7u79-linux-x64.rpm root@"+y+":/root/")
os.system("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+y+" rpm -i hadoop-1.2.1-1.x86_64.rpm --replacefiles")
os.system("sudo sshpass -predhat ssh -o StrictHostKeyChecking=no root@"+y+" rpm -i jdk-7u79-linux-x64.rpm")

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
""".format(y)
#print named

hdfst="""
<configuration>
<property>
<name>dfs.name.dir</name>
<value>/namenod</value>
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

os.system("sudo sshpass -predhat scp core-site.xml  root@"+y+":/etc/hadoop/")
os.system("sudo sshpass -predhat scp hdfs-site.xml root@"+y+":/etc/hadoop/")
os.system("sudo sshpass -predhat ssh -o StrictHostKeychecking=no root@"+y+" setenforce 0")
os.system("sudo sshpass -predhat ssh -o StrictHostKeychecking=no root@"+y+" hadoop namenode -format")
commands.getoutput("sudo sshpass -predhat ssh root@"+y+" hadoop-daemon.sh start namenode")
print commands.getoutput("sudo sshpass -predhat ssh root@"+y+ " /usr/java/jdk1.7.0_79/bin/jps")
print "</br>"
print "Now u are been redirected to create datanode"
time.sleep(10)

print "<meta http-equiv='refresh' content='2;url=http://localhost/cgi-bin/dncheck.py'>"
