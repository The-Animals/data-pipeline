import re

from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser
from nltk.tokenize import sent_tokenize

from textrank import MLA, Session, Sentence, Summarizer
from pandas import DataFrame

minio_client = MinioClient()
mysql_client = MySqlClient()

bucketName = 'speeches'

def run_textrank():
    sentenceId = 1

    mlas = load_from_minio() # loads information from minio to list of MLA classes

    for mla in mlas:
        print('Running summarizer for {0}...'.format(mla.name))
        summarizer = Summarizer(mla)

        print('Uploading summary results to SQL for {0}...'.format(mla.name))
        summaryInfo = []
        mlaId = mla.id
        for session in mla.sessions:
            sessionId = session.id
            for sentence in session.sentences:
                summaryInfo.append({
                    'MLAId': mlaId,
                    'SessionId': sessionId,
                    'Sentence': sentence.text.encode('utf-8'),
                    'Rank': sentence.rank,
                    'Id': sentenceId
                })
                sentenceId += 1

        conn = mysql_client.get_connection_v2()
        df = DataFrame(summaryInfo)
        try:
            df.to_sql('ranks', con=conn, if_exists='replace')
        except:
            print('Failed to upload summary results to SQL for {0}...'.format(mla.name))


def print_top_sentences(mla, sentences):
    ranks = []
    for sentence in mla.sentences:
        ranks += [(sentence.rank, sentence.text)]
    ranks.sort()

    print("\nMLA: {0}".format(mla.name))
    print()
    for i in range(0, sentences):
        try:
            print("{0}: {1}\n".format(i + 1, ranks[i][1]))
        except:
            break


def load_from_minio():
    mlas = []
    buckets = minio_client.list_objects(bucketName) # gets buckets (named after MLAs)

    print("Starting load from Minio client...")
    for bucket in buckets:
        bucket = bucket.object_name # replace class with name
        name = bucket[:-1] # mla name
        print("Loading MLA data for {0} from Minio...".format(name))
        try:
            mlaId = mysql_client.execute_query("SELECT RidingNumber FROM mlas WHERE MLALastName = \"{0}\"".format(name))['RidingNumber'][0] # get id from table
        except:
            print("Failed to fetch SQL data for MLA {0}. Please ensure the MLA is in the table and try again.".format(name))
            continue

        mla = MLA(bucket[:-1], mlaId) # create a new MLA class
        files = minio_client.list_objects(bucketName, prefix=name+'/', recursive=True) # get sessions contained in files

        for file in files:
            file = file.object_name # get the file
            sessionName = file.split('/')[1]
            try:
                sessionId = mysql_client.execute_query("SELECT Id from documents WHERE DateCode = \"{0}\"".format(sessionName))['Id'][0] # get id from table
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

            speech = speech.replace('\n', ' ') # remove trailing \n

            for s in sent_tokenize(speech):
                sentence = Sentence(s.strip(), session) # create a new Sentence class

        mlas += [mla] # add mla data to list
    print("Finished load from Minio client...")
    return mlas

if __name__ == "__main__":
    run_textrank()
