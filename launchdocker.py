#!/usr/bin/env python

import cgi,cgitb
from os import system

cgitb.enable()
system("yum install docker-engine -y")
system("systemctl start docker")
system("systemctl enable docker")

