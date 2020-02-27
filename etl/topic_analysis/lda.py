import pandas as pd
import re
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

"""
Generates lda model for a given corpus

https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py
"""
class TopicAnalyzer:

    N_FEATURES = 2000
    N_COMPONENTS = 15

    def __init__(self, corpus: list, stopwords: set):
        self.corpus = corpus
        self.stopwords = stopwords

    def analyze(self): 
        self.preprocess()
        self.fit()
        return self.get_topics()

    def preprocess(self):
        """
        Create a new column in the corpus data frame containing text that has been 
        preprocessed. Remove punctuation, create lowercase of all words, stem and 
        lemmatize the original text.
        """
        def _text_preprocess(text: str):
            # Remove punctuations
            text = re.sub('[^a-zA-Z]', ' ', text)
            # Convert to lowercase
            text = text.lower()
            # remove tags
            text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
            # remove special characters and digits
            text = re.sub("(\\d|\\W)+", " ", text)
            # Convert to list from string
            text = text.split()
            # Stemming
            stemmer = EnglishStemmer()
            # Lemmatisation
            lem = WordNetLemmatizer()
            text = [lem.lemmatize(word) for word in text if not word in self.stopwords]
            text = " ".join(text)
            return text

        self.preprocessed_data = [_text_preprocess(text) for text in self.corpus]

    def fit(self):
        tf_vectorizer = CountVectorizer(max_df=0.80, min_df=2,
                                        max_features=TopicAnalyzer.N_FEATURES,
                                        stop_words=self.stopwords)
        tf = tf_vectorizer.fit_transform(self.preprocessed_data)
        self.feature_names = tf_vectorizer.get_feature_names()
        self.lda = LatentDirichletAllocation(n_components=TopicAnalyzer.N_COMPONENTS, max_iter=5,
                                             learning_method='online',
                                             learning_offset=50.,
                                             random_state=0)
        self.lda.fit(tf)

    def get_topics(self, n_words_per_topic=20):
        topics = []
        for topic in self.lda.components_:
            topics.append(" ".join([self.feature_names[i]
                                    for i in topic.argsort()[:-n_words_per_topic - 1:-1]]))
        return topics