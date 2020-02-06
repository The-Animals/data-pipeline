from selenium_driver import driver
from selenium.webdriver.common.by import By
from pandas import DataFrame
from datetime import datetime


time_of_day = { 
    "Morning": (9, 0),
    "Afternoon": (13, 30),
    "Evening": (19, 30),
}

def get_date_code(date_string): 
    """
    Given date in Hansard date format:
        ie. Wednesday, December 4, 2019, Evening
    Convert to date code: 
        ie. 04-12-2019-E
    """
    tok = date_string.split(', ')
    date = datetime.strptime(', '.join(tok[1:3]), "%B %d, %Y")
    return f'{date.strftime("%d-%m-%Y")}-{tok[-1][0]}'


def get_date(date_string):
    """
    Given date in Hansard date format:
        ie. Wednesday, December 4, 2019, Evening
    Convert to date code: 
        ie. datetime()
    """
    tok = date_string.split(', ')
    time = time_of_day[tok[-1]]
    date = datetime.strptime(', '.join(tok[1:3]), "%B %d, %Y").replace(hour=time[0], minute=time[1])
    return date


def extract_document_information(date_element, document_element):
    """
    Given 2 selenium elements, one containing a data, and one containing the 
    Hansard document link, extract the data text, and the document url
    """
    date = date_element.text.split('\n')[0]
    document_element.click()
    driver.switch_to_last_tab()
    driver.element_exists((By.XPATH, "//body/img"))
    url = driver.current_window_url()
    driver.close_current_window()
    driver.switch_to_main_tab()
    return (date, url)


def get_urls(hansard_url):
    """
    Get all transciript URLs that are currently available at the main hansard page. 

    Returns a data frame that contains date info related to the document
    """
    driver.navigate(hansard_url)

    html_doc_links = driver.get_elements((By.XPATH, "//input[@src='images/text_html.gif']"))
    date_elements = driver.get_elements((By.XPATH, "//td[contains(text(), ', ')]"))

    assert len(html_doc_links) == len(date_elements)

    document_info = []

    for i in range(len(html_doc_links)):
        date_string, url = extract_document_information(date_elements[i], html_doc_links[i])
        document_info.append({
            "Id": '',
            'DateCode': get_date_code(date_string), 
            'DateString': date_string, 
            'Date': get_date(date_string), 
            'URL': url
        })
        print(f"'DateCode': {get_date_code(date_string)}, 'DateString': {date_string}, 'Date': {get_date(date_string)}, 'URL': {url}")
    
    driver.stop_instance()

    return DataFrame(document_info)
    

def overwrite_urls(df, filepath):
    """
    Overwrite a file from a list
    """
    print(f'writing to file: {filepath}')
    with open(filepath, 'w+') as file:
        file.write(df.to_csv(index=False)) 
