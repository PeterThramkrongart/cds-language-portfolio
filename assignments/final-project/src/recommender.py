#!/usr/bin/python

# import modules
import pandas as pd
import numpy as np
import os
import argparse

# matrix tools
from scipy import sparse

# sklearn tool
from sklearn.preprocessing import StandardScaler, minmax_scale
from sklearn.metrics.pairwise import cosine_similarity


def recommend(title,df, genre_vec, tfidf_vec, authors_vec, tfidf_weight = 1, authors_weight = 0.2, genre_weight = 0.8, review_count_weight = 0.2, rating_weight = 0.3):
    """
    A function for calculating cosine similarity of tfidf book description, genres, and authors and applying customizable weights to the relevant parameters.
    """

    # setting a chosen book as number one and resetting the index
    indices = pd.Series(df.book_title)
    index = indices[indices == title].index[0]

    # calculating cosine similarities
    df["tfidf_sim"] = cosine_similarity(tfidf_vec , tfidf_vec[index])
    df["genres_sim"] = cosine_similarity(genre_vec , genre_vec[index])
    df["authors_sim"] = cosine_similarity(authors_vec , authors_vec[index])

    # standardazing cosine similarities
    scaler = StandardScaler()
    df[['tfidf_sim', 'genres_sim',"authors_sim"]] = scaler.fit_transform(df[['tfidf_sim', 'genres_sim',"authors_sim"]])
    
    # applying customizable weights to the relevant parameters
    df["rec_score"] = df.tfidf_sim*tfidf_weight+df.genres_sim*genre_weight+df.book_review_count*review_count_weight+df.book_rating*rating_weight+df.authors_sim*authors_weight
   
    # dropping the searched title from recommendations
    df = df[df.book_title != title]

    # scaling the final recommendation score to make some sense of it
    df["rec_score"] = minmax_scale(df.rec_score)

    # choosing only relevant columns and sorting them by the recommendation score
    df = df[["book_title","book_authors","genres","book_rating_count","book_rating","rec_score"]]
    return df.sort_values("rec_score", ascending = False)


def main(title = "1984", tfidf_weight = 1, authors_weight = 0.2, genre_weight = 0.8, review_count_weight = 0.2, rating_weight = 0.3):

    # loading cleaned goodreads dataset
    data = pd.read_csv(os.path.join("..","data","processed","rec_catalog.csv"))

    # loading vectors
    genre_vec = np.load(os.path.join("..","data","processed","genre_vec.npy"),allow_pickle  = True)
    authors_vec = np.load(os.path.join("..","data","processed","authors_vec.npy"),allow_pickle  = True)
    tfidf_vec = np.load(os.path.join("..","data","processed","tfidf_vec.npy"),allow_pickle  = True)

    # transorming matrices to fit the recommender
    genre_vec = sparse.csr_matrix(genre_vec.all())
    authors_vec = sparse.csr_matrix(authors_vec.all())
    tfidf_vec = sparse.csr_matrix(tfidf_vec.all())

    error_message = """\nThe title does not seem to be in the dataset. Have you spelled it correctly?\n
    Try to copy the title from goodreads. That's where we got our data.\n
    Note that our data is from 2017 and, that we only used books with more than 50 written reviews."""

    # recommend books and the errror message if the book isn't in the dataset
    try:
      recs = recommend(title, data, genre_vec,tfidf_vec,authors_vec, tfidf_weight, authors_weight, genre_weight, review_count_weight, rating_weight)
    except IndexError:
      raise IndexError(error_message)

    # print first 20 books in the command line
    print(recs.head(20)[["book_title","book_authors","genres","rec_score"]])

    # save 500 best recommendations
    recs.head(500).to_csv(os.path.join("..","reports", "recommendations",f"{title}_recs.csv"))

    return recs


if __name__ =="__main__":

    """
    This script creates a book recommender based on customizable weights.

    Inputs:
        flags: -t, --title, default = 1984, type = str, help = str, Title to base recommendations on

        flags: -tw, --tfidf_weight, default = 1, type = float, help = float, The weight of tfidf on recommendations

        flags: -aw, --authors_weight, default = 0.2, type = float, help = float, The weight of authors on recommendations

        flags: -gw, --genre_weight, default = 0.8, type = float, help = "loat, The weight of genre on recommendations
        
        flags: -rcw, --review_count_weight, default = 0.2, type = float, help = float, The weight of review counts on recommendations

        flags: -rw, --rating_weight, default = 0.3, ype = float, help = float, The weight of ratings on recommendations
    
    Output:
        .csv file with top 500 recommended books saved into reports/recommendations/
        a Pandas DataFrame with the whole dataset sorted by rec_score
        prints(the top 20 best recommendations)
    """
    
    # We argparse to add possible inputs from terminal
    ap = argparse.ArgumentParser(description = "[INFO] Recommends books based on the conted of the given book title")
    
    ap.add_argument("-t", "--title", default = "1984",
                    type = str, help = "str, Title to base recommendations on")

    ap.add_argument("-tw", "--tfidf_weight", default = "1",
                    type = float, help = "float, The weight of tfidf on recommendations")

    ap.add_argument("-aw", "--authors_weight", default = "0.2",
                    type = float, help = "float, The weight of authors on recommendations")

    ap.add_argument("-gw", "--genre_weight", default = "0.8",
                    type = float, help = "float, The weight of genre on recommendations")

    ap.add_argument("-rcw", "--review_count_weight", default = "0.2",
                    type = float, help = "float, The weight of review counts on recommendations")

    ap.add_argument("-rw", "--rating_weight", default = "0.3",
                    type = float, help = "float, The weight of ratings on recommendations")

    args = vars(ap.parse_args())

    main(
        args["title"], 
        args["tfidf_weight"],
        args["authors_weight"],
        args["genre_weight"],
        args["review_count_weight"],
        args["rating_weight"])
