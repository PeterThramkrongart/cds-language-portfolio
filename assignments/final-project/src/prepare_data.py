#!/usr/bin/python

# import general modules
import pandas as pd
import numpy as np
import os
from tqdm import tqdm

# sklearn tools
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# spacy 
import spacy
from spacy_fastlang import LanguageDetector

## spacy pipeline for language detection
nlp = spacy.load('en_core_web_sm', disable=["ner"])
nlp.add_pipe("language_detector",  config={"threshold": 0.50, "default_language": "en"})


def split_authors_and_genres(string):
    """
    A function for splitting strings by comma and space
    """
    vector =  string.split(", ")
    return vector


def main():
    """
    This function preprocesses the data for the remmendation engine. 
    Specifically, it drops duplicated, non-english, and least reviewed books; lemmatizes book description; normalizes integer values to be comparable; vectorizing genres, authors;
    	making tfidf vectorization on the book description.
    
    Input:
    	data
    
    Output:
    	cleaned data
    	vectorized author and genre 
    	tfidf book description matrix
    
    """
	# load goodreads data
    data = pd.read_csv(os.path.join("..","data","raw","book_data.csv"), usecols = ['book_authors', 'book_desc',
           'book_pages', 'book_rating', 'book_rating_count', 'book_review_count',
           'book_title', 'genres',"book_format"])

    # drop NAs
    data = data.dropna()

    # keep only books with 50 and more reviews
    data = data[data["book_review_count"] >= 50]

    # keep only books in the hardcover or paperback edition
    book_format = ['Hardcover', 'Paperback']
    data = data[data.book_format.isin(book_format)]


    # make page numbers numeric
    data["book_pages"] = data.book_pages.str.replace(" pages", "")
    data["book_pages"] = data.book_pages.str.replace(" page", "")

    # regex expression to clean book decription from some html code
    data["book_desc"] = data.book_desc.str.replace("\r", "")
    data["book_desc"] = data.book_desc.str.replace("\n", "")

    # normalize some of the variables for later weighting in recommendation
    scaler = StandardScaler()

    data[['book_pages', 'book_rating', 'book_rating_count', 'book_review_count']] = scaler.fit_transform(data[['book_pages', 'book_rating', 'book_rating_count', 'book_review_count']])
    
    # empty list containers
    english = []
    texts = []

    # parallel detecting a language of book description  and lemmetazing it
    for doc in tqdm(nlp.pipe(data.book_desc,n_process = -1)):
        english.append(doc._.language == 'en')
        texts.append(" ".join([token.lemma_ for token in doc]))

    # appending lemmatized text to the data frame and filtering only english books
    data["text_processed"] = texts
    data = data[english]

    # dropping duplicates and resetting index
    data = data.sort_values("book_review_count", ascending = False)
    data = data.drop_duplicates(subset = ["book_title"])
    data = data.reset_index(drop = True)

    # replacing value seperator in genres and book_authors
    data["genres"] = data.genres.str.replace("|", ", ")
    data["book_authors"] = data.book_authors.str.replace("|", ", ")

    # saving the cleaned dataset
    data.to_csv(os.path.join("..","data","processed","rec_catalog.csv"),index = False)

    # initiliasing a count vectorizer with custom tokenizer to treat author names and two name genres as one
    vectorizer = CountVectorizer(tokenizer = split_authors_and_genres)

    # vectorizing and saving the matrix of genres
    genre_vec = vectorizer.fit_transform((data["genres"]))
    np.save(os.path.join("..","data","processed","genre_vec.npy"), genre_vec)

    # vectorizing and saving the matrix of authors
    authors_vec = vectorizer.fit_transform(data.book_authors)
    np.save(os.path.join("..","data","processed","authors_vec.npy"), authors_vec)

    # making tfidf matrix from book desription and saving it fot later use
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_vec= tf.fit_transform((data["text_processed"]))
    np.save(os.path.join("..","data","processed","tfidf_vec.npy"), tfidf_vec)

if __name__=="__main__":
    main()

