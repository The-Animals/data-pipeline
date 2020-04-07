import os
from nltk.stem.snowball import EnglishStemmer
from pkgutil import get_data

# Variables
# ---------------------------------------------------------------------------------------------
stopwords = {word.strip() for word in str(get_data('data', 'stopwords.txt').decode('utf-8')).split('\n')}
stemmer = EnglishStemmer() # stemmer class
wordPattern = "^[^\W\d_]+$" # regex pattern to match a word
epsilon = 1e-4 # epsilon value for algorithm
damping = 0.85 # damping value for algorithm
delta = 1e-7 # delta value for algorithm
# ---------------------------------------------------------------------------------------------
