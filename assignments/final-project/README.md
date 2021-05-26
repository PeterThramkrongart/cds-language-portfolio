Self-assigned Assignment - Book Recommender
==============================
**Peter Thramkrongart and Jakub Raszka**

##	Github link

Link to the repository: https://github.com/PeterThramkrongart/cds-language-portfolio.git

Link to the assignment folder: https://github.com/PeterThramkrongart/cds-language-portfolio/tree/main/assignments/final-project

## Contribution

Both Peter Thramkrongart and Jakub Raszka contributed equally to every stage of this project from initial conception and implementation, through the production of the final output and structuring of the repository. (50/50%)

##  Description

In this project, the goal is to create a  content-based book recommender using a  short book description, its rating, genre, and number of reviews. To do so, we used  

## Methods

__Data__

Originally we wanted to use the continuously updated _"Goodreads Book Datasets With User Rating 10M"_ (https://www.kaggle.com/bahramjannesarr/goodreads-book-datasets-10m). This is a very extensive data set with a lot of recent and well documented information. Problematically, it does not contain book summaries for the first 600k entries. Those entries are where most of the good and well known books are, so we had to find another dataset. We then stumbled upon a 8+ GB datased containing over 2.3 million books (https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/books?authuser=0). All that was contained in a single JSON file that we could not download using wget or other automatized download methods. Furthermore, we don't think the size and the trouble of the dataset is justified given the small size of this project. We settled for smaller, but much more concise, dataset which contains only 52 932 best-rated books (https://www.kaggle.com/meetnaren/goodreads-best-books). Although it has only has a fraction of the other datasets, we still deem the number of books sufficient, because those books were selected from a "best of" list. Our chosen dataset was not without problems, though. The ISBN codes were corrupted, so we could no longer discern title duplicates from one another as easily, and it prohibited enriching the dataset with information from other datasets. The dataset comes with images for each entry. We did not use the images for this project, so we choose to delete them, thereby, making the dataset below 100mb (the github size threshold).

__Data pre-processing__

The data required some pre-processing. Specifically, we dropped all duplicated books to have only one entry per one book. We also decided to keep only books with 50 and more reviews on goodreads for the sake of optimalisation assuming that a reader has a still many thousands books to choose from.

The dataset also contained some books in different languages. To ensure that only English-written books are included, we used a module called _Spacy FastLang_
(https://github.com/thomasthiebaud/spacy-fastlang) which adds a language detection functionality into the _Spacy_ world.  The module utilizes facebook’s library called _fastText_ (https://github.com/facebookresearch/fastText) which is a very extensive library of word embeddings and text classifications. We managed to filter out most non-english books but we weren’t 100 % successful. We further used _Spacy_ to lemmatize our book summaries. After the pre-processing, the contained only 23 266 unique English books.

We z-score scaled all numeric values. This allows us to use them as weights in the final recommender ranking. Using sklearns vectorizers, we created count vectors of the author and genre columns, and tfidf vectors of the book summaries. We used a seperator for splitting the authors and genres columns instead of tokenizing single words. This allowed us too keep George Orwell separate from George Saunders and to keep Science Fiction separate from Historical Fiction. The tfidf vectorizer used unigrams, bigrams and trigrams and deleted regular English stopwords.

The dataframe was saved as a .csv and the vectorized columns were saved in Numpy's proprietary binary format for fast loading, when using the recommender.

__Recommender__

The recommender itself is very simple. it loads the processed data, and calculates similarity scores for each vectorized variable using cosine similarity and z-score scales them to math the other variables. After that it it calculates a final recommendation score by adding a together the different scaled scores timed by their individual weights. The score is min max scaled, to be of the same size no matter the weights. The score is no way universal, but gives some aid, when comparing accross recommendations. Normalizing the score makes it easier to understand the distribution of scores in the final recommendation. It finally sorts the full dataset based on the recommendation score, and outputs the head of the dataset.

The weighting scheme in Python code:

```python
df["rec_score"] = df.tfidf_sim*tfidf_weight+df.genres_sim*genre_weight+df.book_review_count*review_count_weight+df.book_rating*rating_weight+df.authors_sim*authors_weight
```


## Results
We find that it is difficult to reliably produce good content based recommendations that work well in all scenarios. Most of the time our recommendations a somewhat logical. We are heavily reliant on clean data, and our recommendations shows that our preprocessing still let many errors slip through. We still find it difficult to capture different editions. E.g. in the case of Animal Farm/ 1984 where the books have been joined together to form a new third book. Our scheme for language detection was also far from perfect as shown in the recommendations based on Ulysses by James Joyce. We believe that some summaries are in english, but the books themselves are translations of other works. Our recommender tend to also recommend book compilations and spinoff works as shown in the recommendations based on The Hunger Games and A Game of Thrones.This is can maybe be avoided using a much more advanced embedding scheme, that can capture the feel and themes of the books and filter out named entities. But in general, that is where collaborative filtering methods (recommendations based on what other people liked) are much better suited. Finally, we are rather satisified with our interactive weighting scheme. The default settings emphasizes the similarities in summaries, authors and genres. To combat getting spinoff works, one may deamphasize authors or summaries, and mainly go on genre, with fairly acceptable results as shown in in the recommendations based on A Feast for Crows vs A Game of Thrones. The recommendations based on AFFC demphasized authors, to find similar books, but from other authors.

Top 10 recommendations based on 1984 by George Orwell:

```
|book_title                       |book_authors                        | rec_score|
|:--------------------------------|:-----------------------------------|---------:|
|A Collection of Essays           |George Orwell                       | 1.0000000|
|Animal Farm / 1984               |George Orwell, Christopher Hitchens | 0.9189596|
|Animal Farm                      |George Orwell                       | 0.9107122|
|Nineteen Eighty-Four             |George Orwell                       | 0.8405285|
|Down and Out in Paris and London |George Orwell                       | 0.8336836|
|Keep the Aspidistra Flying       |George Orwell                       | 0.7785718|
|Shooting an Elephant             |George Orwell                       | 0.7247096|
|Homage to Catalonia              |George Orwell, Lionel Trilling      | 0.6990492|
|Coming Up for Air                |George Orwell                       | 0.6568643|
|The Road to Wigan Pier           |George Orwell, Richard Hoggart      | 0.6183259|
```

Top 10 recommendations based on Ulysses by James Joyce:

```
|book_title                                 |book_authors                                            | rec_score|
|:------------------------------------------|:-------------------------------------------------------|---------:|
|Дъблинчани/ Портрет на художника като млад |James Joyce, Джеймс Джойс, Асен Георгиев Христофоров... | 1.0000000|
|Finnegans Wake                             |James Joyce                                             | 0.9937516|
|A Portrait of the Artist as a Young Man    |James Joyce, Seamus Deane                               | 0.9635664|
|Dubliners                                  |James Joyce, Terence Brown, Colum McCann, Roman Muradov | 0.9014175|
|Eveline                                    |James Joyce                                             | 0.8856827|
|Elmer Gantry                               |Sinclair Lewis                                          | 0.4147498|
|The Last Temptation of Christ              |Nikos Kazantzakis, Nikos Kazantzakis, Peter A. Bien     | 0.4130681|
|Tropic of Capricorn                        |Henry Miller                                            | 0.3965215|
|The Sound and the Fury                     |William Faulkner                                        | 0.3933700|
|Sometimes a Great Notion                   |Ken Kesey, Charles Bowden                               | 0.3870019|

```

Top 10 recommendations based on The Hunger Games by Suzanne Collins:

```
|book_title                             |book_authors    | rec_score|
|:--------------------------------------|:---------------|---------:|
|Mockingjay                             |Suzanne Collins | 1.0000000|
|Catching Fire                          |Suzanne Collins | 0.9928887|
|The Hunger Games Trilogy Boxset        |Suzanne Collins | 0.5725807|
|The World of the Hunger Games          |Kate Egan       | 0.5240631|
|The Hunger Games Tribute Guide         |Emily Seife     | 0.4442769|
|Gregor and the Prophecy of Bane        |Suzanne Collins | 0.4304272|
|Gregor and the Code of Claw            |Suzanne Collins | 0.4160059|
|Gregor and the Curse of the Warmbloods |Suzanne Collins | 0.4012589|
|Gregor and the Marks of Secret         |Suzanne Collins | 0.4001130|
|Gregor the Overlander                  |Suzanne Collins | 0.3842942|
```

Top 10 recommendations based on A Game of Thrones by George R.R. Martin:

```
|book_title                                                                        |book_authors         | rec_score|
|:---------------------------------------------------------------------------------|:--------------------|---------:|
|A Storm of Swords                                                                 |George R.R. Martin   | 1.0000000|
|Tormenta de espadas                                                               |George R.R. Martin   | 0.6612630|
|A Game of Thrones: The First 5 Books                                              |George R.R. Martin   | 0.4452066|
|A Clash of Kings                                                                  |George R.R. Martin   | 0.3666152|
|A Dance with Dragons 2: After the Feast                                           |George R.R. Martin   | 0.3473805|
|The World of Ice and Fire: The Untold History of Westeros and the Game of Thrones |George R.R. Martin...| 0.3131561|
|A Dance with Dragons                                                              |George R.R. Martin   | 0.3106538|
|A Storm of Swords: Steel and Snow                                                 |George R.R. Martin   | 0.3098506|
|A Storm of Swords: Blood and Gold                                                 |George R.R. Martin   | 0.3054644|
|A Dance with Dragons: Dreams and Dust                                             |George R.R. Martin   | 0.2973343|
```
Top 10 recommendations based on A Feast for Crows by George R.R. Martin. These recommendations deemphasizes the authors by -1.0:

```
|book_title                                                                  |book_authors      | rec_score|
|:---------------------------------------------------------------------------|:-----------------|---------:|
|The Iron Fey Boxed Set: The Iron King, The Iron Daughter, The Iron Queen... |Julie Kagawa      | 1.0000000|
|King of Thorns                                                              |Mark  Lawrence    | 0.8882314|
|Treason                                                                     |Orson Scott Card  | 0.8856870|
|Malice                                                                      |John Gwynne       | 0.8829934|
|The Iron Legends                                                            |Julie Kagawa      | 0.8807191|
|The Name of the Wind                                                        |Patrick Rothfuss  | 0.8739155|
|The Iron Man: [A Children's Story In Five Nights]                           |Ted Hughes        | 0.8738872|
|Kings or Pawns                                                              |J.J. Sherwood     | 0.8735123|
|Words of Radiance                                                           |Brandon Sanderson | 0.8726171|
|Black Wolves                                                                |Kate Elliott      | 0.8722374|
```

## Reproducibility

**Step 1: Clone repository:**  

- Open a Linux terminal

- Navigate the destination of the repository

- Run the following command  

```console
 git clone https://github.com/PeterThramkrongart/cds-language-portfolio.git
``` 

**step 2: Set up the environment and activate it:**  

- Navigate to the folder "final-project" 

```console
cd assignments/final-project
```  
- We have written a bash script _create_book_recommender_venv.sh_ to set up a virtual environment: 

```console
bash create_book_recommender_venv.sh

source book_recommender_venv/bin/activate
```  

**step 3: Prepare data:**  

- Navigate to the folder "src":  

```console
cd src
```  

- Run the python script _prepare_data.py_ to clean the dataset and create necessary matrices:

 ```console
python prepare_data.py
```

**step 4: Run the recommender:**  

- Run the python script _recommender.py_ with the optional arguments:

```console
        flags: -t,   --title,               default = 1984, type = str, 
                help = str, Title to base recommendations on

        flags: -tw,  --tfidf_weight,        default = 1,    type = float, 
                help = float, The weight of tfidf on recommendations

        flags: -aw,  --authors_weight,      default = 0.2,  type = float, 
                help = float, The weight of authors on recommendations

        flags: -gw,  --genre_weight,        default = 0.8,  type = float, 
                help = "loat, The weight of genre on recommendations
        
        flags: -rcw, --review_count_weight, default = 0.2,  type = float, 
                help = float, The weight of review counts on recommendations

        flags: -rw,  --rating_weight,       default = 0.3,  type = float, 
                help = float, The weight of ratings on recommendations
```  

- Make sure that the book's title matches perfectly with the book's title on Goodreads


```console
python recommender -t "The Hunger Games" -tw 1.0 -aw -5.0 -gw 0.3 -rcw 0.0 -rw 2.0

```  
- Note: The dataset was collected in 2017 so books published after cannot be used

**step 5 (optional): Kill the environment:**  

- Navigate to the folder "final-project"

```console
cd ..
```  

- Run the bash script _kill_book_recommender_venv.sh_ to remove the virtual environment:  

```console
bash kill_network_analysis_venv.sh
```  

## Running the project on something else than Linux

Our projects are mainly made for Linux/Mac users. Our python scripts should run on any machine, though our bash scripts may not work. For this case, we recommend using the python distribution system from https://www.anaconda.com/ to set up environments using our requirements.txt files.

Project Organization
------------
The folder structure of our projects is based on a simplified version of the cookiecutter data science folder structure https://drivendata.github.io/cookiecutter-data-science/. For the sake of generalizability, some folders will remain empty for some projects, but overall this will make folder navigation easier.




    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── utils              <- utility scripts with reusable functions and classes
    |  └──__init__.py      <- Makes utils a Python module
    |
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    |
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   ├── figures        <- Generated graphics and figures to be used in reporting
    │   └── recommendations<- Csv files with saved recommendations for a given book.
    |
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    └── src                <- Source code for use in this project.
    └── __init__.py    <- Makes src a Python module
--------
