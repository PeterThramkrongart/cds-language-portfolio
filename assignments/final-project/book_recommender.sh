#!/usr/bin/env bash

# make the environment
bash create_book_recommender_venv.sh

source book_recommender_venv/bin/activate

cd src

#run the script
python prepare_data.py

python recommender.py -t "The Hunger Games"
python recommender.py -t "1984"
python recommender.py -t "The Idiot"
python recommender.py -t "The Dark Tower"
python recommender.py -t "Meditations"
python recommender.py -t "Harry Potter and the Sorcerer's Stone"
python recommender.py -t "Ulysses"
python recommender.py -t "A Game of Thrones"
python recommender.py -t "A Feast for Crows" -aw -1.0


cd ..

deactivate

# kill the environment
bash kill_book_recommender_venv.sh