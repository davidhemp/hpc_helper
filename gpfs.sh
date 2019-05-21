#!/bin/bash
NODENAME=$1
WORKINGNODE="red100"

errorout() {
  echo $1
  exit 1
}

rebuild_gpfs () {
  # Ensure the node as a usable copy of mmsdrfs
  if ! scp $2:/var/mmfs/gen/mmsdrfs $1:/var/mmfs/gen/mmsdrfs; then
  errorout "Could not copy mmsdrfs from $2 to $1"
  fi

  # Make sure GPFS is stopped on node
  ssh $1 "mmshutdown -N $1"

  # Re-add node to GPFS cluster
  if ! mmdelnode $1; then
    errorout "Could not remove $1 from GPFS cluster" ; 
  fi
  if ! mmaddnode $1; then
    errorout "Could not add $1 to GPFS cluster" ; 
  fi
  if ! mmchlicense client --accept -N $1; then
    errorout "Could not accept a client license for node $1"
  fi

  # Starting up GPFS on node
  if ! mmstartup -N $1; then
    errorout "GPFS startup command failed for $1"
  fi
  state=$(mmgetstate -N $NODENAME | awk '{ print $3 }')
  if [ "$state" != "active" ]; then
    errorout "GPFS still failed to start"
  fi
}

simple_fix() {
  echo "Attempting to restart GPFS"
  mmstartup -N $1 
  sleep 10
  if ! check_gpfs_state $1; then
    echo "Node is still down"
    return 1
  fi
  return 0
}

check_gpfs_state () {
  state=$(mmgetstate -N $1 | grep $1 | awk '{ print $3 }')
  if [ "$state" == "unknown" ] || [ "$state" == "down" ]; then
    echo "$1 is in an unknown or down state"
    return 1
  elif [ "$state" == "active" ]; then
    echo "GPFS is active on $1"
    return 0
  fi
  return 0
}

check_ib_status () {
  if ! ssh $1 "ibstatus"; then
    errorout "IB is not available on $1, no common fix found."
  fi
  return 0
}

check_ib_status $NODENAME
if ! check_gpfs_state $1; then
  if ! simple_fix $NODENAME; then
    echo "Simple fix didn't work, trying a more complex method"
    check_gpfs_state $WORKINGNODE
    rebuild_gpfs $NODENAME $WORKINGNODE
  fi
fi
