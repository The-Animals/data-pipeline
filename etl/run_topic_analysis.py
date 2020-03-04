from pkgutil import get_data
from pandas import DataFrame
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from topic_analysis import TopicAnalyzer
from storage_clients import MySqlClient, DbSchema

top_n_sentences = 2000
stopwords = {word.strip() for word in str(get_data('data', 'stopwords.txt').decode('utf-8')).split('\n')}

"""
Create dataframe of top topics per MLA
and upload to the database
"""


def generate_topics_per_mla():
    table = DbSchema.topics
    with MySqlClient() as mysql_client:
        topic_data = []
        mlas = mysql_client.read_data('SELECT * FROM mlas')

        for mla_id in mlas['Id']:
            print(f'creating topics for MLA with id : {mla_id}')
            try:
                data = mysql_client.read_data(
                    f'SELECT * FROM summaries_{mla_id} ORDER BY Rank LIMIT {top_n_sentences}')
            except:
                print(f'Could not execute query for id : {mla_id}')
                continue
            corpus = list(data['Sentence'])
            ta = TopicAnalyzer(corpus, stopwords)
            try:
                mla_topics = ta.analyze()
            except Exception as e:
                print(f'Could not run analysis for id : {mla_id}')
                print(e)

            for topic_rank, topic_words in enumerate(mla_topics):
                topic_data.append({
                    'MLAId': mla_id,
                    'TopicRank': topic_rank,
                    'Topic': topic_words
                })

        df = DataFrame(topic_data)
        mysql_client.overwrite_table(table, df)


if __name__ == '__main__':
    generate_topics_per_mla()
