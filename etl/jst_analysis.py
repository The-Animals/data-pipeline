import re
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from pkgutil import get_data
from os import remove
from sys import argv
from storage_clients import MinioClient, MySqlClient, DbSchema
from topic_analysis import JSTAnalyzer

minio_client = MinioClient()

stopwords = {word.strip() for word in str(
    get_data('data', 'stopwords.txt').decode('utf-8')).split('\n')}


def train_jst_model(mysql_client):
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)

    remove('topic_analysis/jst/input/training.dat')
    open('topic_analysis/jst/input/training.dat', 'x')

    jst_analyzer.load_data('training-speeches',
                            'topic_analysis/jst/input/training.dat')
    jst_analyzer.train_model()


def test_jst_model(mysql_client):
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)

    remove('topic_analysis/jst/input/test.dat')
    open('topic_analysis/jst/input/test.dat', 'x')

    jst_analyzer.load_data('test-speeches',
                            'topic_analysis/jst/input/test.dat')

    jst_analyzer.estimate('test')
    jst_analyzer.analyze('test')
    total, sim, dif = jst_analyzer.measure_of_success('test')
    print(f'the total accuracy of the model is: {total}')
    print(f'the similarity accuracy of the model is: {sim}')
    print(f'the accuracy of the model is: {dif}')

def analyze_jst_model(mysql_client):
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)

    remove('topic_analysis/jst/input/analyze.dat')
    open('topic_analysis/jst/input/analyze.dat', 'x')

    jst_analyzer.load_data('speeches',
                            'topic_analysis/jst/input/analyze.dat', 'db')
    jst_analyzer.estimate('analyze')
    jst_analyzer.analyze('analyze')
    total, sim, dif = jst_analyzer.measure_of_success('db')
    print(f'the total accuracy of the model is: {total}')
    print(f'the similarity accuracy of the model is: {sim}')
    print(f'the accuracy of the model is: {dif}')


if __name__ == '__main__':
    if len(argv) < 2: 
        print('please specify: one of "train", "test" or "analyze"')
        exit(1)

    with MySqlClient() as mysql_client:
        if argv[1] == 'train':
            train_jst_model(mysql_client)
        elif argv[1] == 'test':
            test_jst_model(mysql_client)
        elif argv[1] == 'analyze': 
            analyze_jst_model(mysql_client)
        else: 
            print(f'unknown argument: {argv[1]}')
