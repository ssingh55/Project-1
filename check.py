#!/usr/bin/env python


import  time,sys,os,commands,re
import cgi,cgitb

print "content-type:text/html"
print ""

cgitb.enable()
c=cgi.FieldStorage()
nodes=c.getvalue("n")
nodes=int(nodes)
#nodes=3
#scanning ip part

#os.system(">dev.txt")
#os.system(">ip.txt")

f=open("dev.txt","w+")
ip=open("ip.txt","w+")

f.close()
ip.close()

x=os.listdir("/sys/class/net/")
for i in  x:
	if re.search("^enp",i) or re.search("^br",i) or re.search("^eno",i):
                x=commands.getoutput("ifconfig "+i+" | grep \"inet \" | awk -F\" \" '{print $2}'")
                ips=".".join(x.split(".")[0:3])
#print ips
                z=os.system("for i in {1..253} ; do (arping "+ips+".$i -c 2 -I "+i+" -w 5 &>/dev/null && echo "+ips+".$i >>ip.txt && echo "+i+" >>dev.txt  &) done")
#print z

time.sleep(30)
nnmem=0
nncpu=0
count=0

print "Reading ip from ip.txt file"
f=open("ip.txt")
x=f.read()
f.close()

fip=x.split("\n")
os.system("sudo setenforce 0")
l=len(fip)

print "Selecting pc for ram"

for i in fip[0:l-1]:
	#print "<input type=\"radio\" name=\"nn\" value=\""+i+"\">"+i
	mem=commands.getoutput("sudo ssh -o StrictHostKeyChecking=no root@"+i+" cat /proc/meminfo | grep MemTo | awk '{print $2}'")
	cpu=commands.getoutput("sudo ssh -o StrictHostKeyChecking=no root@"+i+" lscpu | grep '^CPU(s)' | awk '{print $2}'")

	if mem >= nnmem:
                if cpu >= nncpu:
                        nnmem=mem
                        nn=i

f=open("nnip.txt","w")
f.write(nn)
f.close()

#Assigning jobtracker and datanode  ip

os.system("sed -i '/"+nn+"/d' ip.txt")
f=open("ip.txt")
jip=f.read()
f.close()
jip=jip.split("\n")[0]
f=open("jip.txt","w")
f.write(jip)
f.close()
os.system("sed -i '/"+jip+"/d' ip.txt")


ans = open('/etc/ansible/hosts', 'w')
ans.write('[namenode]\n')
ans.write(nn+'\n\n')
ans.write('[jobtracker]\n')
ans.write(jip+'\n\n')
f=open("ip.txt")
dnip=f.read()
f.close()
dnip=dnip.split("\n")

ans.write('[datanode]\n')

for i in dnip[:len(dnip)-1]:
        if count <=nodes:
            ans.write(i+'\n')
	    ans.write("\n")
            count+=1


ans.write('[tasktracker]\n')

for i in dnip[:len(dnip)-1]:
        if count <=nodes:
            ans.write(i+'\n')
	    ans.write("\n")
            count+=1

ans.close()
#Entries for namenode

f='<?xml version="1.0"?>'
f1='<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>'
x=f+'\n'+f1+'\n\n'"<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://"+nn+":10001</value>\n</property>\n</configuration>"
fcore='core-site.xml'
f2=open(fcore,'w')
f2.write(x)
f2.close()
#for   i in  ip:
#	commands.getoutput('ssh  root@'+i+' rpm -ivh ftp://192.168.56.1/rhel/rhel7rpm/hadoop-1.2.1-1.x86_64.rpm --replacefiles')
commands.getoutput("sudo ansible all -a 'rpm -ivh ftp://192.168.2.13/pub/packages/rhel7rpm/hadoop-1.2.1-1.x86_64.rpm --replacefiles'")
commands.getoutput("sudo ansible all -a 'rpm -ivh ftp://192.168.2.13/pub/packages/rhel7rpm/jdk-7u79-linux-x64.rpm'")



commands.getoutput('sudo chmod 766 core-site.xml')

stat=commands.getstatusoutput("sudo ansible all -m copy -a 'src=core-site.xml dest=/etc/hadoop/' ")

nnd="/namenod"
f='<?xml version="1.0"?>'
f1='<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>'
x=f+'\n'+f1+'\n\n'"<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>/"+nnd+"</value>\n</property>\n</configuration>"
fsite="hdfs-site.xml"
f3=open(fsite,'w')
f3.write(x)
f3.close()

commands.getoutput('sudo chmod 766 hdfs-site.xml')
stat=commands.getstatusoutput("sudo ansible namenode -m copy -a 'src=hdfs-site.xml dest=/etc/hadoop/' ")

#datanode hdfs-site

dnd="/datanode"
f='<?xml version="1.0"?>'
f1='<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>'
x=f+'\n'+f1+'\n\n'"<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>/"+dnd+"</value>\n</property>\n</configuration>"
fdnsite="hdfs-site.xml"
f3=open(fdnsite,'w')
f3.write(x)
f3.close()

commands.getoutput('sudo chmod 766 hdfs-site.xml')
commands.getstatusoutput("sudo ansible datanode -m copy -a 'src=hdfs-site.xml dest=/etc/hadoop/' ")


#mapred-site.xml
f=open('mapred-site.xml','w')
f.write('<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n\n')
f.write('<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>'+jip+':10002</value>\n</property>\n</configuration>\n')
f.close()
commands.getoutput('sudo chmod 766 mapred-site.xml')

commands.getoutput("sudo ansible tasktracker -m copy -a 'src=mapred-site.xml dest=/etc/hadoop/'")
commands.getoutput("sudo ansible jobtracker -m copy -a 'src=mapred-site.xml dest=/etc/hadoop/'")

##starting the services for hadoop

commands.getoutput('sudo ansible  namenode  -m   shell  -a  "hadoop namenode -format" ')
time.sleep(5)
commands.getoutput('sudo ansible  namenode  -m   shell  -a  "hadoop-daemon.sh start namenode"')
commands.getoutput('sudo ansible  jobtracker -m   shell  -a  "hadoop-daemon.sh start jobtracker"')
commands.getoutput('sudo ansible  datanode  -m   shell  -a  "hadoop-daemon.sh start tasktracker"')
commands.getoutput('sudo ansible  datanode  -m   shell  -a  "hadoop-daemon.sh start datanode"')


