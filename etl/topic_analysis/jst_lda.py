import re
import numpy as np
import pandas as pd
from os import remove
from subprocess import PIPE, run
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from storage_clients import MinioClient, MySqlClient, DbSchema

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

    def load_data(self, bucket, output_file, db):
        """
        grab data from the minio instance and load into the jst analyzer.
        """
        mla_table = self._mysql_client.read_data(f"SELECT * FROM {db}.mlas")

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

            if len(text) > 0:
                with open(output_file, 'a') as f:
                    f.write(f'{mla.Id} {text}\n')

    def train_model(self):
        run(['topic_analysis/jst/Debug/jst', '-est', '-config',
             'topic_analysis/jst/training.properties'])

    def estimate(self, stage):
        run(['topic_analysis/jst/Debug/jst', '-inf',
             '-config', f'topic_analysis/jst/{stage}.properties'])

    def analyze(self, stage):
        mla_ids, vectors = self.load_estimate(
            f'topic_analysis/jst/{stage}/final_final.newtheta',
            f'topic_analysis/jst/{stage}/final_final.newpi'
        )
        table = DbSchema.comparison
        df = self.compute_distances(mla_ids, vectors)
        self._mysql_client.overwrite_table(table, df)

    def measure_of_success(self, db): 
        sim = self._mysql_client.read_data(f"""
            select count(*) as sim
            from {db}.mlas as p, {db}.mlas as sim, {db}.mlacomparison as s
            where s.MLAId = p.Id
            and s.MostSimilar = sim.Id
            and p.Caucus = sim.Caucus;
        """).sim
        dif = self._mysql_client.read_data(f"""
            select count(*) as dif
            from {db}.mlas as p, {db}.mlas as dis, {db}.mlacomparison as s
            where s.MLAId = p.Id
            and s.LeastSimilar = dis.Id
            and p.Caucus != dis.Caucus;
        """).dif
        total = self._mysql_client.read_data(f"""
            select count(*) as total
            from {db}.mlacomparison
        """).total
        return (sim + dif)/(total*2), sim/total, dif/total

    def load_estimate(self, theta_file, pi_file):
        pi_regex = r'd_\d+ \d+ [\d. ]+'
        theta_regex = r'Document [\d\n. ]+'
        theta = open(theta_file, 'r').read()
        pi = open(pi_file, 'r').read()
        theta_matches = re.findall(theta_regex, theta)
        pi_matches = re.findall(pi_regex, pi)

        mla_ids = []
        vectors = []

        for d_m, p_m in zip(theta_matches, pi_matches):
            _, mla_id, senti1, senti2 = p_m.split()
            mla_id = int(mla_id)
            senti1 = float(senti1)
            senti2 = float(senti2)
            _, topic_senti1, topic_senti2, _ = d_m.split('\n')
            topic_senti1 = [float(x) for x in topic_senti1.split()]
            topic_senti2 = [float(x) for x in topic_senti2.split()]
            topic_vec = np.subtract(topic_senti1, topic_senti2)
            topic_vec = topic_vec / np.linalg.norm(topic_vec)
            mla_ids.append(mla_id)
            vectors.append(topic_vec)

        return mla_ids, np.array(vectors)

    def compute_distances(self, mla_ids, vectors):
        distances = []
        for i in range(len(mla_ids)):
            min_dist = float('inf')
            max_dist = 0
            for j in range(len(mla_ids)):
                dist = np.linalg.norm(vectors[i] - vectors[j], 2)
                if dist < min_dist and i != j:
                    min_dist = dist
                    min_index = j
                if dist > max_dist:
                    max_dist = dist
                    max_index = j

            distances.append({
                'MLAId': mla_ids[i],
                'MostSimilar': mla_ids[min_index],
                'LeastSimilar': mla_ids[max_index],
            })

        return pd.DataFrame(distances)

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
        text = [lem.lemmatize(word) for word in text if not lem.lemmatize(
            word) in self.stopwords]
        text = " ".join(text)
        text += " "
        return text
