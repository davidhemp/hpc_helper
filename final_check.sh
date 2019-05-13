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
  errorout "Still can not ssh to $NODENAME"
fi

rtn=`ssh $NODENAME "uptime"`
if [ $? -ne 0 ] ; then
  errorout "Still can not ssh to $NODENAME"
else
  echo "Can ping and ssh to node"
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
esac

rtn=`ssh $NODENAME "systemctl status slurmd"`
if [ $? -ne 0 ] ; then
    echo "Slurmd is not running on $NODENAME"
else
    echo "Slurmd present and running"
fi
