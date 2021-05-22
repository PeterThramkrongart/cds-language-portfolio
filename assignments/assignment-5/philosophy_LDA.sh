#!/usr/bin/env bash

# make the environment
bash create_lda_venv.sh

source lda_venv/bin/activate

cd src

#run the script
python philosophy_LDA.py

cd ..

deactivate

# kill the environment
bash kill_lda_venv_venv.sh