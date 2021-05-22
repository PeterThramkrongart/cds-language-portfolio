
import os # system tools
from csv import reader
import pandas as pd
from tqdm import tqdm #progression bar
import spacy
nlp = spacy.load("en_core_web_sm")

from itertools import combinations
from collections import Counter

def main():
	input_file = os.path.join("..", "data", "raw", "fake_or_real_news.csv")
	data = pd.read_csv(input_file)
	real_df = data[data["label"] == "REAL"]["text"]

	post_entities = []
	for doc in tqdm(nlp.pipe(real_df.values, n_process = -1)):
	    # Do something with the doc here
	    tmp_list = []
	    for ent in doc.ents:
	        if ent.label_ == "PERSON":
	            tmp_list.append(ent.text)
	    post_entities.append(tmp_list)

	edgelist = []

	# iterate over every document
	for doc in post_entities:
	    # use combinations to create edgelist
	    edges = list(combinations(doc, 2))
	    # for each combination - e.g., each pair of "nodes"
	    for edge in edges:
	        # append this to final edgelist
	        edgelist.append(tuple(sorted(edge)))

	counted_edges = []

	for pair, weight in Counter(edgelist).items():
	    nodeA = pair[0]
	    nodeB = pair[1]
	    counted_edges.append((nodeA, nodeB, weight))


	edge_df = pd.DataFrame(counted_edges, columns = ["nodeA", "nodeB", "weight"])
	edge_df.to_csv(os.path.join("..", "data", "interim", "edges_df.csv"))

  # defining behavior for when the script is run from the terminal
if __name__ =="__main__":
    
    main()
