#!/usr/bin/env bash

# make the environment
bash create_network_visualization_venv.sh

source network_visualization_venv/bin/activate

cd src

#run the script
python network_analysis.py

cd ..

deactivate

# kill the environment
bash kill_network_visualization_venv.sh