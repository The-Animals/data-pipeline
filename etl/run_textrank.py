from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from io import BytesIO
import re
import pkgutil


from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser

from nltk.corpus import stopwords

from textrank_algorithm import MLA, Session, Sentence
from textrank_algorithm import TextRankSummarizer as Summarizer

minio_client = MinioClient()
mysql_client = MySqlClient()

bucketName = 'speeches'
validPeriods = ['Mr.', 'Ms.', 'Mrs.', 'Dr.', 'B.C.']

# def get_stop_words():
#     stopwords_data = pkgutil.get_data("sumy", "data/stopwords/english.txt")
#     return frozenset(w.rstrip() for w in str(stopwords_data).splitlines() if w)

def run_textrank():
    mlas = load_from_minio() # loads information from minio to list of MLA classes
    mla = mlas[0]

    LANGUAGE = "english"
    SENTENCES_COUNT = 10

    summarizer = Summarizer()
    summarizer.stop_words = frozenset(stopwords.words('english'))#get_stop_words(LANGUAGE)

    for sentence in summarizer(mla, SENTENCES_COUNT):
        print(sentence.sentence)



def load_from_minio():
    mlas = []
    buckets = minio_client.list_objects(bucketName) # gets buckets (named after MLAs)

    for bucket in buckets:
        bucket = bucket.object_name # replace class with name
        mla = MLA(bucket[:-1]) # create a new MLA class (-1 to remove folder /)
        files = minio_client.list_objects(bucketName, prefix=mla.name+'/', recursive=True) # get sessions contained in files

        for file in files:
            file = file.object_name # get the file
            session = Session(file.split('/')[1]) # create a new Session class (split is because file name contains bucket name)
            sentences = minio_client.get_object(bucketName, file) # open HTTP stream to file containing sentences
            speech = b'' # will hold entire byte stream

            for s in sentences.stream(65536):
                speech += s

            try:
                speech = speech.decode('iso-8859-1') # decode from bytecode
            except:
                print("Error on file {0}".format(file))
                continue

            speech = speech.replace('\n', ' ') # remove trailing \n

            for s in sentence_split(speech):
                sentence = Sentence(s.strip()) # create a new Sentence class
                session.addSentence(sentence) # add sentence to active session class

            mla.addSession(session) # add session to active mla class

        mlas += [mla] # add mla data to list
        break
    return mlas


def sentence_split(sentences):
    regexString = r'' # starting regex string

    for v in validPeriods:
        regexString += "(?<!{0})".format(v) # will ignore anything in validPeriods on split
    regexString += '(?<=[\.!?]) ' # add sentence splitter at the end

    return re.split(regexString, sentences)





if __name__ == "__main__":
    run_textrank()
