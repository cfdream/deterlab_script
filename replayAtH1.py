import commands
import subprocess
import sys
import string
import re

#get the port name of h1
file=open("/users/xuemei/topoNew.txt", 'r')
lines=file.readlines()
lines=map(lambda x:x[:-1], lines)
h1Port='eth0'
for i in range(2, len(lines)):
    items=lines[i].split(' ')
    if len(items) == 2:
        #get ports for hosts and switches
        #could be got after the ports are binded
        machine=items[0]
        port=items[1]
        #portId=items[2]
        if 'h1' == machine:
            h1Port = port
            break

#kill existing tcpreplay
COMMAND = "sudo pkill tcpreplay"
ret,output=commands.getstatusoutput(COMMAND)

#set mtu size
COMMAND = "sudo ifconfig {0} mtu 9000" .format(h1Port)
ret,output=commands.getstatusoutput(COMMAND)

#tcpreplay
COMMAND = "nohup sudo tcpreplay -i {0} --mbps=200 /users/xuemei/pcapFileGenerator/data/equinix-sanjose.dirA.20120920-130000.UTC.anon.pcap.csv.pcap  > foo.out 2> foo.err < /dev/null &" .format(h1Port)
#COMMAND = "ls&"

ret=subprocess.Popen(COMMAND, shell=True)
if ret is None:
    print 'fail:{0}' .format(COMMAND)
    exit(-1)
else:
    print "succ:{0}" .format(COMMAND)
