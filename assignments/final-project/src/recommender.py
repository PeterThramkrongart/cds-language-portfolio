import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler, minmax_scale
from sklearn.metrics.pairwise import cosine_similarity
import argparse
from scipy import sparse

def recommend(title,df, genre_vec, tfidf_vec, authors_vec, tfidf_weight = 1, authors_weight = 0.2, genre_weight = 0.8, review_count_weight = 0.2, rating_weight = 0.3):

    indices = pd.Series(df.book_title)
    index = indices[indices == title].index[0]

    df["tfidf_sim"] = cosine_similarity(tfidf_vec , tfidf_vec[index])
    df["genres_sim"] = cosine_similarity(genre_vec , genre_vec[index])
    df["authors_sim"] = cosine_similarity(authors_vec , authors_vec[index])

    scaler = StandardScaler()
    df[['tfidf_sim', 'genres_sim',"authors_sim"]] = scaler.fit_transform(df[['tfidf_sim', 'genres_sim',"authors_sim"]])
    
    df["rec_score"] = df.tfidf_sim*tfidf_weight+df.genres_sim*genre_weight+df.book_review_count*review_count_weight+df.book_rating*rating_weight+df.authors_sim*authors_weight
   
    df = df[df.book_title != title]

    df["rec_score"] = minmax_scale(df.rec_score)

    df = df[["book_title","book_authors","genres","book_rating_count","book_rating","rec_score"]]
    return df.sort_values("rec_score", ascending = False)

def main(title = "1984", tfidf_weight = 1, authors_weight = 0.2, genre_weight = 0.8, review_count_weight = 0.2, rating_weight = 0.3):
	data = pd.read_csv(os.path.join("..","data","processed","rec_catalog.csv"))
	genre_vec = np.load(os.path.join("..","data","processed","genre_vec.npy"),allow_pickle  = True)
	authors_vec = np.load(os.path.join("..","data","processed","authors_vec.npy"),allow_pickle  = True)
	tfidf_vec = np.load(os.path.join("..","data","processed","tfidf_vec.npy"),allow_pickle  = True)


	genre_vec = sparse.csr_matrix(genre_vec.all())
	authors_vec = sparse.csr_matrix(authors_vec.all())
	tfidf_vec = sparse.csr_matrix(tfidf_vec.all())

	recs = recommend(title, data, genre_vec,tfidf_vec,authors_vec, tfidf_weight, authors_weight, genre_weight, review_count_weight, rating_weight)

	print(recs.head(20)[["book_title","book_authors","genres","rec_score"]])

	recs.to_csv(os.path.join("..","reports",f"{title}_recs.csv"))
	return recs


if __name__ =="__main__":
    
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
      args["title"], args["tfidf_weight"],args["authors_weight"],args["genre_weight"],args["review_count_weight"],args["rating_weight"])
