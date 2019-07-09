# Question-Reduce
The idea of these scripts is to identify questions that are similar to one another in the list of questions and pick the best question as a representative of them.  This question would then be saved and exported as part of a CSV file containing all the unique questions.  Obviously, manual work would be required to format the resulting questions, but it would serve as a start by reducing 14k questions that have to be worked through down to a more manageable amount (e.g. 1400).

## Excel-Reduce
Initial design, use SpaCy to process the text using NLP and then apply sypatic analysis to the text to vectorize based on the words used and it's surrounding context.  Failed to work due to requiring 64-bit OS whilst only having 32-bit OS available.

## New_tool
Idea was to break questions down into multiple columns and then comparing the levenshtein distance between the first column, column_0, which contains the start of the question.  Questions too similar in column_0 are deleted as they are highly likely to be the same questions, but with some differing parts later on that were deemed pointless e.g. "Have you taken: Cocaine" vs "Have you taken: Opiods".  

After this, the levenshtein distance would be calculated over the full question and this would be used to determine if the whole question is too similar or not.  Similar questions would be dropped.

## Question-Reduce
Simplify the problem.  Vectorize the questions using TfidfVectorizer and then run a MiniBatchKMeans model on the results to cluster the similar questions together.  From here, we can simply pick the longest question because it will have all the parts that we are interested in as well as parts that we deem are pointless, but can be manually worked through.  
