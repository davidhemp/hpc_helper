#!/bin/bash
# This script should rebuild a node if it is uncontactable via ping or ssh


NODENAME=$1

errorout() {
  echo $1
  exit 1
}

sleep_countdown() {
  secs=$1
  while [ $secs -gt 0 ]; do
    echo -ne "$secs\033[0K\r"
    sleep 1
    : $((secs--))
  done
}

rebuild_node() {
  rpower $NODENAME boot
#  sleep_countdown 600
}

rebuild_node $NODENAME
