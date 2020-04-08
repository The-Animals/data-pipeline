from pkgutil import get_data
from sys import argv
from os.path import exists 
from os import remove
from pathlib import Path
from jst_analysis import JSTAnalyzer
from storage_clients import MySqlClient, MinioClient

minio_client = MinioClient()

stopwords = {word.strip() for word in str(
    get_data('data', 'stopwords.txt').decode('utf-8')).split('\n')}

def load_data(mysql_client, data_file, data_bucket):
    if exists(data_file): 
        remove(data_file)
    
    open(data_file, 'x')
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)
    jst_analyzer.load_data(data_bucket, data_file)

def load_training_data(mysql_client): 
    data_file = Path('topic_analysis/jst/input/training.dat')
    load_data(mysql_client, data_file, 'training-speeches')

def load_test_data(mysql_client): 
    data_file = Path('topic_analysis/jst/input/test.dat')
    load_data(mysql_client, data_file, 'test-data')

def load_analytical_data(mysql_client): 
    data_file = Path('topic_analysis/jst/input/analyze.dat')
    load_data(mysql_client, data_file, 'speeches')


if __name__ == '__main__':
    if len(argv) < 2:
        print('please specify: one of "train", "test" or "analyze"')
        exit(1)
    if argv[1] == 'train':
        with MySqlClient('train') as mysql_client:
            load_training_data(mysql_client)
    elif argv[1] == 'test':
        with MySqlClient('test') as mysql_client:
            load_test_data(mysql_client)
    elif argv[1] == 'analyze':
        with MySqlClient() as mysql_client:
            load_analytical_data(mysql_client)
    else:
        print(f'unknown argument: {argv[1]}')
