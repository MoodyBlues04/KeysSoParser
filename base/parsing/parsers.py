from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from abc import ABC, abstractmethod
from base.parsing.web_elements import WebElement
from os import getenv
from time import sleep


class ParsingResult:
    def __init__(self, result: dict) -> None:
        self.__result = result
    
    def get_result(self) -> dict:
        return self.__result
    
    
class Parser(ABC):
    _browser: webdriver.Chrome
    
    def __init__(self) -> None:
        super().__init__()
        self._browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
    @abstractmethod
    def parse(self) -> ParsingResult:
        pass
    
    def _get_web_element(self, by: str, identifier: str, delay: float = -1) -> WebElement:
        return WebElement(self._browser, by, identifier, delay)


class KeysSoParserDto:
    def __init__(self, search: str) -> None:
        self.search = search


class KeysSoParser(Parser):
    SEARCH_URL = 'https://www.keys.so/ru/rsya'
    LOGIN_URL = 'https://www.keys.so/ru/login'
    
    __LOGIN_EMAIL_INPUT_ID = 'login__email'
    __LOGIN_PASSWORD_INPUT_ID = 'login__pass'
    __LOGIN_BUTTON_XPATH = '//*[@id="keysoApp"]/div[3]/div/div/div[2]/div/form/div[3]/button[1]'
    
    __SEARCH_INPUT_XPATH = '//*[@id="keysoApp"]/div[3]/div[3]/div/div[1]/div/div/div[1]/div/div[1]/div/input'
    __SEARCH_OPERATOR_XPATH = '//*[@id="keysoApp"]/div[3]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/div/select'
    __SEARCH_BUTTON_XPATH = '//*[@id="keysoApp"]/div[3]/div[3]/div/div[1]/div/div/div[3]/a[1]'
    
    __SEARCH_RESULT_CONTAINER_XPATH = '//*[@id="keysoApp"]/div[3]/div[3]/div/div[2]/div/div[3]/table/tbody/tr/td/div/div'
    __SEARCH_RESULT_ITEM_CLASS = 'rsya-item__container rsya_item'
    __SEARCH_NEXT_PAGE_XPATH = '//*[@id="keysoApp"]/div[3]/div[3]/div/div[2]/div/div[2]/div[1]/ul/li[9]/a'
    
    __dto: KeysSoParserDto
    
    def __init__(self, dto: KeysSoParserDto) -> None:
        super().__init__()
        self.__dto = dto

    def parse(self) -> ParsingResult:
        try:
            # TODO split to classes
            self.__login()
            sleep(3)
            self.__search()
            sleep(10)
        finally:
            self._browser.quit()
        
        return ParsingResult({'test': 'test'})
    
    def __login(self) -> None:
        self._browser.get(self.LOGIN_URL)
        self._get_web_element(By.ID, self.__LOGIN_EMAIL_INPUT_ID, 5).fill_input(getenv('KEYS_SO_EMAIL'))
        self._get_web_element(By.ID, self.__LOGIN_PASSWORD_INPUT_ID).fill_input(getenv('KEYS_SO_PASSW'))
        self._get_web_element(By.XPATH, self.__LOGIN_BUTTON_XPATH).submit_button()
    
    def __search(self) -> None:
        self._browser.get(self.SEARCH_URL)
        sleep(10)
        self._get_web_element(By.XPATH, self.__SEARCH_INPUT_XPATH, 5).fill_input(self.__dto.search)
        self._get_web_element(By.XPATH, self.__SEARCH_OPERATOR_XPATH, 5).select_by_value('LIKE')
        self._get_web_element(By.XPATH, self.__SEARCH_BUTTON_XPATH).click()
        
        while True:
            self.__parse_search_page()
            # self.__next_page()
            break
    
    def __parse_search_page(self) -> None:
        search_items_container = self._browser.find_element(By.XPATH, self.__SEARCH_RESULT_CONTAINER_XPATH)
        print(search_items_container.get_attribute('class'))
        for search_result_item in search_items_container.find_elements(By.CLASS_NAME, self.__SEARCH_RESULT_ITEM_CLASS):
            print(1, search_result_item.get_attribute('class'))