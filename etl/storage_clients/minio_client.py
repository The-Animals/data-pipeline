from io import StringIO
from minio import Minio
from minio.error import (BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

from .utils import get_config


class MinioClient(Minio):

    def __init__(self):
        config = get_config()
        super().__init__(
            config['minio']['url'],
            access_key=config['minio']['access_key'],
            secret_key=config['minio']['secret_key'],
            secure=False
        )