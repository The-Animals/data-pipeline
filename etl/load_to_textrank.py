from io import BytesIO

from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser

minio_client = MinioClient()
mysql_client = MySqlClient()

def load_all_speeches():
    mlas = mysql_client.execute_query("SELECT * FROM mlas")

    for mla in mlas:
        print("{0}:\n\n{1}".format(mlas['MLALastName'], list_objects(mlas['MLALastName'])))

if __name__ == '__main__':
    load_all_speeches()
