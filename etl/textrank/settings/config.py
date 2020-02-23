import os
from nltk.stem.snowball import EnglishStemmer

# Variables
# ---------------------------------------------------------------------------------------------
stopwordsFile = 'nltk.txt' # file to grab stopwords from (in stopwords folder)
stemmer = EnglishStemmer() # stemmer class
wordPattern = "^[^\W\d_]+$" # regex pattern to match a word
epsilon = 1e-4 # epsilon value for algorithm
damping = 0.85 # damping value for algorithm
delta = 1e-7 # delta value for algorithm
# ---------------------------------------------------------------------------------------------




# Code
# ---------------------------------------------------------------------------------------------

# Create stopwords
with open('{0}\\stopwords\\{1}'.format(os.path.dirname(os.path.realpath(__file__)), stopwordsFile), 'r') as f:
    words = ()
    for word in f.readlines():
        words += (word.rstrip(),)
    stopwords = frozenset(words)

# ---------------------------------------------------------------------------------------------
