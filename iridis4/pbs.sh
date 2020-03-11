#!/bin/bash
# This script will re-add a node to the queue. As such it should be 
# the last script to run in common fixes.


NODENAME=$1

errorout() {
  echo $1
  exit 1
}

check_is_down() {
  cmd="pbsnodes $NODENAME | grep 'state = '"
  state="$(ssh blue101 ${cmd} | awk {' print $3 '})"
  if [ $state == "down" ] || [ $state == "drained" ]; then
    echo "PBS has marked $NODENAME as down or drained"
    return 1
  fi
  return 0
}

check_pbs_mom () { 
  ssh $NODENAME "service pbs_mom status"
  return $?
}

# Check that the node is even marked as down
if check_is_down ; then
  echo "$NODENAME is not marked as down or drained, no fix needed"
  exit 0
fi

#Return code 2 is server loaded but not started
check_pbs_mom
if [ $? -eq 2 ] ; then
  echo "Attempting restart pbs_mom serice"
  if ! ssh $1 "service pbs_mom restart"; then
    errorout "Could not restart PBS_mom, no common fix found"
  fi
  if ! check_pbs_mom $NODENAME ; then
    errorout "Restart command sent but server didn't restart"
  fi
fi

# Double check that the node is now free for jobs
if ! check_pbs_mom $NODENAME; then
  errorout "Failed to restart pbs_mom on $NODENAME, no common fix found"
else
  echo "$NODENAME should be working and in the queue"
  exit 0
fi
