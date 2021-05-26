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
For this project we choose to only use books in the paperback and hardback formats assuming that most else will be duplicates of the paperbacks and hardbacks. As the data contained books from multiple languages, we used _Spacy's_ module _Fastlang_ to detect only books whose description is in the English. Also, used _Spacy_ to tokenize a lemmatize book descriptions. Lastly, we dropped books with missing values and duplicates resulting in XXXX unique titles.
The cleaning code can be found in the _prepare_data.sh_ script in the src folder.


__Recommender__

normalize - number of reviews, rating score
tfidf book description

Count vectorize - genres, author

cosine similarity - tfidf description, genres, author

We used sklearn tfidf vectorizer to create a matrix out of the book descriptions. Tfidf is generally used to express how important a words in a document is based on how many times it occurs within that document and how many times within all the documents. This leaves us with a good measure of how relevant each word in the book's description is. 

For the genre and author we used sklearn's count vectorizer to 





## Results

```
|book_title                       |book_authors                        |genres                                                                    | rec_score|
|:--------------------------------|:-----------------------------------|:-------------------------------------------------------------------------|---------:|
|A Collection of Essays           |George Orwell                       |Writing, Essays, Nonfiction, Classics, Politics, Literature, Philosophy   | 1.0000000|
|Animal Farm / 1984               |George Orwell, Christopher Hitchens |Classics, Fiction, Science Fiction, Dystopia, Literature, Science Fiction | 0.9189596|
|Animal Farm                      |George Orwell                       |Classics, Fiction, Science Fiction, Dystopia, Fantasy, Literature         | 0.9107122|
|Nineteen Eighty-Four             |George Orwell                       |Classics, Fiction, Science Fiction, Science Fiction, Dystopia             | 0.8405285|
|Down and Out in Paris and London |George Orwell                       |Nonfiction, Classics, Biography, Autobiography, Memoir, Travel            | 0.8336836|
|Keep the Aspidistra Flying       |George Orwell                       |Fiction, Classics, European Literature, British Literature, Literature    | 0.7785718|
|Shooting an Elephant             |George Orwell                       |Nonfiction, Classics, Short Stories, Writing, Essays, Politics            | 0.7247096|
|Homage to Catalonia              |George Orwell, Lionel Trilling      |History, Nonfiction, Politics, Classics, War, Autobiography, Memoir       | 0.6990492|
|Coming Up for Air                |George Orwell                       |Fiction, Classics, Novels                                                 | 0.6568643|
|The Road to Wigan Pier           |George Orwell, Richard Hoggart      |Nonfiction, History, Classics, Politics, Sociology                        | 0.6183259|
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
