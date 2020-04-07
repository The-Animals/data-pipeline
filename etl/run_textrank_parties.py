import re

from storage_clients import MySqlClient, MinioClient
from preprocess.speech_parser import SpeechParser
from nltk.tokenize import sent_tokenize

from textrank import MLA, Session, Sentence, Summarizer
from pandas import DataFrame
from storage_clients import DbSchema
from pkgutil import get_data


import time

#minio_client = MinioClient()
#null_sentences = {sentence.strip() for sentence in str(get_data('data', 'sentences.txt').decode('utf-8')).split('\n')}
number_of_sentences = 20

def run_textrank(mysql_client):
    table = DbSchema.ranks

    # mysql_client.drop_table(table)
    # mysql_client.create_table(table)

    i = 1
    s = 0
    startTime = time.clock()
    for sentences in load_data(mysql_client, number_of_sentences):
        print(f'processing party {i} / 2')
        # loads information from minio to list of MLA classes
        if sentences != []:
            summarizer = Summarizer(sentences)
        save_to_sql(sentences, mysql_client)
        i += 1


def load_data(mysql_client, number_of_sentences):
    """
    generator for querying top mla sentences per party

    fetches {number_of_sentences} sentences from each mla in party and performs textrank on them
    """

    party_table = mysql_client.read_data("SELECT * FROM parties")
    mla_table = mysql_client.read_data("SELECT * FROM mlas")

    for party_index, party_row in party_table.iterrows():
        sentences = []
        for mla_index, mla_row in mla_table.iterrows():
            if party_row.Name == mla_row.Caucus:
                sentence_table = mysql_client.read_data(f"SELECT * FROM summaries_{mla_row.Id} WHERE MLARank <= {number_of_sentences}")
                for sentence_index, sentence_row in sentence_table.iterrows():
                    sentences += [Sentence(sentence_row.Sentence, None, sentence_row.Id)]
        yield sentences


def save_to_sql(sentences, mysql_client):

    for sentence in sentences:
        mysql_client.execute(f'UPDATE ranks SET PartyRank = {sentence.rank} WHERE Id = {sentence.id}')


if __name__ == "__main__":
    with MySqlClient() as mysql_client:
        run_textrank(mysql_client)
