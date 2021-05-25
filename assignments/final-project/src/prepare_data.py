import pandas as pd
import numpy as np
import spacy
from spacy_fastlang import LanguageDetector

nlp = spacy.load('en_core_web_sm',disable=["ner"])
nlp.add_pipe("language_detector",  config={"threshold": 0.50, "default_language": "en"})

import os
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel 
from sklearn.preprocessing import StandardScaler


from sklearn.metrics.pairwise import cosine_similarity

def split_authors_and_genres(string):
    vector =  string.split(", ")
    return vector

def main():
    data = pd.read_csv(os.path.join("..","data","raw","book_data.csv"), usecols = ['book_authors', 'book_desc',
           'book_pages', 'book_rating', 'book_rating_count', 'book_review_count',
           'book_title', 'genres',"book_format"])
    data = data.dropna()
    data = data[data["book_review_count"] >= 50]
    data["book_pages"] = data.book_pages.str.replace(" pages", "")
    data["book_pages"] = data.book_pages.str.replace(" page", "")
    data["book_desc"] = data.book_desc.str.replace("\r", "")
    data["book_desc"] = data.book_desc.str.replace("\n", "")
    scaler = StandardScaler()
    data[['book_pages', 'book_rating', 'book_rating_count', 'book_review_count']] = scaler.fit_transform(data[['book_pages', 'book_rating', 'book_rating_count', 'book_review_count']])
    book_format = ['Hardcover', 'Paperback']
    data = data[data.book_format.isin(book_format)]

    english = []
    texts = []
    for doc in tqdm(nlp.pipe(data.book_desc,n_process = -1)):
        english.append(doc._.language == 'en')
        texts.append(" ".join([token.lemma_ for token in doc]))


    data["text_processed"] = texts
    data = data[english]
    data = data.sort_values("book_review_count", ascending = False)
    data = data.drop_duplicates(subset = ["book_title"])
    data = data.reset_index(drop = True)
    data["genres"] = data.genres.str.replace("|", ", ")
    data["book_authors"] = data.book_authors.str.replace("|", ", ")

    data.to_csv(os.path.join("..","data","processed","rec_catalog.csv"),index = False)

    vectorizer = CountVectorizer(tokenizer = split_authors_and_genres)
    genre_vec = vectorizer.fit_transform((data["genres"]))

    np.save(os.path.join("..","data","processed","genre_vec.npy"), genre_vec)

    authors_vec = vectorizer.fit_transform(data.book_authors)
    
    np.save(os.path.join("..","data","processed","authors_vec.npy"), authors_vec)

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')

    tfidf_vec= tf.fit_transform((data["text_processed"]))

    np.save(os.path.join("..","data","processed","tfidf_vec.npy"), tfidf_vec)

if __name__=="__main__":
  main()
