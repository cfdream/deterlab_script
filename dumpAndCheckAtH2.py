import commands
import subprocess
import sys
import string
import re

#kill tcpdump, detect
COMMAND = "sudo pkill tcpdump && sudo pkill detect"
commands.getstatusoutput(COMMAND)

#remove the present dumpfile
COMMAND = "cd /users/xuemei/detectLostPackets && sudo rm -rf tcpdump.pcap"
commands.getstatusoutput(COMMAND)


#get the port name of h1
file=open("/users/xuemei/deterlab_script/topoNew.txt", 'r')
lines=file.readlines()
lines=map(lambda x:x[:-1], lines)
h2Port='eth0'
for i in range(2, len(lines)):
    items=lines[i].split(' ')
    if len(items) == 2:
        #get ports for hosts and switches
        #could be got after the ports are binded
        machine=items[0]
        port=items[1]
        #portId=items[2]
        if 'h2' == machine:
            h2Port = port
            break

#set mac address of the port of s4 connecting to h2
COMMAND = "sudo arp -s 10.1.1.2 06:0b:2b:06:01:02"
commands.getstatusoutput(COMMAND)

#tcpdump 
COMMAND="cd /users/xuemei/detectLostPackets && nohup sudo tcpdump -s 1520 -ttt -vvv -n -i {0} -w tcpdump.pcap > foo.out 2> foo.err < /dev/null &" .format(h2Port)
ret=subprocess.Popen(COMMAND, shell=True)
if ret is None:
    print 'fail:{0}' .format(COMMAND)
    exit(-1)
else:
    print "succ:{0}" .format(COMMAND)

#run checkAndSend
COMMAND="cd /users/xuemei/detectLostPackets && nohup sudo ./detect tcpdump.pcap ../pcapFileGenerator/data/equinix-sanjose.dirA.20120920-130000.UTC.anon.pcap.csv.pcap > foo.out 2> foo.err < /dev/null &"
ret=subprocess.Popen(COMMAND, shell=True)
if ret is None:
    print 'fail:{0}' .format(COMMAND)
    exit(-1)
else:
    print "succ:{0}" .format(COMMAND)
