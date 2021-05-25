#!/usr/bin/env bash

# make the environment
bash create_book_recommender_venv.sh

source book_recommender_venv/bin/activate

cd src

#run the script
#python GOT_classification.py

cd ..

deactivate

# kill the environment
bash book_recommender_venv_venv.sh