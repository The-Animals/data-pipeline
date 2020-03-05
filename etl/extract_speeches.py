from io import BytesIO

from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser

minio_client = MinioClient()

"""
From raw text objects contained in the MinIO instance, 
parse out the speeches and attribute them to the different 
MLAs. Store speeches back in the MinIO instance attributed 
to the MLA that said them. 
"""


def parse_all_speeches():
    with MySqlClient() as mysql_client:
        documents = mysql_client.read_data("SELECT * FROM documents")
        mlas = mysql_client.read_data("SELECT * FROM mlas")

    # Construct a dictionary mapping MLA names as they are found in the
    # hansard with a '-' delimited firstname-lastname string.
    mla_lookup = {k: f'{f}_{l}' for (k, (f, l)) in zip(
        mlas['HansardName'], zip(mlas['FirstName'], mlas['LastName']))}

    sp = SpeechParser(set(mla_lookup.keys()))

    for date_code in documents['DateCode']:
        print(f'parsing: {date_code}')

        raw_text = minio_client.get_object(
            'rawtext', date_code).read().decode('utf-8')
        speeches = sp.parse_speeches(raw_text)

        print("loading data to minio")
        for speaker, speeches in speeches.items():
            mla = mla_lookup[speaker]
            data = '\n'.join(speeches)
            bytes_data = BytesIO(data.encode('utf-8'))
            length = bytes_data.getbuffer().nbytes
            minio_client.put_object(
                "speeches", f'{mla}/{date_code}', bytes_data, length)


if __name__ == '__main__':
    parse_all_speeches()
