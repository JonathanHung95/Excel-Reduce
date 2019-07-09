# -*- coding: utf-8 -*-
"""
Created on Tue Jul 09 11:53:14 2019

@author: n173437
"""

# import libraries as needed
import pandas as pd
import numpy as np
import string

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# import the data and assign to the variable "questions"
questions = pd.read_csv("U:\Book1.csv", encoding='iso-8859-1')

# define a set of functions to process the given data
def df_cluster(df = questions, target_column = "Question", cluster_number = 1500):
    """
    Initializes a MiniBatchKMeans model with cluster_number of clusters, 
    vectorizes the strings inside the target_column and clusters the strings based on vectors.
    Returns a dataframe with the strings and cluster number.
    """
    km = MiniBatchKMeans(n_clusters = cluster_number, random_state = 322, batch_size = 1000)
    vectorizer = TfidfVectorizer(stop_words = "english")
    X = vectorizer.fit_transform(df[target_column])
    km.fit(X)
    predictions = km.predict(X)
    df["cluster"] = pd.Series(predictions)
    return df  

def df_best_question(df = questions, target_column = "Question"):
    """
    Cleans up the df.
    Returns a dataframe with the longest strings of each cluster.
    """
    df = df.sort("cluster").reset_index()
    df["length"] = questions[target_column].str.len()
    final_df = df.groupby(["cluster"]).max().drop(["index", "length"], axis = 1)
    return final_df

# run the required functions
questions = df_cluster() 
final_questions = df_best_question()

# write to a csv file
final_questions.to_csv("U:\cleaned_questions.csv", encoding = "utf-8")