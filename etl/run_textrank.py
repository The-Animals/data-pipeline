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
    mlas = load_from_minio()  # loads information from minio to list of MLA classes
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
        print('Running summarizer for {0} {1}...'.format(mla.firstname, mla.lastname))
        summarizer = Summarizer(mla)
        save_to_sql(mla, table)


def save_to_sql(mla, table):
    print('Uploading summary results to SQL for {0} {1}...'.format(mla.firstname, mla.lastname))
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
            mysql_client.execute(
                'CREATE VIEW summaries_{0} as SELECT * FROM ranks WHERE MLAId = {0}'.format(mla.id))
        except:
            print(
                'Failed to upload summary results to SQL for {0}...'.format(mla.name))


def load_from_minio():
    mlas = []
    # gets buckets (named after MLAs)
    buckets = minio_client.list_objects(bucketName)

    print("Starting load from Minio client...")
    with MySqlClient() as mysql_client:
        for bucket in buckets:
            bucket = bucket.object_name  # replace class with name
            firstname = bucket.split('_')[0]
            lastname = bucket.split('_')[-1][:-1]
            print("Loading MLA data for {0} {1} from Minio...".format(
                firstname, lastname))

            # try:
            mlaId = mysql_client.read_data("SELECT Id FROM mlas WHERE FirstName = \"{0}\" and LastName = \"{1}\"".format(firstname, lastname))['Id'][0]  # get id from table
            # except:
                # print(
                    # "Failed to fetch SQL data for MLA {0} {1}. Please ensure the MLA is in the table and try again.".format(firstname, lastname))
                # continue

            mla = MLA(firstname, lastname, mlaId)  # create a new MLA class
            # get sessions contained in files
            files = minio_client.list_objects(
                bucketName, prefix=f'{firstname}_{lastname}/', recursive=True)

            for file in files:
                file = file.object_name  # get the file
                sessionName = file.split('/')[1]
                try:
                    sessionId = mysql_client.read_data("SELECT Id from documents WHERE DateCode = \"{0}\"".format(
                        sessionName))['Id'][0]  # get id from table
                except:
                    print("Failed to fetch SQL data for document {0} of MLA {1} {2}. Please ensure the MLA is in the table and try again.".format(
                        sessionName, firstname, lastname))
                    continue

                # create a new Session class (split is because file name contains bucket name)
                session = Session(sessionName, mla, sessionId)
                # open HTTP stream to file containing sentences
                sentences = minio_client.get_object(bucketName, file)
                speech = b''  # will hold entire byte stream

                for s in sentences.stream(65536):
                    speech += s

                try:
                    speech = speech.decode('utf-8')  # decode from bytecode
                except:
                    print("Error on file {0}".format(file))
                    continue

                for s in sent_tokenize(speech):
                    # create a new Sentence class
                    sentence = Sentence(s.strip(), session)

            mlas += [mla]  # add mla data to list

    print("Finished load from Minio client...")
    return mlas


def replace_chars(match):
    char = match.group(0)
    return chars[char]


if __name__ == "__main__":
    run_textrank()
