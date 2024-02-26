from __future__ import annotations
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement as RemoteWebElement
from selenium.webdriver.support.select import Select
import time


class WebElement:
    def __init__(self, browser: webdriver.Chrome, by: str, identifier: str, delay: float = -1) -> None:
        self.__browser = browser
        if delay > 0:
            WebDriverWait(self.__browser, delay).until(
                EC.presence_of_element_located((by, identifier)))
        self.__web_element = self.__browser.find_element(by, identifier)
    
    def fill_dropdown_input(self, input_value: str, delay: float = 1) -> None:
        self.fill_input(input_value)
        self.fill_input(Keys.ENTER)
        
        time.sleep(delay)
        
    def fill_input(self, input_value: str, delay: float = 1) -> None:
        self.__web_element.send_keys(input_value)
        
        time.sleep(delay)
    
    def select_by_value(self, value: str, delay: float = 1) -> None:
        select_el = Select(self.__web_element)
        select_el.select_by_value(value)
        
        time.sleep(delay)
    
    def submit_button(self):
        self.__web_element.submit()
    
    def click(self):
        self.__web_element.click()
    
    def get_attribute(self, attribute: str):
        return self.__web_element.get_attribute(attribute)
    