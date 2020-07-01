NODE_LIST=`scontrol show hostname ${1} | sort -u`
for NODENAME in ${NODE_LIST}; do
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
  echo "Can ping and ssh to ${NODENAME}"
fi


### Services
GPFS_STATE=`ssh $NODENAME "mmgetstate"`
case "$GPFS_STATE" in
  *active*)
    echo "GPFS Active"
    ;;
  *)
    echo "GPFS issue, attempting fix"
    ./gpfs.sh $NODENAME
esac

### Slurm
./slurm.sh $NODENAME

### Check hardware
TOTAL_MEM=`ssh $NODENAME "free -h | grep Mem: "| awk {'print $2'}`
if [[ "$TOTAL_MEM" = "188G" ]]; then
    echo "All ram found"
else
    echo "$NODENAME is missing RAM, $TOTAL_MEM found"
fi
done
