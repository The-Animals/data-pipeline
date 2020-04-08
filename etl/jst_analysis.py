# REQ 4.3.3.5 (REQ11) Most similar and/or most dissimilar MLA based on sentiment/content analysis of summarizing quotes

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
    jst_analyzer.train_model()

def test_jst_model(mysql_client):
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)
    # jst_analyzer.estimate('test') 
    jst_analyzer.analyze('test')
    total, sim, dif = jst_analyzer.measure_of_success('test')
    print(f'the total accuracy of the model is: {total}')
    print(f'the similarity accuracy of the model is: {sim}')
    print(f'the accuracy of the model is: {dif}')


def analyze_jst_model(mysql_client):
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)
    # jst_analyzer.estimate('analyze')
    jst_analyzer.analyze('analyze')
    total, sim, dif = jst_analyzer.measure_of_success('db')
    print(f'the total accuracy of the model is: {total}')
    print(f'the similarity accuracy of the model is: {sim}')
    print(f'the accuracy of the model is: {dif}')

def mos_test(mysql_client):
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)
    total, sim, dif = jst_analyzer.measure_of_success('test')
    print(f'the total accuracy of the model is: {total}')
    print(f'the similarity accuracy of the model is: {sim}')
    print(f'the accuracy of the model is: {dif}')

def mos(mysql_client):
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)
    total, sim, dif = jst_analyzer.measure_of_success('db')
    print(f'the total accuracy of the model is: {total}')
    print(f'the similarity accuracy of the model is: {sim}')
    print(f'the accuracy of the model is: {dif}')


if __name__ == '__main__':
    if len(argv) < 2:
        print('please specify: one of "train", "test" or "analyze"')
        exit(1)
    if argv[1] == 'train':
        with MySqlClient('train') as mysql_client:
            train_jst_model(mysql_client)
    elif argv[1] == 'test':
        with MySqlClient('test') as mysql_client:
            test_jst_model(mysql_client)
    elif argv[1] == 'analyze':
        with MySqlClient() as mysql_client:
            analyze_jst_model(mysql_client)
    elif argv[1] == 'mos_test':
        with MySqlClient() as mysql_client:
            mos_test(mysql_client)
    elif argv[1] == 'mos':
        with MySqlClient() as mysql_client:
            mos(mysql_client)
    else:
        print(f'unknown argument: {argv[1]}')
