#!/bin/bash

### Helper functions
errorout() {
  echo $1
  exit 1
}

### Input varibles
if [ -z "$1"]; then
    errorout "Need node name"
else
    NODENAME=$1
fi


if [ -z "$2"]; then
    echo "Machine not set, defaulting to 7x21"
    NODETYPE="7x21"
else
    NODETYPE=$2
fi
PASSWD=`cat .keys/USERID`
### Main script
/root/onecli/OneCli update acquire --mt $NODETYPE --ostype rhel7 --dir /root/FW/7X21

/root/onecli/OneCli update flash  --platform rhel7 --bmc USERID:'$PASSWD'@$NODENAME-ipmi --dir /root/FW/7X21

