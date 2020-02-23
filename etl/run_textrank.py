import re

from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser

from textrank import MLA, Session, Sentence, Summarizer

minio_client = MinioClient()
mysql_client = MySqlClient()

bucketName = 'speeches'
validPeriods = ['Mr.', 'Ms.', 'Mrs.', 'Dr.', 'B.C.']

def run_textrank():
    mlas = load_from_minio() # loads information from minio to list of MLA classes

    for mla in mlas:
        print('---------------------------------------------------------------------------------------------------------------')
        summarizer = Summarizer(mla)
        print_top_sentences(mla, 10)


def print_top_sentences(mla, sentences):
    ranks = []
    for sentence in mla.sentences:
        ranks += [(sentence.rank, sentence.text)]
    ranks.sort(reverse=True)

    print("MLA: {0}".format(mla.name))
    print()
    for i in range(0, sentences):
        print("{0}: {1}\n".format(i + 1, ranks[i][1]))


def load_from_minio():
    mlas = []
    buckets = minio_client.list_objects(bucketName) # gets buckets (named after MLAs)

    for bucket in buckets:
        bucket = bucket.object_name # replace class with name
        mla = MLA(bucket[:-1]) # create a new MLA class (-1 to remove folder /)
        files = minio_client.list_objects(bucketName, prefix=mla.name+'/', recursive=True) # get sessions contained in files

        for file in files:
            file = file.object_name # get the file
            session = Session(file.split('/')[1], mla) # create a new Session class (split is because file name contains bucket name)
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
                sentence = Sentence(s.strip(), session) # create a new Sentence class

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
