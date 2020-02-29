from selenium.webdriver.common.by import By
from pandas import DataFrame

from storage_clients import MySqlClient, DbSchema
from preprocess.webscraping.utils import get_date_code, get_date

"""
Get pdf document urls from the hansard website and store them in the 
database in the 'documents' table
"""


HANSARD_SESSION_URL ='https://www.assembly.ab.ca/net/index.aspx?p=han&section=doc&fid=1'

def get_urls():
    """
    Get all transcript URLs that are currently available at the main hansard page. 

    Returns a data frame that contains date info related to the document
    """
    from preprocess.webscraping.selenium_driver import driver
    driver.navigate(HANSARD_SESSION_URL)

    input("Please navigate the hansard to the proper page and then press enter to continue")

    date_elements = driver.get_elements((By.XPATH, "//td[contains(text(), ', ')]"))
    pdf_doc_elements = driver.get_elements((By.XPATH, "//a[contains(text(), 'PDF')]"))

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
        print(f"'DateCode': {get_date_code(date_string)}, 'DateString': {date_string}, 'Date': {get_date(date_string)}, 'Url': {url}")
    
    driver.stop_instance()

    return DataFrame(document_info)


def overwrite_documents(): 
    table = DbSchema.documents

    docs = get_urls()

    with MySqlClient() as mysql_client:
        print('writing new documents to database')
        mysql_client.overwrite_table(table, docs)


def append_documents(): 
    table = DbSchema.documents

    with MySqlClient() as mysql_client:
        print('reading previously seen documents from database')
        prev_docs = mysql_client.read_data('documents')

    docs = get_urls()
    new_date_codes = list(set(docs['DateCode']) - set(prev_docs['DateCode']))
    new_docs = docs.loc[docs['DateCode'].isin(new_date_codes)]

    with MySqlClient() as mysql_client:
        print('writing new documents to database')
        mysql_client.append_data(table, new_docs)


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
