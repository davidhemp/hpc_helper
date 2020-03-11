#!/bin/bash

#/local/bin/nodes_free down > nodes_down
line=$(tail -n 1 nodes_down)
nodes="${line//[,]/ }"

for node in $nodes; do
  echo $node
  ./fix_node.sh $node
#  ./final_checks.sh $node
  echo ""
done
