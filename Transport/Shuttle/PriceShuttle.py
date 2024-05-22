from unidecode import unidecode
from selenium import webdriver

from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

from unidecode import unidecode
from datetime import date, timedelta, datetime

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import pandas as pd

class ShuttleCrawler:
    def __init__(self):
        
        self.options = Options()
        #self.options.add_argument("--headless")
        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("excludeSwitches",["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument("--disable-blink-features")
        self.options.add_argument("--disable-blink-features=AutomationControlled")

        prefs = {"profile.default_content_settings.popups": 0,
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "profile.managed_default_content_settings.images": 2
        }
        self.options.add_experimental_option("prefs",prefs)

        self.driver = None
       
        ## SAVE data
        self.minPrice = 0
        self.maxPrice = 0
    
    def crawler(self, url ):

        self.driver = webdriver.Chrome(self.options)
        self.driver.get(url)
        sleep(3)
        
        actions = ActionChains(self.driver)
        try:
            buttonLowest = self.driver.find_element( By.XPATH , '//*[@id="route-fixed-left"]/div[1]/div[2]/label[5]/span[1]/input')
            actions.click(buttonLowest).perform()
            sleep(4)
            priceLowest = self.driver.find_element(By.CSS_SELECTOR ,'div.fare').text
            priceLowest = priceLowest.strip('Từ').strip().strip('đ').replace('.' , '')

            buttonHighest = self.driver.find_element( By.XPATH , '//*[@id="route-fixed-left"]/div[1]/div[2]/label[6]/span[1]/input').click()
            actions.click(buttonHighest).perform()
            sleep(3)

            priceHightest = self.driver.find_element(By.CSS_SELECTOR ,'div.fare').text
            priceHightest = priceHightest.strip('Từ').strip().strip('đ').replace('.' , '')

            self.minPrice = priceLowest
            self.maxPrice = priceHightest
        except:
            pass 


class GetPriceShuttle:
    def __init__(self , cityStart , cityEnd , datePlan ):
        ## INPUT TRANSPORT
        self.cityStart = cityStart
        self.cityEnd   = cityEnd
        self.datePlan  = datePlan
        
        self.minPrice = 0
        self.maxPrice = 0



    def getPriceShuttle(self):
        codeStart = unidecode(self.cityStart).lower().replace(' ' , '-')
        codeEnd   = unidecode(self.cityEnd).lower().replace(' ' , '-')
        url =  f'https://vexere.com/vi-VN/ve-xe-khach-tu-{codeStart}-di-{codeEnd}-129t181.html?date={self.datePlan}&v=4'

        perform = ShuttleCrawler()
        perform.crawler(url)
        self.minPrice = perform.minPrice
        self.maxPrice = perform.maxPrice



    