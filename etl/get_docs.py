from sys import argv
from os.path import abspath
from preprocess.webscraping import get_urls, overwrite_urls


HANSARD_SESSION_URL ='https://www.assembly.ab.ca/net/index.aspx?p=han&section=doc&fid=1'


if __name__ == '__main__':
    if len(argv) < 2:
        raise Exception("Usage: python3 get_urls.py <out_file_path> [<hansard_url>]")
    elif len(argv) == 3:
        HANSARD_SESSION_URL = argv[2]

    filepath = abspath(argv[1])
    df = get_urls(HANSARD_SESSION_URL)
    overwrite_urls(df, filepath)
