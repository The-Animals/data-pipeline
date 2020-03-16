import re

from storage_clients import MySqlClient, MinioClient
from preprocess.speech_parser import SpeechParser
from nltk.tokenize import sent_tokenize

from textrank import MLA, Session, Sentence, Summarizer
from pandas import DataFrame
from storage_clients import DbSchema
from pkgutil import get_data


import time

minio_client = MinioClient()
null_sentences = {sentence.strip() for sentence in str(get_data('data', 'sentences.txt').decode('utf-8')).split('\n')}

def run_textrank(mysql_client):
    table = DbSchema.ranks

    mysql_client.drop_table(table)
    mysql_client.create_table(table)

    i = 1
    s = 0
    startTime = time.clock()
    for mla in load_data(mysql_client):
        print(f'processing MLA {i} / 87: {mla.firstname} {mla.lastname}')
        # loads information from minio to list of MLA classes
        summarizer = Summarizer(mla.sentences)
        save_to_sql(mla, table, mysql_client)
        s += mla.numberOfSentences
        i += 1


def load_data(mysql_client):
    """
    generator for querying mlas, documents and loading
    speech data from the minio instance.

    this allows prefetching of metadata, while also
    only querying the mlas underlying speech data at the
    runtime for the summarizer.
    """
    bucket = 'speeches'
    mla_table = mysql_client.read_data("SELECT * FROM mlas")
    documents = mysql_client.read_data("SELECT Id, DateCode FROM documents")

    for index, row in mla_table.iterrows():
        mla = MLA(row.FirstName, row.LastName, row.Caucus, row.Id)
        # get sessions contained in files
        files = minio_client.list_objects(
            bucket, prefix=f'{mla.firstname}_{mla.lastname}', recursive=True)

        for file in files:
            date_code = file.object_name.split('/')[-1]
            document_id = int(
                documents.loc[documents['DateCode'] == date_code]['Id'])
            session = Session(date_code, mla, document_id)

            speeches_from_session = minio_client.get_object(
                bucket, file.object_name).read().decode('utf-8')

            for sent in sent_tokenize(speeches_from_session):
                # Variables
                # ---------------------------------------------------------------------------------------------
                if sent not in null_sentences:
                    sentence = Sentence(sent.strip(), session)
        yield mla


def save_to_sql(mla, table, mysql_client):
    summary_info = []

    for session in mla.sessions:
        for sentence in session.sentences:
            summary_info.append({
                'MLAId': mla.id,
                'DocumentId': session.id,
                'Sentence': str(sentence.text),
                'MLARank': sentence.rank,
                'Caucus': mla.caucus
            })

    df = DataFrame(summary_info)
    mysql_client.append_data(table, df)


if __name__ == "__main__":
    with MySqlClient() as mysql_client:
        run_textrank(mysql_client)
