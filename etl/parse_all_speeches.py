from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser

minio_client = MinioClient()
mysql_client = MySqlClient()


def parse_all_speeches(): 
    documents = mysql_client.execute_query("SELECT * FROM documents LIMIT 1")
    mlas = mysql_client.execute_query("SELECT * FROM mlas")

    for url in documents['URL']:
        print(url)
        sp = SpeechParser(url)
        sp.parseData()
        info = sp.getInfo()
        print(info)


if __name__ == '__main__':
    parse_all_speeches()