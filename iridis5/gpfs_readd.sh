#!/bin/bash

errorout() {
  echo $1
  exit 1
}


  # Ensure the node as a usable copy of mmsdrfs
  if ! rsync -av /var/mmfs/gen/mmsdrfs $1:/var/mmfs/gen/mmsdrfs; then
  errorout "Could not copy mmsdrfs from local node to $1"
  fi

  # Make sure GPFS is stopped on node
  ssh $1 "mmshutdown -N $1"

  # Re-add node to GPFS cluster
  if ! mmdelnode -N $1; then
    errorout "Could not remove $1 from GPFS cluster" ;
  fi
  if ! mmaddnode -N $1; then
    errorout "Could not add $1 to GPFS cluster" ;
  fi
  if ! mmchlicense client --accept -N $1; then
    errorout "Could not accept a client license for node $1"
  fi

  # Starting up GPFS on node
  if ! mmstartup -N $1; then
    errorout "GPFS startup command failed for $1"
  fi
  sleep 30 
  state=$(mmgetstate -N $1 | awk '{ print $3 }')
  if [ "$state" != "active" ]; then
    errorout "GPFS still failed to start"
  fi
