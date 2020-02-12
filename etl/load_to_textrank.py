from io import BytesIO

from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser

minio_client = MinioClient()
mysql_client = MySqlClient()

def load_all_speeches():
    #mlas = mysql_client.execute_query("SELECT MLALastName FROM mlas")
    #print(type(minio_client.list_objects('speeches')))
    mlas = minio_client.list_objects('speeches')
    for mla in mlas:
        speaker = mla.object_name
        print("Speaker is {0}:\n".format(speaker))
        hearings = minio_client.list_objects('speeches', prefix=speaker, recursive=True)
        sentences = ""
        for hearing in hearings:
            file = hearing.object_name

        print('\n-----------------------------')

if __name__ == '__main__':
    load_all_speeches()
