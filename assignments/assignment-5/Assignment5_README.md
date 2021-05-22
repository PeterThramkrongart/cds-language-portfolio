## Assignment 5 -Unsupervised machine learning

#### Authors: 
Peter Thramkrongart & Jakub Raszka

### Task:

Train an LDA model on your data to extract structured information that can provide insight into your data. For example, maybe you are interested in seeing how different authors cluster together or how concepts change over time in this dataset.

You should formulate a short research statement explaining why you have chosen this dataset and what you hope to investigate. This only needs to be a paragraph or two long and should be included as a README file along with the code. E.g.: I chose this dataset because I am interested in... I wanted to see if it was possible to predict X for this corpus.

In this case, your peer reviewer will not just be looking to the quality of your code. Instead, they'll also consider the whole project including choice of data, methods, and output. Think about how you want your output to look. Should there be visualizations? CSVs?


You should also include a couple of paragraphs in the README on the results, so that a reader can make sense of it all. E.g.: I wanted to study if it was possible to predict X. The most successful model I trained had a weighted accuracy of 0.6, implying that it is not possible to predict X from the text content alone. And so on.

Tips

Think carefully about the kind of preprocessing steps your text data may require - and document these decisions!
Your choice of data will (or should) dictate the task you choose - that is to say, some data are clearly more suited to supervised than unsupervised learning and vice versa. Make sure you use an appropriate method for the data and for the question you want to answer
Your peer reviewer needs to see how you came to your results - they don't strictly speaking need lots of fancy command line arguments set up using argparse(). You should still try to have well-structured code, of course, but you can focus less on having a fully-featured command line tool

General instructions

You should upload standalone .py script(s) which can be executed from the command line
You must include a requirements.txt file and a bash script to set up a virtual environment for the project You can use those on worker02 as a template
You can either upload the scripts here or push to GitHub and include a link - or both!
Your code should be clearly documented in a way that allows others to easily follow the structure of your script and to use them from the command line

Purpose

This assignment is designed to test that you have an understanding of:

how to formulate research projects with computational elements;
how to perform unsupervised machine learning on text data;
how to present results in an accessible manner.

### Instructions to run the script:

To run the script follow these steps:   
1. Clone the repository: git clone https://github.com/JakubR12/cds-language.git  
2. Navigate to the newly created repository  
3. Create a virtual environment: bash create_lda_venv.sh  
4. Activate the virtual environment: source ldavenv/bin/activate  
5. go to the src folder: cd src  
6.  Run the script: python philosophy_lda.py 

The script will take a little less than 20 minutes to runb on worker2, but muuuuuch longer if you run it on a local machine with few cores. The output will be available in data/assignment5 as philosophy_LDAvis.html


### Research statement:
We don't know much about western philosophy, so we want to investigate what major philosophical topics have been discussed throughout time. We will use the History of Philosophy data set available at: https://www.kaggle.com/kouroshalizadeh/history-of-philosophy.The data set contains over 300,000 sentences from 51 texts spanning 11 schools of philosophy. The represented schools are: Plato, Aristotle, Rationalism, Empiricism, German Idealism, Communism, Capitalism, Phenomenology, Continental Philosophy, Stoicism and Analytic Philosophy. We don'´t know the schools very well, but in this project we assume that they together as a whole have discussed many of the same topics but with differing viewpoints overtime. For this project we used the probabilistic, unsupervised learning method latent Dirichlet allocation to attempt to allocate the words of the text into major topics of western philosophy.

### Preprocessing pipeline:
The pre-processing pipeline consists of 3 major steps.    
First, we loaded the data as sentences and collapsed them into large text strings of individual books.  
Second, we divided the texts into chunks of 2000 tokens for easier modeling. The chunk size of 2000 tokens was chosen as balance between strain on memory or CPU, sufficient context to words, and reasonable computing times.   
Third, we removed stopwords and then tokenized, lemmatized and pos-tagged the texts using modified version of Ross' function for pre-processing with spaCy. We chose to only consider nouns, adjectives, and verbs, and to disregard n-grams entirely. This was because this analysis was about the major concepts and topics in philosophy and not the major individuals or places. We therefore, don't expect n-grams to be of much use for us. Lastly, we chose to bind lemmas to their POS-tag to aid comprehension of the models and to attempt to individualize homonyms(words that are spelled the same way, but have multiple meanings like the word "show").

### Modeling
We modeled our data using Gensim's LDA-algorithm. We fit the model to 15 topics with 1000 iterations and 10 passes. We set a the gamma threshold to 0.005 to stop model earlier when it stopped improving more than the threshold. Each text chunk (that originally consisted of 2000 words each before pre-processing) of was treated as a separate document. Lastly, we computed a coherence score and perplexity to evaluate model's performance.

### Results
In total, the whole pipeline took a little less than 20 minutes to run on worker2. We decided on a model with 15 topics, because that seemed to be the maximum number of topics we could fit while still being sufficiently distinct and human interpretable. the Coherence Score was 0.55 and Perplexity was -7.36. 

We interpret the topic to be as follows:

1) Phenomenology and consciousness  
2) Scientific methods and logic  
3) Rhetorical elements of philosophical discussion  
4) The emotions and mental states of human life.  
5) Morality in society  
6) Finance , commodities and market powers  
7) Reality, perception, and imagination  
8) Destiny  
9) The industrialized world  
10) Cognition  
11) Medicine and biology  
12) The elements and the natural world
13) Justice and legislation  
14) Ideologies of economy and society  
15) Perception  

In our view, this model largely sums up the philosophical topics we have heard about. We would have expected the the topic of ethics to be a single distinct topic, but in our model that does not seem to be the case. Rather, It is tangled to topics 4,5,8, and 13.

### Futher work:
This project mainly ordered texts by titles. This was because we don't know that much about philosophy to begin with. To further the project, we could attempt to find out what schools and authors are related to each topic. 

