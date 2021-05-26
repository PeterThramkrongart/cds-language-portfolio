#!/usr/bin/env bash

VENVNAME=network_analysis_venv

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate
pip install --upgrade pip

pip install ipython
pip install jupyter

python -m ipykernel install --user --name=$VENVNAME

test -f requirements.txt && pip install -r requirements.txt

python -m spacy download en_core_web_sm

#pip freeze | grep -v "pkg-resources" > requirements.txt

deactivate
echo "build $VENVNAME"
