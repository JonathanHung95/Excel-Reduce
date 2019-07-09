# -*- coding: utf-8 -*-
"""
Python script to remove questions that are very similar to one another.  Should refactor at some point
for a more efficient script.
"""

# import libraries as needed
import pandas as pd
import numpy as np
import string

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from similarity.levenshtein import Levenshtein

# import the data and assign to the variable "questions"
questions = pd.read_csv("U:\Book2.csv", encoding='iso-8859-1')

"""
# cluster the data so that we can see how different questions are related to each other
# n_clusters can be changed, set to 100 here becasue I'm not sure how many questions there actually are
km = KMeans(n_clusters = 100, random_state = 322)
vectorizer = TfidfVectorizer(stop_words = "english")

X = vectorizer.fit_transform(questions["Question"])
km.fit(X)
predictions = km.predict(vectorizer.fit_transform(questions["Question"]))
questions["cluster"] = pd.Series(predictions, index = questions.index)

questions = questions.sort("cluster").reset_index()
"""
# split the questions based on the "\\n" in them into seperate columns
def seperate_text(text):
	seperated_text = text.split("\\n")
	return seperated_text

questions["listed_text"] = questions["Question"].apply(seperate_text)

split_questions = pd.DataFrame(questions.listed_text.values.tolist(), questions.index).add_prefix("column_")
questions = pd.merge(questions, split_questions, left_index = True, right_index = True).reset_index()

# compare the similarity of just column_0 to filter out questions that are too similar to
# one another where the question is essentially the same, but with a different object
# e.g. "Have you taken: cocaine" or "Have you taken: opiods"
levenshtein = Levenshtein()

index = 1
threshold = 0.9
reference_string = questions["column_0"].iloc[0]

while index < len(questions) - 1:
    string_1 = reference_string
    string_2 = questions["column_0"].iloc[index]
    levenshtein_distance = levenshtein.distance(string_1, string_2)
    if len(string_1) > len(string_2):
        similarity = 1 - levenshtein_distance / len(string_1)
    else:
        similarity = 1 - levenshtein_distance / len(string_2)
    if similarity > threshold:
        questions = questions.drop(questions.index[[index]])
        index += 1
    else:
        reference_string = questions["column_0"].iloc[index]
        index += 1

# clean up the questions by setting all to lower case and stripping punctuation
questions["Question"] = questions["Question"].str.lower()

# compare the similarity of each whole question and drop the questions that are very similar to one another
index = 1
threshold = 0.7
reference_string = questions["Question"].iloc[0]

while index < len(questions) - 1:
    string_1 = reference_string
    string_2 = questions["Question"].iloc[index]
    levenshtein_distance = levenshtein.distance(string_1, string_2)
    if len(string_1) > len(string_2):
        similarity = 1 - levenshtein_distance / len(string_1)
    else:
        similarity = 1 - levenshtein_distance / len(string_2)
    if similarity > threshold:
        questions = questions.drop(questions.index[[index]])
        index += 1
    else:
        reference_string = questions["Question"].iloc[index]
        index += 1

# export as a csv file "cleaned_questions.csv"
final_questions = pd.DataFrame(questions["Question"])
final_questions.to_csv("U:\cleaned_questions3.csv", encoding = "utf-8")
