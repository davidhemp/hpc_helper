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

# Check node has been up long enough for everthing to start
rtn=$(ssh $NODENAME "cat /proc/uptime")
if [ $? -ne 0 ] ; then
  errorout "Still can not ssh to $NODENAME"
else
  echo "Can ping and ssh to node"
  uptime=$(echo $rtn | awk '{ print $1 }' | cut -d. -f 1)
  if [[ $uptime -lt 600 ]] ; then
    errorout "Node is still booting, wait 10 minutes"
  fi
fi
echo "Node should have finished booting, checking state"

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
  *)
    echo "PBS issue, check error"
    echo $PBS_STATE
    exit 1
esac


### Hardware
MEM_STATE=`ssh green0712 "free -g | grep Mem:" | awk {' print $2 '}`
if [ $MEM_STATE -ne 63 ] ; then 
  errorout "Memory missing!!"
else
  echo "All memory present"
fi

