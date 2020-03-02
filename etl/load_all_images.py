from sys import argv
from preprocess.webscraping import get_images
from storage_clients import MySqlClient, DbSchema

IMAGES_URL ='http://www.assembly.ab.ca/net/index.aspx?p=mla_report&memPhoto=True&alphaboth=True&alphaindex=True&build=y&caucus=All&conoffice=True&legoffice=True&mememail=True'

mysql_client = MySqlClient()

def load_from_webpage():
    df = get_images(IMAGES_URL)
    table = DbSchema.images

    with MySqlClient() as mysql_client:
        try:
            mysql_client.create_table(table)
        except:
            print("Failed to create image table")
            return

        try:
            mysql_client.append_data(table, df)
        except:
            print("Failed to append data to image table")


if __name__ == '__main__':
    if len(argv) == 2:
        IMAGES_URL = argv[1]

    load_from_webpage()
