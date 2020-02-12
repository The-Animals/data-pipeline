from io import BytesIO

from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser
from textrank_algorithm import MLA, Session, Sentence

minio_client = MinioClient()
mysql_client = MySqlClient()

bucketName = 'speeches'

def load_all_speeches():

    buckets = minio_client.list_objects(bucketName)
    for bucket in buckets:
        mla = MLA(bucket.object_name)
        files = minio_client.list_objects(bucketName, prefix=mla.getName(), recursive=True)
        for file in files:
            session = Session(file.object_name)

            sentences = minio_client.get_object(bucketName, session.getDateCode())
            speech = b''
            for s in sentences.stream(65536):
                speech += s
            speech = speech.decode('utf-8')
            speech = speech.replace('\n', '')

            for sentence in speech.split('.'):
                session.addSentence(Sentence(sentence.strip()))

            mla.addSession(session)
            break
        break

if __name__ == '__main__':
    load_all_speeches()
