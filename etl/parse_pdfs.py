import requests
from io import StringIO, BytesIO
from os import SEEK_END, SEEK_SET
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from storage_clients import MySqlClient, MinioClient

"""
Take document URLs from the documents table, download the pdfs, 
run them through a pdf -> text parser and store the raw text in the 
minio instance. 
"""

def raw_text_from_pdf(url):
    print(f'getting document at {url}')
    r = requests.get(url)
    output_string = StringIO()
    parser = PDFParser(BytesIO(r.content))
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)

    return BytesIO(output_string.getvalue().encode('utf-8'))


def parse_pdfs(): 

    with MySqlClient() as mysql_client: 
        documents = mysql_client.read_data('SELECT DateCode, Url FROM documents')

    minio_client = MinioClient()

    for date_code, url in zip(documents['DateCode'], documents['Url']): 
        raw_text = raw_text_from_pdf(url)
        length = raw_text.getbuffer().nbytes
        minio_client.remove_object("rawtext", date_code)
        minio_client.put_object("rawtext", date_code, raw_text, length)


if __name__ == '__main__': 
    parse_pdfs()