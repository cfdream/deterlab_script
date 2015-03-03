#!/bin/bash 

if [ $# -ne 1 ]; then
    echo "usage: sh -x loginC1H1H2_initial.sh restart  : restart"
    echo "usage: sh -x loginC1H1H2_initial.sh stop : stop"
    exit
fi

if [ "$1" == "restart" ]; then
    #1. controller c1.mscm.vcrib
    ssh c1.mscm.vcrib "sudo pkill controller; cd controller; \
        nohup ./controller > foo.out 2> foo.err < /dev/null &"

    #2. host2 h2.mscm.vcrib
    ssh h2.mscm.vcrib "cd /users/xuemei/deterlab_script; python dumpAndCheckAtH2.py"

    #3. host1 h1.mscm.vcrib
    ssh h1.mscm.vcrib "cd /users/xuemei/deterlab_script; python replayAtH1.py"
elif [ "$1" == "stop" ]; then
    #1. controller c1.mscm.vcrib
    ssh c1.mscm.vcrib "sudo pkill controller"

    #2. host2 h2.mscm.vcrib
    ssh h2.mscm.vcrib "sudo pkill tcpdump; sudo pkill detect"

    #3. host1 h1.mscm.vcrib
    ssh h1.mscm.vcrib "sudo pkill tcpreplay"
fi
