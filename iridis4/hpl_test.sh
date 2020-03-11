#!/bin/bash

pbsnodes -c green0435
setres -u dwh1d17 -s 09:00_04/25/2019 -e 18:00_10/25/2019 'green0435'
qsub -l nodes=green0435:ppn=16 /home/dwh1d17/scratch/hpl/hpl-2.2/bin/16core/sub_16.pbs
