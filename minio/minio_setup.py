import configparser
from minio import Minio
from minio.error import (BucketAlreadyOwnedByYou, 
    BucketAlreadyExists)


def setup():
    config, secrets = get_configuration()
    
    print(f'Attempting connection to: {config["dev"]["URL"]}')

    minioClient = Minio(config['dev']['URL'], 
        access_key=secrets['secrets']['AccessKey'], 
        secret_key=secrets['secrets']['SecretKey'],
        secure=False)
    
    try: 
        minioClient.make_bucket("speeches") 
    except (BucketAlreadyOwnedByYou, BucketAlreadyExists):
        print("Bucket Already Exists: speeches")

    try: 
        minioClient.make_bucket("images")
    except (BucketAlreadyOwnedByYou, BucketAlreadyExists):
        print("Bucket Already Exists: images")     


def get_configuration(): 
    secrets = configparser.ConfigParser()
    secrets.read("secrets.conf")
    config = configparser.ConfigParser()
    config.read("config.conf")
    return config, secrets


if __name__ == '__main__': 
    setup()