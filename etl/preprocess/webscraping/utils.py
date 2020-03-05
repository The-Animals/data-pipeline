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

def extract_image_information(image_element):
    """
    Given an image selenium element containing the MLA image link, extract the MLA last name and image url
    """
    root_url = 'assembly.ab.ca'
    name = image_element.get_attribute('alt')
    name = name.replace(' ', '_')
    name = name.title()
    url = image_element.get_attribute('src').replace('..', root_url)

    return name, url

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

def get_images(images_url):
    """
    Get all MLA images that are currently available at the hansard website.

    Returns a data fame that contains date info related to the document
    """
    driver.navigate(images_url)

    image_links = driver.get_elements((By.XPATH, "//div[@class='member']/img"))

    images_info = []

    for i in range(len(image_links)):
        name, url = extract_image_information(image_links[i])
        images_info.append({"Name": name, "URL": url})
        print(f"'Name': {name}, 'URL': {url}")

    driver.stop_instance()

    return images_info
