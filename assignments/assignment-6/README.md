Assignment 6 - Text Classification Using Deep Learning (GoT)
==============================
**Peter Thramkrongart and Jakub Raszka**

##	Github link

Link to the repository: https://github.com/PeterThramkrongart/cds-language-portfolio.git

Link to the assignment folder: https://github.com/PeterThramkrongart/cds-language-portfolio/tree/main/assignments/assignment-6

## Contribution

Both Peter Thramkrongart and Jakub Raszka contributed equally to every stage of this project from initial conception and implementation, through the production of the final output and structuring of the repository. (50/50%)

##  Description

_Winter is coming..._

In this assignment, the we are supposed to use deep learning models like CNNS for classifying a specific kind of cultural data - scripts from the TV series Game of Thrones (https://www.kaggle.com/albenft/game-of-thrones-script-all-seasons). The task is to find out how accurately we can model the relationship between each season and the lines spoken. That is to say - is it possible to predict which season a line comes from? Or to phrase that another way, is dialogue a good predictor of season?

You should:
- build a baseline model with using logistic regression and count vectorization for pre-processing
- build a deep learning model 
- choose the best method for data pre-processing (TFIDF vectorizer, Glove, word2vec)

## Methods


## Results

<img width="400" alt="week_mean" src="reports/figures/1195191_week_plot_mean.png">
<img width="400" alt="month_mean" src="reports/figures/1195191_month_plot_mean.png">


## Reproducibility

**Step 1: Clone repository**  
- open a Linux terminal
- Navigate the destination of the repository
- run the following command  
```console
 git clone https://github.com/PeterThramkrongart/cds-language-portfolio.git
``` 

**step 2: Run bash script**  
- Navigate to the folder "assignment-6".  
```console
cd assignments/assignment-6
```  
- We have written a bash script _GOT_classification.sh_ to set up a virtual environment, run the python script, save the plots, and kill the environment afterwards:  
```console
bash GOT_classification.sh
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
    │   └── figures        <- Generated graphics and figures to be used in reporting
    |
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    └── src                <- Source code for use in this project.
    └── __init__.py    <- Makes src a Python module
--------
