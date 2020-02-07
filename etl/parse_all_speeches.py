from io import BytesIO

from storage_clients import MinioClient
from storage_clients import MySqlClient
from preprocess.speech_parser import SpeechParser

minio_client = MinioClient()
mysql_client = MySqlClient()


def parse_all_speeches(): 
    documents = mysql_client.execute_query("SELECT * FROM documents")
    mlas = mysql_client.execute_query("SELECT * FROM mlas")

    for date_code, url in zip(documents['DateCode'], documents['URL']):
        print(f'parsing: {date_code}, {url}')
        sp = SpeechParser(url, mlas['MLALastName'])
        sp.parseData()
        info = sp.getInfo()
        print("loading data to minio")
        for speaker, speeches in info['speakers'].items():
            data = ' '.join(speeches)
            bytes_data = BytesIO(data.encode('utf-8'))
            length = len(data)
            minio_client.put_object("speeches", f'{speaker}/{date_code}', bytes_data, length)


if __name__ == '__main__':
    parse_all_speeches()