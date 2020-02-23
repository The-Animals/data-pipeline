import os
from nltk.stem.snowball import EnglishStemmer

# Variables
# ---------------------------------------------------------------------------------------------
stopwordsFile = 'nltk.txt'
stemmer = EnglishStemmer()
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
