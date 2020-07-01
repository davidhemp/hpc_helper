NODENAME=$1

if [ -z "$2"]; then
    JUSTCHECK=0
else
    JUSTCHECK=$2
fi


errorout() {
  echo $1
  exit 1
}

check_is_down() {
  cmd="scontrol show node $NODENAME | grep State"
  state="$(ssh blue51 ${cmd} | awk {' print $1 '})"
  if echo "$state" | grep -qi "Down" || echo "$state" | grep -qi "Drain"; then
    echo "Slurm has marked $NODENAME as down or drained"
    return 0
  fi
  return 1
}

check_slurmd () {
  ssh $NODENAME "systemctl is-active --quiet slurmd"
  return $?
}

if check_is_down ; then
  if check_slurmd $NODENAME; then
    echo "$NODENAME should be working and in the queue"
    exit 0
  else
    if [ $JUSTCHECK -eq 1 ]; then # If just running checks then don't try fix
      echo "Slurmd is down on $NODENAME"
    else
      echo "Attempting restart slurmd"
      ssh $NODENAME "systemctl restart slurmd"
      if ! check_slurmd $NODENAME ; then
        errorout "Restart command sent but server didn't restart"
      else
        echo "Slurm deamon is now running"
      fi
    fi
  fi
fi
