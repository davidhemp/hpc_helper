#!/bin/bash
echo $(date)
cd "$(dirname "$0")"
. /local/software/python/3.7.3/bin/activate
export PYTHONPATH=$(pwd)/venv
export PATH=$(pwd)/venv/bin/:$PATH
python main.py
echo "Done"
