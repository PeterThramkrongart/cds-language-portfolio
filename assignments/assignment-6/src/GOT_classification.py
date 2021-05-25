#!/usr/bin/env python

# system tools
import os
import sys
sys.path.append(os.path.join(".."))

# pandas, numpy
import pandas as pd
import numpy as np

# import my classifier utility functions
import utils.classifier_utils as clf
from sklearn.preprocessing import LabelBinarizer, LabelEncoder

# Machine learning stuff from sklearn
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn import metrics


# tools from tensorflow
import tensorflow as tf
from tensorflow.random import set_seed
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Dense, 
                                     Dropout,
                                     BatchNormalization,
                                    )
from tensorflow.keras.optimizers import SGD
from tensorflow.keras import backend as K
from tensorflow.keras.utils import plot_model
from tensorflow.keras.regularizers import L2

# matplotlib
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

random_state = 42

#set seed for reproducibility
set_seed(random_state)
np.random.seed(random_state)

def plot_history(H, epochs):
    """
    Utility function for plotting model history using matplotlib
    
    H: model history 
    epochs: number of epochs for which the model was trained
    """
    plt.style.use("fivethirtyeight")
    plt.figure()
    plt.plot(np.arange(0, epochs), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epochs), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, epochs), H.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, epochs), H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.draw()
    plt.savefig(os.path.join("..","models", "nn_training_history.png"))


def main():

  """
  A function for running text classification of GoT texts from the terminal
  """
  # loading data
  data = pd.read_csv(os.path.join("..", "data", "raw","Game_of_Thrones_Script.csv"))

  # gathering all lines from a given character by a seson an episode to context and model's accuracy
  data = data.groupby(["Season", "Episode", "Name"])
  data = data["Sentence"].agg(lambda x: " ".join(x)).to_frame()
  data = data.reset_index().rename(columns ={"Sentence": "Text"}) #resetting index

  # train and test split using sklearn
  X_train, X_test, y_train, y_test = train_test_split(data.Text,
                                                      data["Season"], 
                                                      test_size=0.1, 
                                                      random_state=random_state)
  print("Data loaded and split")

  ### a baseline model of a logistic regresssion ###
  print("fitting baseline LogReg model")
  pipe = Pipeline(steps=[
       ('tfidf', TfidfVectorizer()),
       ('clf', LogisticRegression(solver = "liblinear",random_state = random_state))
   ])

  # report model metrict
  classifier = pipe.fit(X_train, y_train)
  y_pred = classifier.predict(X_test)
  classifier_metrics_lr = metrics.classification_report(y_test, y_pred)
  print(classifier_metrics_lr)

  # save the classification report
  filepath = os.path.join("..","models","LG_metrics.txt")
  text_file = open(filepath, "w")
  text_file.write(classifier_metrics_lr)
  text_file.close()

  ### Building network ###

  # integers to one-hot vectors
  lb = LabelBinarizer()
  y_train_bin = lb.fit_transform(y_train)
  y_test_bin = lb.fit_transform(y_test)

  # the nn will have a vocabulary size of 15000
  maxlen = 15000

  vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features = maxlen)
  X_train_feats = vectorizer.fit_transform(X_train).toarray()
  X_test_feats = vectorizer.transform(X_test).toarray()

  # l2 regularization
  l2 = L2(0.00001)

  # a new neural network
  model = Sequential()
  model.add(Dense(64, activation='relu', kernel_regularizer=l2,input_shape=(maxlen,)))
  model.add(BatchNormalization())
  model.add(Dropout(0.3))

  model.add(Dense(8, activation='softmax'))

  # compiler
  model.compile(loss='categorical_crossentropy',
                optimizer= SGD(learning_rate=  .01),
                metrics=['accuracy'])

  epochs = 10

  print(model.summary())
  achitecture_path = os.path.join("..","models","nn_model_architecture.png")
  #plot model
  plot_model(model, to_file = achitecture_path, show_shapes=True, show_layer_names=True)
  print(f"Image of model architecture saved in {achitecture_path}")

  print("fitting nn-model")

  # a fit history of the network
  history = model.fit(X_train_feats, y_train_bin,
                      epochs=epochs,
                      verbose=True,
                      validation_data=(X_test_feats, y_test_bin))


  # plot history
  plot_history(history, epochs = epochs)

  predictions=model.predict(X_test_feats, verbose=True)

  # get the class with highest probability for each sample
  y_pred = np.argmax(predictions, axis=1)
    
  le = LabelEncoder()
  y_test_int = le.fit_transform(y_test) #encode labels for the classification report
    
  # get the classification report
  metrics_nn =  metrics.classification_report(y_test_int, y_pred, target_names = y_test.sort_values().unique())
  print(metrics_nn)
  # save metrics

  filepath = os.path.join("..","models","NN_metrics.txt")
  text_file = open(filepath, "w")
  text_file.write(metrics_nn)
  text_file.close()

  print("We will now use grid search and crossvalidation to find a better model using an SGD-classifier")
  
  # Grid Search for SGD Classifier (stochastic gradient classifier)
  ## making a pipeline where we use two embedding methods to find out the best one
  pipe = Pipeline(steps=[
       ('tfidf', TfidfVectorizer()),
       ('clf', SGDClassifier(random_state = random_state))
   ])


  ## specifying 
  parameters = {
      'tfidf__ngram_range': [(1, 1), (1, 2),(1,3)],
      'tfidf__max_df': [1.0, 0.95,0.9,0.85],
      'tfidf__min_df': [0.0, 0.05],
      'clf__alpha': [1e-3, 1e-2, 1e-1], # learning rate
      'clf__penalty': ['l2'],
       
  }

  search = GridSearchCV(pipe, parameters, n_jobs = -1, verbose = 1, refit = True)
  gs_clf = search.fit(X_train, y_train)

  print(f"The best{gs_clf.best_score_}")
  print(f"The best model hyper parameters: {gs_clf.best_params_}")
  y_pred = gs_clf.predict(X_test)

  classifier_metrics_sgd = metrics.classification_report(y_test, y_pred)

  print(classifier_metrics_sgd)

  # get the classification report
  filepath = os.path.join("..","models", "SGD_metrics.txt")
  text_file = open(filepath, "w")
  text_file.write(classifier_metrics_sgd)
  text_file.close()

if __name__=="__main__":
  main()
