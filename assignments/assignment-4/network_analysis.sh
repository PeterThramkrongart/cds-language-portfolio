#!/usr/bin/env bash

# make the environment
bash create_network_analysis_venv.sh

source network_analysis_venv/bin/activate

cd src

#run the scripts

python create_network_data.py
python network_analysis.py -l -p

cd ..

deactivate

# kill the environment
bash kill_network_analysis_venv.sh