import commands
import subprocess
import sys
import string
import re

hosts=['h1', 'h2']
switches=['s1', 's2', 's3', 's4']
machines=['s1', 's2', 's3', 's4', 'h1', 'h2']

def generate_new_topofile():
    oFile = open('topoNew.txt', 'w')
    #login to machine and autobuild
    for machine in machines:
        COMMAND ="cd /users/xuemei/deterlab_script && ifconfig > ifconfig.out.{0}" .format(machine)
        ssh = subprocess.Popen(["ssh", "%s.mscm.vcrib" % machine, COMMAND],
                                shell=False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    #print hosts
    for i in range(len(hosts)-1):
        oFile.write("{0} " .format(hosts[i]))
    oFile.write("{0}\n" .format(hosts[len(hosts)-1]))
    #print switches
    for i in range(len(switches)-1):
        oFile.write("{0} " .format(switches[i]))
    oFile.write("{0}\n" .format(switches[len(switches)-1]))
        
    #get machine-eth, machine-ip map
    machineEthMap={}
    machineIpMap={}
    for machine in machines:
        ifconfigFile="ifconfig.out.{0}" .format(machine)
        file=open(ifconfigFile)
        lines=file.readlines()
        lines=map(lambda x:x[:-1], lines)

        eth_now=''
        ip=''
        found_eth=False
        prog=re.compile('inet addr:(10.1.[1-9]+\.\d+)')
        for i in range(len(lines)):
            line=lines[i]
            if len(line)==0:
                continue
            if not line[0] in [' ','\t','\n']:
                eth_now=line.split(' ')[0]
                found_eth=True
            res=prog.search(line)
            if res!=None and found_eth:
                found_eth=False
                ip=res.group(1)
                #one eth-ip pair is found
                if machine not in machineEthMap:
                    machineEthMap[machine] = [eth_now]
                    machineIpMap[machine] = [ip]
                else:
                    machineEthMap[machine].append(eth_now)
                    machineIpMap[machine].append(ip)    
                print "machine-eth-ip:{0}-{1}-{2}" .format(machine, eth_now, ip)
                oFile.write("{0} {1}\n" .format(machine, eth_now))
    #get links, IP:10.1.x.y. If x is the same, then in the same link
    for i in range(len(machines)):
        m1=machines[i]
        for k in range(len(machineEthMap[m1])):
            m1eth=machineEthMap[m1][k]
            m1IpByte3=machineIpMap[m1][k].split('.')[2]
            for j in range(i+1, len(machines)):
                m2=machines[j]
                for l in range(len(machineEthMap[m2])):
                    m2eth=machineEthMap[m2][l]
                    m2IpByte3=machineIpMap[m2][l].split('.')[2]
                    if m1IpByte3 == m2IpByte3:
                        print "link:{0} {1} {2} {3}" .format(m1, m2, m1eth, m2eth)
                        oFile.write("{0} {1} {2} {3}\n" .format(m1, m2, m1eth, m2eth))
    oFile.write("\n")


def auto_login_and_build(flag):
    #login to switches and autobuild
    for switch in switches:
        COMMAND ="cd /users/xuemei/openvswitch-2.3.0 && python autobuild.py {0}" .format(flag)

        ssh = subprocess.Popen(["ssh", "%s.mscm.vcrib" % switch, COMMAND],
                                shell=False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            print >>sys.stderr, "ERROR: %s" % error
        else:
            print result

def test():
    HOST="xuemei@users.isi.deterlab.net"
    # Ports are handled in ~/.ssh/config since we use OpenSSH
    COMMAND="uname -a && ls"

    ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
    shell=False,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print >>sys.stderr, "ERROR: %s" % error
    else:
        print result


if len(sys.argv)!=2 or not sys.argv[1] in ['0','1','2','3','4']:
    print 'usage: python autoLoginAndBuild.py k\n\tk=0:\tbuild from scratch\n\tk=1:\tbuild from modification\n\tk=2:\trestart\n\tk=3:\tstart_switch\n\tk=4:\tkill_switch\n'
    exit(0)


#1. generate topo file
generate_new_topofile()

#2. start every switch
auto_login_and_build(sys.argv[1])

