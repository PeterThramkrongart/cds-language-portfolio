#!/usr/bin/env bash

# make the environment
bash create_got_venv.sh

source got_venv/bin/activate

cd src

#run the script
python GOT_classification.py

cd ..

deactivate

# kill the environment
bash kill_got_venv.sh