#!/bin/bash
# Final checks before node is returned to service

## Setup and helper scripts
errorout() {
  echo $1
  exit 1
}

if [ -z $1 ] ; then
  errorout "Input node name not given"
fi
NODENAME=$1


## Checks
### Connection checks
rtn=`ping -c 1 $NODENAME`
if [ $? -ne 0 ] ; then
  #### Assuming the newest messages file is relavent
  PAST_MESSAGE_LOG=$(ls -str /var/log/messages-* | tail -n 1 | awk {' print $2 '})
  zgrep $NODENAME $PAST_MESSAGE_LOG > /dev/shm/dwh1d17/${NODENAME}-messages
  cat /dev/shm/dwh1d17/${NODENAME}-messages $(grep $NODENAME /var/log/messages) | less
  read -p "Node is unconnectable, do you which to power cycle the node? " choice
  case "$choice" in
    yes|Yes) 
	./rebuild $NODENAME
	echo "Node has been set to rebuild, re-run checks in 10 minutes"
	exit 0
	;;
    no|No)  errorout "Unable to ssh to $NODENAME";;
    *) echo "Invalid input";;
  esac
fi
echo "Node pingable"

# Check node has been up long enough for everthing to start
rtn=$(ssh $NODENAME "cat /proc/uptime")
if [ $? -ne 0 ] ; then
  errorout "Still can not ssh to $NODENAME"
else
  uptime=$(echo $rtn | awk '{ print $1 }' | cut -d. -f 1)
  if [[ $uptime -lt 600 ]] ; then 
    errorout "Node is still booting, wait 10 minutes"
  fi
fi
echo "Node should have finished booting, checking state"

### Hardware
MEM_STATE=`ssh green0712 "free -g | grep Mem:" | awk {' print $2 '}`
if [ $MEM_STATE -ne 63 ] ; then 
  errorout "Memory missing!!"
else
  echo "All memory present"
fi

### Services
GPFS_STATE=`ssh $NODENAME "mmgetstate"`
case "$GPFS_STATE" in
  *active*)
    echo "GPFS Active"
    ;;
  *)
    echo "GPFS issue, check error"
    echo $GPFS_STATE
    exit 1
esac

PBS_STATE=`ssh $NODENAME "service pbs_mom status"`
case "$PBS_STATE" in
  *running*)
    echo "PBS Active"
    ;;
  'pbs_mom dead but subsys locked')
    echo "Need to restart pbs_mom"
    ./pbs.sh $NODENAME
    ;;
  *)
    echo "PBS issue, check error"
    echo $PBS_STATE
    exit 1
esac


