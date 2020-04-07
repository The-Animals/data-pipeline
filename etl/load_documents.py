import requests
from selenium.webdriver.common.by import By
from pandas import DataFrame
from io import StringIO, BytesIO
from os import SEEK_END, SEEK_SET
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


from storage_clients import MySqlClient, MinioClient, DbSchema
from preprocess.webscraping.utils import get_date_code, get_date

"""
1.  Get pdf document urls from the hansard website and store them in the 
    database in the 'documents' table. 

2.  from url, download the pdf document

3.  from the pdf, extract raw text from the pdf

4.  store the raw text in the minio instance
"""


HANSARD_SESSION_URL = 'https://www.assembly.ab.ca/net/index.aspx?p=han&section=doc&fid=1'

"""
Take document URLs from the documents table, download the pdfs, 
run them through a pdf -> text parser and store the raw text in the 
minio instance. 
"""


def assert_document_table_format(df: DataFrame):
    counts = df.count()
    length = df.shape()[0]

    assert counts.DateCode == length
    assert counts.DateString == length
    assert counts.Date == length
    assert counts.Url == length


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


def parse_pdfs(documents):

    minio_client = MinioClient()

    for date_code, url in zip(documents['DateCode'], documents['Url']):
        raw_text = raw_text_from_pdf(url)
        assert len(raw_text) > 0
        length = raw_text.getbuffer().nbytes
        minio_client.remove_object("rawtext", date_code)
        minio_client.put_object("rawtext", date_code, raw_text, length)


def get_urls():
    """
    Get all transcript URLs that are currently available at the main hansard page. 

    Returns a data frame that contains date info related to the document
    """
    from preprocess.webscraping.selenium_driver import driver
    driver.navigate(HANSARD_SESSION_URL)

    input("Please navigate the hansard to the proper page and then press enter to continue")

    date_elements = driver.get_elements(
        (By.XPATH, "//td[contains(text(), ', ')]"))
    pdf_doc_elements = driver.get_elements(
        (By.XPATH, "//a[contains(text(), 'PDF')]"))

    assert len(pdf_doc_elements) == len(date_elements)

    document_info = []

    for date_element, pdf_doc_element in zip(date_elements, pdf_doc_elements):
        date_string = date_element.text.split('\n')[0]
        url = pdf_doc_element.get_attribute('href')

        document_info.append({
            'DateCode': get_date_code(date_string),
            'DateString': date_string,
            'Date': get_date(date_string),
            'Url': url
        })
        print(
            f"'DateCode': {get_date_code(date_string)}, 'DateString': {date_string}, 'Date': {get_date(date_string)}, 'Url': {url}")

    driver.stop_instance()

    return DataFrame(document_info)


def overwrite_documents():
    table = DbSchema.documents

    docs = get_urls()

    assert_document_table_format(docs)

    with MySqlClient() as mysql_client:
        print('writing new documents to database')
        mysql_client.overwrite_table(table, docs)

    parse_pdfs(docs)


def append_documents():
    table = DbSchema.documents

    with MySqlClient() as mysql_client:
        print('reading previously seen documents from database')
        prev_docs = mysql_client.read_data('documents')

    docs = get_urls()
    new_date_codes = list(set(docs['DateCode']) - set(prev_docs['DateCode']))
    new_docs = docs.loc[docs['DateCode'].isin(new_date_codes)]

    assert len(new_date_codes) == len(new_docs)
    assert_document_table_format(new_docs)

    with MySqlClient() as mysql_client:
        print('writing new documents to database')
        mysql_client.append_data(table, new_docs)

    parse_pdfs(new_docs)


if __name__ == '__main__':
    response = input('(o)verwrite data or (a)ppend data: ')
    if response is 'o':
        print('overwriting documents table')
        overwrite_documents()
    elif response is 'a':
        print('appending documents table')
        append_documents()
    else:
        print('unknown response')
