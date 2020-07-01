#!/bin/bash
export PATH=/local/software/conda/anaconda3/bin/:$PATH
source activate serviceline
python update_database.py
