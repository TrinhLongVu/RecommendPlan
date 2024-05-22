from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image
from unidecode import unidecode
from datetime import date, timedelta, datetime

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import pandas as pd
from datetime import date, timedelta, datetime
import os 

class AirlineCrawler:
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
        sleep(5)

        minPrice = sys.maxsize
        maxPrice  = 0

        try:
            checkAirline =  self.driver.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1l31rp8.r-1mnahxq')
            checkAirline =  checkAirline.find_elements( By.CSS_SELECTOR , 'div.css-1dbjc4n.r-knv0ih')
            for i in checkAirline:
                check = i.find_element( By.CSS_SELECTOR, 'div[aria-checked="false"][tabindex="0"][class="css-1dbjc4n r-1loqt21 r-1otgn73 r-1i6wzkk r-lrvibr"]')
                check.click()
                sleep(5)
                ## GET PRICE 
               
                lstPrice = self.driver.find_elements(By.CSS_SELECTOR , 'div.css-1dbjc4n.r-eqz5dr.r-1ssbvtb.r-xyw6el.r-184en5c')
                uniquePrice = set()
                for i in lstPrice:
                    getPrice = i.find_element(By.CSS_SELECTOR, 'h3.css-4rbku5.css-901oao.r-t1w4ow.r-ubezar.r-b88u0q.r-rjixqe.r-fdjqy7').text
                    getPrice = getPrice.strip('VND/khách').strip()
                    getPrice = getPrice.replace('.','')
                    getPrice = int(getPrice)
                    uniquePrice.add(getPrice)
                    if getPrice < minPrice:
                        minPrice = getPrice
                      
                    if getPrice > maxPrice:
                        maxPrice = getPrice
                   
                uniquePrice = list(uniquePrice)
                uniquePrice = sorted(uniquePrice)
                check.click()
                sleep(3)
        except:
            pass

        ## 'minPrice' ,   'maxPrice' 
        self.minPrice      = minPrice
        self.maxPrice    = maxPrice
        self.driver.quit()



class GetPriceAirline():
    def __init__(self , cityStart , cityEnd , datePlan):
        ## INPUT HERE
        self.cityStart = cityStart
        self.cityEnd   = cityEnd
        self.datePlan      = datePlan

        self.codeStart = None
        self.codeEnd   = None

        ## OUTPUT
        self.minPrice = 0 
        self.maxPrice = 0

    def getPriceAirline(self):

        perform = AirlineCrawler()
        types = [ 'ECONOMY' ]

        ## GET CODE AIRLINE
        f = open(f'{os.getcwd()}\Transport\Airline\codeAirline.txt', "r",  encoding="utf8")
        lstCityStart  = f.readlines()
        for i in lstCityStart:
            codeStart , cityStart , _ = i.split(',')
            if cityStart == self.cityStart:
                self.codeStart = codeStart
                break
        for i in lstCityStart:
            codeEnd , cityEnd , _ = i.split(',')
            if cityEnd == self.cityEnd:
                self.codeEnd = codeEnd
                break
        
        for type in types:  
            url =  f'https://www.traveloka.com/vi-vn/flight/fullsearch?ap={self.codeStart}.{self.codeEnd}&dt={self.datePlan}.NA&ps=1.0.0&sc={type}'
            perform.crawler( url )
        self.minPrice = perform.minPrice
        self.maxPrice = perform.maxPrice





    
    
