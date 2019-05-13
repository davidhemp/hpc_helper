NODENAME=$1

errorout() {
  echo $1
  exit 1
}

check_is_down() {
  cmd="scontrol show node $NODENAME | grep State"
  state="$(ssh blue51 ${cmd} | awk {' print $1 '})"
  if echo "$state" | grep -qi "Down" || echo "$state" | grep -qi "Drain"; then
    echo "Slurm has marked $NODENAME as down or drained"
    return 1
  fi
  return 0
}

check_slurmd () {
  ssh $NODENAME "systemctl is-active --quiet slurmd"
  return $?
}

# Check that the node is even marked as down
if check_is_down ; then
  echo "$NODENAME is not marked as down or drained, no fix needed"
  exit 0
fi

#Return code 2 is server loaded but not started
check_slurmd
if [ $? -eq 3 ] ; then
  echo "Attempting restart slurmd"
  if ! ssh $1 "systemctl restart slurmd"; then
    errorout "Could not restart slurmd, no common fix found"
  fi
  if ! check_slurmd $NODENAME ; then
    errorout "Restart command sent but server didn't restart"
  fi
fi

# Double check that the node is now free for jobs
if ! check_slurmd $NODENAME; then
  errorout "Failed to restart slurmd on $NODENAME, no common fix found"
else
  echo "$NODENAME should be working and in the queue"
  exit 0
fi

