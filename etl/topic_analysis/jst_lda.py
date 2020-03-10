import pandas as pd
import re
from subprocess import run
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

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
        self._load_data('training-speeches', './jst/input/training.dat')

    def load_test_data(self): 
        self._load_data('test-speeches', './jst/input/test.dat')    

    def _load_data(self, bucket, output_file):
        """
        grab data from the minio instance and load into the jst analyzer.    
        """
        mla_table = self._mysql_client.read_data("SELECT * FROM training.mlas")

        for index, mla in mla_table.iterrows():
            print(f'loading data for {mla.FirstName} {mla.LastName}')
            # get sessions contained in files
            files = minio_client.list_objects(
                bucket, prefix=f'{mla.FirstName}_{mla.LastName}', recursive=True)

            text = ''
            for file in files:
                file_text = self._minio_client.get_object(
                    bucket, file.object_name).read().decode('utf-8')

                text += _preprocess(file_text)

        with open(output_file, 'a') as f:
            f.write(f'{mla.FirstName}_{mla.LastName} {text}\n')

    def train_model(self):
        run(['./jst/Debug/jst', '-est', '-config', 'training.properties'], capture_output=True )

    def test_model(self):
        run(['./jst/Debug/jst', '-inf', '-config', 'test.properties'], capture_output=True)   

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
        text = [lem.lemmatize(word) for word in text if not lem.lemmatize(word) in stopwords]
        text = " ".join(text)
        text += " "
        return text
