import re
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from pkgutil import get_data
from storage_clients import MinioClient, MySqlClient
from topic_analysis import JSTAnalyzer

minio_client = MinioClient()

stopwords = {word.strip() for word in str(get_data('data', 'stopwords.txt').decode('utf-8')).split('\n')}

def build_jst_model(mysql_client):
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)
    jst_analyzer.load_training_data()
    jst_analyzer.train_model()
    jst_analyzer.load_test_data()
    jst_analyzer.test_model()

def run_jst_model(mysql_client):
    jst_analyzer = JSTAnalyzer(minio_client, mysql_client, stopwords)
    jst_analyzer.analyze()

if __name__ == '__main__':
    with MySqlClient() as mysql_client:
        build_jst_model(mysql_client)
