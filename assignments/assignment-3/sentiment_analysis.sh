#!/usr/bin/env bash

# make the environment
bash create_sentiment_analysis_venv.sh

source sentiment_analysis_venv/bin/activate

cd src

#run the script
python sentiment_analysis.py

cd ..

deactivate

# kill the environment
bash kill_sentiment_analysis_venv.sh