import re

from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser
from nltk.tokenize import sent_tokenize

from textrank import MLA, Session, Sentence, Summarizer
from pandas import DataFrame
from storage_clients import DbSchema

minio_client = MinioClient()

bucketName = 'speeches'

def run_textrank():
    mlas = load_from_minio() # loads information from minio to list of MLA classes
    table = DbSchema.ranks
    with MySqlClient() as mysql_client:
        try:
            mysql_client.drop_table(table)
        except:
            print("Failed to drop ranks table")

        try:
            mysql_client.create_table(table)
        except:
            print("Failed to create ranks table")

    for mla in mlas:
        print('Running summarizer for {0}...'.format(mla.name))
        summarizer = Summarizer(mla)
        save_to_sql(mla, table)


def save_to_sql(mla, table):
    print('Uploading summary results to SQL for {0}...'.format(mla.name))
    summaryInfo = []
    mlaId = mla.id
    with MySqlClient() as mysql_client:
        try:
            mysql_client.execute('DROP VIEW summaries_{0}'.format(mla.id))
        except:
            print('Failed to drop view for MLA {0}'.format(mla.name))

        for session in mla.sessions:
            sessionId = session.id
            for sentence in session.sentences:
                summaryInfo.append({
                    'MLAId': mlaId,
                    'DocumentId': sessionId,
                    'Sentence': sentence.text.encode('utf-8'),
                    'Rank': sentence.rank,
                })

        df = DataFrame(summaryInfo)
        try:
            mysql_client.append_data(table, df)
            mysql_client.execute('CREATE VIEW summaries_{0} as SELECT * FROM ranks WHERE MLAId = {0}'.format(mla.id))
        except:
            print('Failed to upload summary results to SQL for {0}...'.format(mla.name))


def load_from_minio():
    mlas = []
    buckets = minio_client.list_objects(bucketName) # gets buckets (named after MLAs)

    print("Starting load from Minio client...")
    with MySqlClient() as mysql_client:
        for bucket in buckets:
            bucket = bucket.object_name # replace class with name
            name = bucket.split('_')[-1][:-1] # mla name
            print("Loading MLA data for {0} from Minio...".format(name))

            try:
                mlaId = mysql_client.read_data("SELECT RidingNumber FROM mlas WHERE LastName = \"{0}\"".format(name))['RidingNumber'][0] # get id from table
            except:
                print("Failed to fetch SQL data for MLA {0}. Please ensure the MLA is in the table and try again.".format(name))
                continue

            mla = MLA(bucket[:-1], mlaId) # create a new MLA class
            files = minio_client.list_objects(bucketName, prefix=name+'/', recursive=True) # get sessions contained in files

            for file in files:
                file = file.object_name # get the file
                sessionName = file.split('/')[1]
                try:
                    sessionId = mysql_client.read_data("SELECT Id from documents WHERE DateCode = \"{0}\"".format(sessionName))['Id'][0] # get id from table
                except:
                    print("Failed to fetch SQL data for document {0} of MLA {1}. Please ensure the MLA is in the table and try again.".format(sessionName, name))
                    continue

                session = Session(sessionName, mla, sessionId) # create a new Session class (split is because file name contains bucket name)
                sentences = minio_client.get_object(bucketName, file) # open HTTP stream to file containing sentences
                speech = b'' # will hold entire byte stream

                for s in sentences.stream(65536):
                    speech += s

                try:
                    speech = speech.decode('utf-8') # decode from bytecode
                except:
                    print("Error on file {0}".format(file))
                    continue

                # TO BE REMOVED AFTER SPEECH PARSER INTEGRATION --------------------------------------------------------------------------------------
                speech = speech.replace('\n', ' ') # remove trailing \n
                speech = speech.replace('. . .', '<inaudible>')
                for key, value in chars.items():
                    speech = speech.replace(key, value)
                # TO BE REMOVED AFTER SPEECH PARSER INTEGRATION --------------------------------------------------------------------------------------

                for s in sent_tokenize(speech):
                    sentence = Sentence(s.strip(), session) # create a new Sentence class

            mlas += [mla] # add mla data to list
    print("Finished load from Minio client...")
    return mlas

def replace_chars(match):
    char = match.group(0)
    return chars[char]

if __name__ == "__main__":
    run_textrank()
