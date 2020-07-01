#!/bin/bash
module load conda
source activate serviceline
echo "Checking for Iridis Applications"
python Iridis_applications.py
#echo "Checking for Lyceum Applications"
#python Lyceum_applications.py
