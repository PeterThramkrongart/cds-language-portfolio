#!/usr/bin/python

# import modules
import os #For creating paths
import pandas as pd #for dataframes
import matplotlib.pyplot as plt  #for plots
import matplotlib
matplotlib.use("Agg")
import spacy # for nlp pipeline
from spacytextblob.spacytextblob import SpacyTextBlob  #For sentiment analysis
import argparse
from tqdm import tqdm

# initialise spacy
nlp = spacy.load("en_core_web_sm")  #load spacy language model
nlp.add_pipe("spacytextblob") ## add to nlp pipeline


def sentiment_plot(data,y_lim, title, filename, samples):
	"""
This function plots and saves sentiment plots

input:
	data: pd.DataFrame with sentement scores over time
	y_lim: tuple of limits for the y axis
	title: string with the title
	samples: number of samples used
	"""
	# specify plot asthetics
	plot = data.plot(
    ylabel = "Sentiment Score",
    xlabel = "Published Date",
    ylim = y_lim, #set axis limits
    title = title)

	# save plot
	fig = plot.get_figure()
	fig.savefig(os.path.join("..", "reports", "figures",f"{samples}_{filename}"))



def main(samples = 1195191, cores = -1):
	"""
	This function loads data as a pandas dataframe, calculates mean and variance of the sentiment scores per week and month. Lastly, it saves the figures.

	Inputs:
		samples,  default: 50000:  description: int, a number of titles to be sampled (max 1 milion)
		cores,    default: -1   :  descritption int, the number of cpu cores use for the text processing. Uses all available cores as a default.

	Output:
		plots of mean and variance per week and month saved in reports/figures/
	"""
  
	# load data as a pandas dataframe
	data_path = os.path.join("..", "data", "raw", "abcnews-date-text.csv") #path to data
	data = pd.read_csv(data_path) # read data
	
	print("Succesfully loaded data")
	# set a column to a date type and sample data frame 
	data['publish_date'] = pd.to_datetime(data.publish_date, format="%Y%m%d") #convert variable to datetime format
	data = data.sample(samples) # sample x random headlines

	# sort data
	data = data.sort_values("publish_date")

	# empty list for sentiment scores
	senti_list = []
	
	print(f"Processing texts using {cores} cores")
	
	# a loop to extract sentiment score for every headline
	for doc in tqdm(nlp.pipe(data.headline_text, disable = ["ner"], n_process = cores)): #for each headline...
	    #doc = nlp(headline)  #process headline
	    score = doc._.polarity #extract sentiment score
	    senti_list.append(score) #append to list
	
	# appending list with the sentiment score into pandas dataframe
	data["sentiment"] = senti_list


	# calculating and plotting mean score per week
	data_week_mean = data.resample("W",on ="publish_date").mean()
	sentiment_plot(data_week_mean, y_lim = (-0.175,0.175), title = "Mean of Weekly Sentiment Scores", filename = "week_plot_mean",samples = samples)
	
	# calculating and plotting mean score per month
	data_month_mean = data.resample("M",on ="publish_date").mean()
	sentiment_plot(data_month_mean, y_lim = (-0.175,0.175), title = "Mean of Monthly Sentiment Scores", filename = "month_plot_mean",samples = samples)



	# calculating and plotting variance per week
	data_week_var = data.resample("W",on ="publish_date").var()
	sentiment_plot(data_week_var, y_lim = (0,0.125), title = "Variance of Weekly Sentiment Scores", filename ="week_plot_variance",samples = samples)

	# calculating and plotting variance per month
	data_month_var = data.resample("M",on ="publish_date").var()
	sentiment_plot(data_month_var, y_lim = (0,0.125), title = "Variance of Monthly Sentiment Scores", filename = "month_plot_variance",samples= samples)
	
	print(f"Done :-) \n Plots are available at {os.path.join('..', 'reports', 'figures')}")

if __name__ =="__main__":

	# We argparse to add possible inputs from terminal
    ap = argparse.ArgumentParser(description = "[INFO] This function loads data as a pandas dataframe, calculates mean and variance of the sentiment scores per week and month. Lastly, it saves the figures.")
    
    ap.add_argument("-s", "--samples", default = 1195191,
                    type = int, help = "int, The number of samples to use in the analysis")

    ap.add_argument("-c", "--cores", default = -1,
                    type = int, help = "int,the number of cpu cores use for the text processing. Uses all available cores as a default.")
    
    args = vars(ap.parse_args())


    main(args["samples" ], args["cores"])

