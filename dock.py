#!/usr/bin/python

import cgi,cgitb
import os,commands,time

cgitb.enable()

print "content-type:text/html"
print ""

v=cgi.FieldStorage()
n=v.getvalue("d")
nodes=int(n)
#nodes=int(nodes)-2
contId=[]

print "creating docker containers for namenode"
y=commands.getoutput('sudo docker run -itd -h nn.example.com newhadoop')
contId.append(y)


print "creating docker containers for jobtracker"
y=commands.getoutput('sudo docker run -itd -h jobt.example.com newhadoop')
contId.append(y)

print "creating docker container for datanodes"
count=1
for i in range(nodes-2):
	y=commands.getoutput("sudo docker run -itd -h dn" +str(count)+".example.com newhadoop")
	contId.append(y)
	count+=1

print "Entrying in the ansible hosts file"
f= open('/etc/ansible/hosts','a')
f.write("[namenode]\n")
f.write("172.17.0.2 \n\n")
f.write("[jobtracker]\n")
f.write("172.17.0.3 \n\n")
f.write("[datanode]\n")
count=4 
for i in range(n-2):
	f.write("172.17.0."+str(count)+"\n")
	count+=1

f.close()

print "creating files"

commands.getoutput("sudo touch hdfs-site.xml")
commands.getoutput("sudo touch core-site.xml")
commands.getoutput("sudo touch mapred-site.xml")

commands.getoutput('sudo chmod 766 hdfs-site.xml')
commands.getoutput('sudo chmod 766 core-site.xml')
commands.getoutput('sudo chmod 766 mapred-site.xml')


print "Entrying in the core-site.xml"

f=open("core-site.xml","w")
f.write('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n')

f.write("<configuration>\n")
f.write("<property>\n<name>fs.default.name</name>\n<value>hdfs://172.17.0.2:10005</value>\n</property>\n</configuration>\n")
f.close()


stat=commands.getstatusoutput("sudo ansible all -m copy -a 'src=core-site.xml dest=/etc/hadoop/' ")


print "Entrying hdfs-site.xml for datanode"

f=open('hdfs-site.xml','w')
f.write('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n')
f.write('<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>/new_hadoop_dir</value>\n</property>\n</configuration>\n')
f.close()

stat=commands.getstatusoutput("sudo ansible datanode -m copy -a 'src=hdfs-site.xml dest=/etc/hadoop/' ")

print "hdfs-site.xml for namenode"
f=open('hdfs-site.xml','w')
f.write('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n')
f.write('<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>/metadata</value>\n</property>\n</configuration>\n')
f.close()
stat=commands.getstatusoutput("sudo ansible namenode -m copy -a 'src=hdfs-site.xml dest=/etc/hadoop/' ")


print "mapred-site.xml"
f=open('mapred-site.xml','w')
f.write('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n')
f.write('<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>172.17.0.3:9001</value>\n</property>\n</configuration>\n')
f.close()

commands.getoutput("sudo ansible datanode -m copy -a 'src=mapred-site.xml dest=/etc/hadoop/'")
commands.getoutput("sudo ansible jobtracker -m copy -a 'src=mapred-site.xml dest=/etc/hadoop/'")


print "starting the services for hadoop"

commands.getoutput('sudo ansible  namenode  -m   shell  -a  "hadoop namenode -format" ')
time.sleep(5)
commands.getoutput('sudo ansible  namenode  -m   shell  -a  "hadoop-daemon.sh start namenode"')
commands.getoutput('sudo ansible  jobtracker -m   shell  -a  "hadoop-daemon.sh start jobtracker"')
commands.getoutput('sudo ansible  datanode  -m   shell  -a  "hadoop-daemon.sh start tasktracker"')
commands.getoutput('sudo ansible  datanode  -m   shell  -a  "hadoop-daemon.sh start datanode"')

