from selenium import webdriver
import urllib.request
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from unidecode import unidecode

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

class ActivityCrawler:
    def __init__(self):
        self.options = Options()
        #self.options.add_argument("--headless")
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
        self.driver  = None

        self.saveColumn = [ 'id' ,  'nameActivity' , 'rateActivity' , 'numComment' ,  'priceActivity' , 'urlImage' , 'city' , 'time' , 'distance', 'typeActivity'  ]
        self.df = pd.DataFrame(columns=self.saveColumn)

    def crawler( self  , citySearch , cityAddress):
        url = f'https://www.google.com/search?q=hoạt+động+du+lịch+nổi+tiếng+ở+{citySearch}&sca_esv=e54de6d9ee195691&sca_upv=1&sxsrf=ADLYWILOiBdczc8M99ss6wLYczpaWBI6Cg:1715720757630&udm=15&sa=X&ved=2ahUKEwivh6vyhY6GAxVhfGwGHZGXApcQxN8JegQIEBAb&biw=1280&bih=559&dpr=1.5'
        print(url)
        
        self.driver = webdriver.Chrome(self.options)
        self.driver.get(url)
        actions = ActionChains(self.driver)
        sleep(5)

        buttonFirst = self.driver.find_element(By.XPATH , '//*[@id="Rzn5id"]/div/a[3]').click()
        try :
            elementXemThem = self.driver.find_elements(By.CSS_SELECTOR , "span.PBBEhf")
        except:
            elementXemThem = None

        while True :
            count = 0
            for i in elementXemThem:
                if i.text == 'Điểm tham quan khác':
                    i.click()
                    count +=1
                    sleep(7)
            if count == 0:
                break
            elementXemThem = self.driver.find_elements(By.CSS_SELECTOR , "span.PBBEhf")
 
        lstNameActivity = []  
        lstName = self.driver.find_elements(By.CSS_SELECTOR , 'span.Yt787')
        for i in lstName:
            lstNameActivity.append(i.text)

        lstRateActivity  = [] 
        lstNumComment    = [] 
        lstTypeActivity  = []
        lstPriceActivity = []

        lstData = self.driver.find_elements(By.CSS_SELECTOR, 'div.e1H2sd.N8D9gb.OdBhM.GUHazd')

        for i  in lstData:
            ## GET VALUE 
            getRate = ''
            getNumComment = ''
            getType = ''
            getPrice = ''

            ## GET RATE ACTIVITY
            try:
                getRate = i.find_element(By.CSS_SELECTOR , 'span.yi40Hd.YrbPuc').text
            except:
                pass
    
            ## GET NUMBER COMMENT ACTIVITY
            try:
                getNumComment = i.find_element(By.CSS_SELECTOR , 'span.RDApEe.YrbPuc').text
                getNumComment = getNumComment.strip('() ')
                getNumComment = getNumComment.replace(',' , '.')
                if 'N' in getNumComment:
                    getNumComment = getNumComment.replace('N' , '').strip()
                    getNumComment = float(getNumComment) * 1000
                    getNumComment = int(getNumComment)

            except:
                pass
        
            ## GET TYPE ACTIVITY
            try: 
                getType  = i.find_element(By.CSS_SELECTOR, 'div.ZJjBBf.cyspcb.DH9lqb').text 
               
            except:
                pass

            ## GET PRICE ACTIVITY
            try:
                getPrice = i.find_element(By.CSS_SELECTOR , 'div.rDUZLd.JNI6Yb').text
                getPrice  = getPrice.replace('₫', '').strip()
                getPrice  = getPrice.replace('.', '')

            except:
                pass

            ## Save to LIST 
            lstRateActivity.append(getRate)
            lstNumComment.append(getNumComment)
            lstTypeActivity.append(getType)
            lstPriceActivity.append(getPrice)

        ## GET IMAGE 
        lstURLImage = []
        lstImage = self.driver.find_elements( By.CSS_SELECTOR , 'div.gdOPf.uhHOwf.ez24Df')
        for i in lstImage:
            getURLImage = i.find_element(By.CSS_SELECTOR , 'img')
            link = getURLImage.get_attribute('src')
            lstURLImage.append(link)

        lstDetail   = []
        lstTime     = []
        lstDistance = []
        lstLink =  self.driver.find_elements(By.CSS_SELECTOR , 'a.ddkIM.c30Ztd')
        for i in lstLink:
            link = i.get_attribute('href')
            lstDetail.append(link)
    
        
        for url in lstDetail:
            self.driver.get(url)
            sleep(2)
            ## GET TIME
            getTime = ''
            try:
                getTime = self.driver.find_element(By.CSS_SELECTOR , 'span.JjSWRd').click()
                getTime = self.driver.find_element(By.CSS_SELECTOR , 'tr.K7Ltle').text
        
            except:
                pass

            ## GET Tọa độ
            getLatitude = 0
            getLongitude = 0
            try:

                getDistance = self.driver.find_elements( By.CSS_SELECTOR , 'span.PbOY2e' )
                for i in getDistance:
                    if i.text == 'Đường đi':
                        i.click()
                        sleep(8)

                        getAdd = self.driver.find_elements(By.CSS_SELECTOR , 'div.twHv4e')
                        url = str(self.driver.current_url)
                        *rest,getAdd = url.split('@')
                        getAdd,*rest = getAdd.split('/')
                        getLatitude,getLongitude,*rest = getAdd.split(',')
                        break
            except:
                pass
                
            lstTime.append(getTime)
            lstDistance.append( (getLatitude,getLongitude) )
        
        self.driver.quit()
       
        ## SAVE data
        ## 
        for i in range(len(lstNameActivity)):
            self.df.loc[len(self.df)] = [ len(self.df)  , lstNameActivity[i] , lstRateActivity[i] , lstNumComment[i] ,  lstPriceActivity[i] , lstURLImage[i] , cityAddress , lstTime[i] , lstDistance[i]  ,  lstTypeActivity[i] ]

if __name__ == '__main__':
    perform = ActivityCrawler()

    f = open("codeActivity.txt", "r",  encoding="utf8")
    lstCity = f.readlines()
    for i in lstCity:
        citySearch , cityAddress  = i.split(',')
        perform.crawler(citySearch , cityAddress.strip())
    perform.df.to_csv('activityRawData.csv', index=False)



