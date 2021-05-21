#!/usr/bin/env bash

VENVNAME=sentiment_analysis_venv

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate
pip install --upgrade pip

pip install ipython
pip install jupyter


python -m ipykernel install --name=$VENVNAME --user

test -f requirements.txt && pip install -r requirements.txt

pip freeze | grep -v "pkg-resources" > requirements.txt

# Spacy and spacytext blob requires these modules
python -m spacy download en_core_web_sm
python -m textblob.download_corpora

deactivate
echo "build $VENVNAME"