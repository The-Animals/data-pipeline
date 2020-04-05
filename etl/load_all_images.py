from sys import argv
from io import BytesIO
from preprocess.webscraping import get_images
from storage_clients import MinioClient
import urllib.request as urllib

IMAGES_URL ='http://www.assembly.ab.ca/net/index.aspx?p=mla_report&memPhoto=True&alphaboth=True&alphaindex=True&build=y&caucus=All&conoffice=True&legoffice=True&mememail=True'

minio_client = MinioClient()

if __name__ == '__main__':
    if len(argv) == 2:
        IMAGES_URL = argv[1]

    images = get_images(IMAGES_URL)

    assert len(images) == 87  # number of MLAs

    for image in images:
        name = image["Name"]
        url = image["URL"]
        print(f"Loading image to minio for {name}")

        resource = urllib.urlopen(url).read()
        bytes_data = BytesIO(resource)
        length = len(resource)
        minio_client.remove_object("images", f'{name}.jpg')
        minio_client.put_object("images", f'{name}.jpg', bytes_data, length)
