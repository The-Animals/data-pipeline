import pandas as pd
import re
from os import remove
from subprocess import PIPE, run
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from storage_clients import MinioClient, MySqlClient

"""
Generates JST LDA for a given model using: 

https://github.com/linron84/JST

explained in this paper:

http://people.cs.pitt.edu/~huynv/research/aspect-sentiment/Joint%20sentiment%20topic%20model%20for%20sentiment%20analysis.pdf

In order to run the model, make sure that the jst executable is available in:
data-pipeline/etl/topic_analysis/jst/Debug/
"""
class JSTAnalyzer:

    def __init__(self, minio_client: MinioClient, mysql_client: MySqlClient, stopwords: set):
        self._minio_client = minio_client
        self._mysql_client = mysql_client
        self.stopwords = stopwords

    def analyze(self):
        self.load_data()
        self.generate_model()
        self.analyze_model()

    def load_training_data(self):
        remove('topic_analysis/jst/input/training.dat')
        open('topic_analysis/jst/input/training.dat', 'x')
        self._load_data('training-speeches', 'topic_analysis/jst/input/training.dat')

    def load_test_data(self): 
        remove('topic_analysis/jst/input/test.dat')
        open('topic_analysis/jst/input/test.dat', 'x')
        self._load_data('test-speeches', 'topic_analysis/jst/input/test.dat')    

    def _load_data(self, bucket, output_file):
        """
        grab data from the minio instance and load into the jst analyzer.    
        """
        mla_table = self._mysql_client.read_data("SELECT * FROM training.mlas")

        for index, mla in mla_table.iterrows():
            print(f'loading data for {mla.FirstName} {mla.LastName}')
            # get sessions contained in files
            files = self._minio_client.list_objects(
                bucket, prefix=f'{mla.FirstName}_{mla.LastName}', recursive=True)

            text = ''
            for file in files:
                file_text = self._minio_client.get_object(
                    bucket, file.object_name).read().decode('utf-8')

                text += self._preprocess(file_text)

            with open(output_file, 'a') as f:
                f.write(f'{mla.FirstName}_{mla.LastName} {text}\n')

    def train_model(self):
        run(['topic_analysis/jst/Debug/jst', '-est', '-config', 'topic_analysis/jst/training.properties'])

    def test_model(self):
        run(['topic_analysis/jst/Debug/jst', '-inf', '-config', 'topic_analysis/jst/test.properties'])  

    def _preprocess(self, text):
        """
        Remove punctuation, create lowercase of all words, stem and 
        lemmatize the original text.
        """
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
        text = [lem.lemmatize(word) for word in text if not lem.lemmatize(word) in self.stopwords]
        text = " ".join(text)
        text += " "
        return text
