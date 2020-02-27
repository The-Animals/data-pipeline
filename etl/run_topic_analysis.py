from pkgutil import get_data
from pandas import DataFrame
from storage_clients import MySqlClient
from topic_analysis import TopicAnalyzer
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer


top_n_sentences = 2000
stopwords = {word.strip() for word in open('data/topic_stopwords.txt', 'r')}

"""
Create dataframe of top topics per MLA
and upload to the database
"""


def generate_topics_per_mla():
    topics = []
    mysql_client = MySqlClient()
    mlas = mysql_client.read_data('SELECT * FROM mlas')

    for last_name, mla_id in zip(mlas['MLALastName'], mlas['RidingNumber']):
        print(f'creating topics for {last_name}')
        try: 
            data = mysql_client.read_data(
            f'SELECT * FROM {last_name} ORDER BY Rank LIMIT {top_n_sentences}')
        except: 
            print(f'Could not execute query for {last_name}')
            continue
        corpus = list(data['Sentence'])
        ta = TopicAnalyzer(corpus, stopwords)
        try: 
            mla_topics = ta.analyze()
        except Exception as e:
            print(f'Could not run analysis for {last_name}')
            print(e)

        for topic_rank, topic_words in enumerate(mla_topics):
            topics.append({
                'MLAId': mla_id,
                'TopicRank': topic_rank,
                'TopicWords': topic_words
            })
    topics_table = DataFrame(topics)
    mysql_client.write_data('topics', topics_table)


if __name__ == '__main__':
    generate_topics_per_mla()