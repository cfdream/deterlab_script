#!/bin/bash 

ssh s1.mscm.vcrib "ps aux | grep ovs-vswitchd"
ssh s2.mscm.vcrib "ps aux | grep ovs-vswitchd"
ssh s3.mscm.vcrib "ps aux | grep ovs-vswitchd"
ssh s4.mscm.vcrib "ps aux | grep ovs-vswitchd"

ssh s1.mscm.vcrib "ps aux | grep ovsdb-server"
ssh s2.mscm.vcrib "ps aux | grep ovsdb-server"
ssh s3.mscm.vcrib "ps aux | grep ovsdb-server"
ssh s4.mscm.vcrib "ps aux | grep ovsdb-server"
