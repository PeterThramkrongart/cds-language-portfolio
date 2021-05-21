Assignment 4 - Network Analysis
==============================
**Peter Thramkrongart and Jakub Raszka**

##	Github link

Link to the repository: https://github.com/PeterThramkrongart/cds-language-portfolio.git

Link to the assignment folder: https://github.com/PeterThramkrongart/cds-language-portfolio/tree/main/assignments/assignment-4

## Contribution

Both Peter Thramkrongart and Jakub Raszka contributed equally to every stage of this project from initial conception and implementation, through the production of the final output and structuring of the repository. (50/50%)

##  Description

The purpose of this assignment is to create a reusable network analysis pipeline.This command-line tool will take a given dataset and perform simple network analysis. In particular, it is supposed to build networks based on entities appearing together in the same documents and create its visual representation. The script should:

-  be able to be run from the command line

- take any weighted edgelist as an input, providing that edgelist is saved as a CSV with the column headers "nodeA", "nodeB"
- create a network visualization, which will be saved, for any given weighted edgelist given as an input.
- create a data frame showing the degree, betweenness, and eigenvector centrality for each node.

## Methods



## Results

<img src="./reports/figures/network_visualization.png" alt="Cropped Image" width="500"/>


## Reproducibility

**Step 1: Clone repository**  
- open a Linux terminal
- Navigate the destination of the repository
- run the following command  
```console
 git clone https://github.com/PeterThramkrongart/cds-language-portfolio.git
``` 

**step 2: Run bash script:**  
- Navigate to the folder "assignment-3".  
```console
cd assignments/assignment-3
```  
- We have written a bash script _network_analysis.sh_ to set up a virtual environment, run the python script, save the plot, and kill the environment afterwards:  
```console
bash network_analysis.sh
```  
By default, the bash script runs the analysis on all the data and uses all available cores. This may not by an option for you. Therefore, you have to run the analysis manually:

**Step 1: Clone repository**  
- open a Linux terminal
- Navigate the destination of the repository
- run the following command  
```console
 git clone https://github.com/PeterThramkrongart/cds-language-portfolio.git
``` 

**step 2: Set up the environment and activate it:**  
- Navigate to the folder "assignment-3".  
```console
cd assignments/assignment-3
```  
- We have written a bash script _create_network_analysis_venv.sh_ to set up a virtual environment:  
```console
bash create_network_analysis_venv.sh

source network_analysis_venv/bin/activate
```  

**step 3: run the python script:**  
- Navigate to the folder "src".  
```console
cd src
```  
- run the python script _network_analysis.py_ and specify the number of cores to use in integers and the number of samples to use:  
```console
python network_analysis.py -c {number of cores} -s {number of samples}
```  

**step 4 (optional): kill the environment:**  
- Navigate to the folder "assignment-3".  
```console
cd ..
```  
- run the bash script _kill_network_analysis_venv.sh_ to remove the virtual environment:  
```console
bash kill_network_analysis_venv.sh
```  

## Running the project on something else than Linux

Our projects are mainly made for Linux/mac users. Our python scripts should run on any machine, though our bash scripts may not work. For this case, we recommend using the python distribution system from https://www.anaconda.com/ to setup environments using our requirements.txt files.

Project Organization
------------
The folder structure of our projects is based on a simplified version of the cookiecutter datascience folder structure https://drivendata.github.io/cookiecutter-data-science/. For the sake of generalizability, some folders will remain empty in some projects but overall this will make folder navigation easier.


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

