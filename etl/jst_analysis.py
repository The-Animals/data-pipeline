import re
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from pkgutil import get_data
from storage_clients import MinioClient, MySqlClient
from topic_analysis import JSTAnalyzer

minio_client = MinioClient()

stopwords = {word.strip() for word in str(get_data('data', 'stopwords.txt').decode('utf-8')).split('\n')}

def run_jst_analysis(mysqlclient):
    jst_analyzer = JSTAnalyzer(minio_client, mysqlclient, stopwords)
    jst_analyzer.load_training_data()
    jst_analyzer.load_test_data()
    jst_analyzer.train_model()
    jst_analyzer.test_model()

if __name__ == '__main__':
    with MySqlClient() as mysql_client:
        run_jst_analysis(mysql_client)