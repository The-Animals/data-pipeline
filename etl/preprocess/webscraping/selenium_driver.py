from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException

DRIVER_TIMEOUT = 10 

class Driver(object):
    """Singleton class for interacting with the selenium webdriver object"""

    instance = None

    class SeleniumDriverNotFound(Exception):
        pass

    @classmethod
    def get_instance(cls):
        if cls.instance == None:
            cls.instance = Driver()
        return cls.instance

    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def get_driver(self):
        return self.driver

    def stop_instance(self):
        self.driver.quit()
        instance = None

    def navigate(self, url):
        self.driver.get(url)

    def _execute_with_wait(self, condition):
        return WebDriverWait(self.driver, DRIVER_TIMEOUT).until(condition)

    def element_exists(self, locator):
        try:
            self._execute_with_wait(
                ec.presence_of_element_located(
                    (locator[0], locator[1]))
            )
            return True
        except TimeoutException:
            return False

    def get_element(self, locator):
        if not self.element_exists(locator):
            raise NoSuchElementException(f"Could not find {locator}")

        return self.driver.find_element(locator[0], locator[1])

    def get_elements(self, locator): 
        if not self.element_exists(locator): 
            raise NoSuchElementException(f"Could not find {locator}")

        return self.driver.find_elements(locator[0], locator[1])


driver = Driver.get_instance()