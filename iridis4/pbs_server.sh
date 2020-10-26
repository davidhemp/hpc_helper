#!/bin/bash

ssh_error_check(){
    ssh $1 $2
    if [[ $? -ne 0 ]] ; then
      exit 1
    fi
    return 0
}

rtn=`ssh blue101 "top -b -n 1 | grep pbs_server"`
MEM_PERCENT=$(echo $rtn | awk '{ print $10 }' | cut -d. -f1)

if [[ $MEM_PERCENT -gt 30 ]]; then
    echo "PBS Server is over 30% of system memory, restarting service"
    # Check both services are running as normal
    ssh_error_check blue102 "service pbs_server status"
    ssh_error_check blue101 "service pbs_server status"
    # Shutdown in reverse order to prevent fail over
    ssh_error_check blue102 "service pbs_server stop"
    sleep 5
    ssh_error_check blue101 "service pbs_server stop"
    sleep 5
    # Start up in the correct order with a pause to ensure blue101 is up.
    ssh_error_check blue101 "service pbs_server start"
    sleep 60
    ssh_error_check blue102 "service pbs_server start"
fi
