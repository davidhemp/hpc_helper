#!/bin/bash
date

export PATH=/local/software/conda/miniconda-py3-new/bin:${PATH}
export CONDA_PKGS_DIRS=/scratch/dwh1d17/.conda-temp/py3
cd /home/dwh1d17/tools/hpc_helper/serviceline

source activate serviceline
echo "Checking for Iridis Applications"
python Iridis_applications.py
echo "Checking for Lyceum Applications"
python Lyceum_applications.py
