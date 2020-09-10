#!/bin/bash
# Empty list to input values
node_set=""
node_list=""

# Get data
node_map=$(mmfsadm dump cfgmgr | egrep "c0n" | grep "10.13" | awk '{ print $3, "  ", $2 }')
node_requests=$(ssh violet55 mmfsadm dump nsd | grep nsdId | awk '{ print $8 }')

#Process data
for request in $node_requests; do
  new_node=$(echo $node_map | grep -o -E "[a-z]{1,6}[0-9]{1,3} $(echo $request | cut -d, -f1)" | awk '{ print $1 }')
  node_list="${node_list} ${new_node}"
  if ! echo ${node_set} | grep -q "${new_node}"; then
    node_set="${node_set} ${new_node}"
  fi
done


export LD_LIBRARY_PATH=/local/software/slurm/default/lib:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=/local/software/slurm/default/lib/slurm:${LD_LIBRARY_PATH}
export PATH=/mainfs//local/software/slurm/default/bin:${PATH}
echo $(hostname)
echo $(uptime)
echo "-------------------"
echo "Node | owner | count"
echo "-------------------"
for node in $node_set; do
  count=$(echo $node_list | grep -o $node | wc -l)
  #user=$(/mainfs//local/software/slurm/default/bin/scontrol show node=${node} | grep -oe "Owner=[a-z0-9]*" | cut -d= -f2)
  echo "${node} | ${user} | ${count}"
done
echo "-------------------"
