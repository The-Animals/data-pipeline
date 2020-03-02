from sys import argv
from preprocess.webscraping import get_images
from storage_clients import MinioClient

IMAGES_URL ='http://www.assembly.ab.ca/net/index.aspx?p=mla_report&memPhoto=True&alphaboth=True&alphaindex=True&build=y&caucus=All&conoffice=True&legoffice=True&mememail=True'

minio_client = MinioClient()

if __name__ == '__main__':
    if len(argv) == 2:
        IMAGES_URL = argv[1]

    df = get_images(IMAGES_URL)

    # for date_code, url in zip(documents['DateCode'], documents['URL']):
    #     print(f'parsing: {date_code}, {url}')
    #     sp = SpeechParser(url, mlas['MLALastName'])
    #     sp.parseData()
    #     info = sp.getInfo()
    #     print("loading data to minio")
    #     for speaker, speeches in info['speakers'].items():
    #         data = ' '.join(speeches)
    #         bytes_data = BytesIO(data.encode('utf-8'))
    #         length = len(data)
    #         minio_client.remove_object("speeches", f'{speaker}/{date_code}')
    #         minio_client.put_object("speeches", f'{speaker}/{date_code}', bytes_data, length)
