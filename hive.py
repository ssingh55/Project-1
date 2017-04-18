#!/usr/bin/python


import os,commands
import cgi,cgitb

cgitb.enable()


print "content-type:text/html"
print ""

os.system("tar -xvzf apache-hive-1.2.1-bin.tar.gz")
os.system("mv apache-hive-* /hive")
os.system("export HIVE_HOME=/hive")
os.system("export JAVA_HOME=/usr/java/jdk-1.7.0_79")
x= """ 1. Create Database
2. Create Table
3. Insert values into table"

"""
print x
print "\n\n"
y=raw_input("Enter your option :: ")
if y == "1":
	nm=raw_input("Enter the database name u want to create ::")
	("CREATE DATABASE "+nm)

elif y == "2" :
	nm=raw_input("Enter the table name u want to create ::")

