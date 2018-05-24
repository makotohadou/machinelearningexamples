import os,sys,time,csv
import pandas
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


##############     VARIABLES    #################

ftURL = 'https://markets.ft.com/data/funds/uk'
lseURL = 'http://www.londonstockexchange.com/exchange/searchengine/search.html?lang=en&x=0&y=0&q='
timeout = 10
targetFile = 'large One.csv'
temp = 'temp.csv'


##############       VALUES     #################
FTrow  = 5
LSErow = 6



data = pandas.read_csv(targetFile,encoding='utf-8')


#main class
class Scraper:
    
    def __init__(self):
        self.OS = sys.platform

    def initiate(self):
        try:
            self.driver = self.buildDriver()
            time.sleep(1)
        except Exception as e:
            print str(e)
            time.sleep(4)
            try:
                self.driver.quit()
            except Exception as e:
                print str(e)
                print "Unable to close the driver. Please close it manually"
                return

    def checkFT(self,ISIN):

        self.driver.get(ftURL)
        
        searchInput = self.findElement((By.XPATH,"//section[@class='mod-funds-browse-app__form--search']/form/div[@class='o-forms-affix-wrapper']/input[@class='o-forms-text']"))
        confirmButton = self.findElement((By.XPATH,"//form/div[@class='o-forms-affix-wrapper']/div[@class='o-forms-suffix']/button[@class='o-buttons']"))
        
        searchInput.clear()
        searchInput.send_keys(ISIN)

        print "ISIN sent"

        confirmButton.click()


        try:
            resultLink = self.findElement((By.XPATH,"//td[@class='mod-ui-table__cell--text'][1]/a[@class='mod-ui-link']"))
            resultLink.click()

            tblISIN = self.findElement((By.XPATH,"//div[@class='mod-tearsheet-overview__header__symbol']/span"))
            print tblISIN.text,ISIN
            if tblISIN.text[:-4] == ISIN:
                return True

        except Exception as e:
            print e
            return False
        return False

    def checkLSE(self,ISIN):

        self.driver.get(lseURL+ISIN)
        try:
            resultLink = self.findElement((By.XPATH,"//td[@class='name'][2]/a"))
            resultLink.click()

            tblISIN = self.findElement((By.XPATH,"//div[@id='csDetail']/table[@class='table_dati']/tbody/tr[@class='odd'][1]/td[@class='name'][2]"))
            print tblISIN.text,ISIN
            if tblISIN.text == ISIN:
                return True

        except Exception as e:
            print e
            return False
        return False


    def findElement(self,locator):
        return WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located(locator))

    def finalize(self):
        self.driver.quit()


    def buildDriver(self):
        #This function builds the driver (phantomJS)
        number = 0
        while True:
            try:
                driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true','--ssl-protocol=any'],service_log_path=os.path.devnull)
                driver.set_window_size(1120,800)
                driver.implicitly_wait(30)
                driver.get(ftURL)
                break
            except Exception as e:
                number += 1
                if number > 5:
                    print(str(e)+ " ...retrying...")
                    time.sleep(random.uniform(1.9,3.8))
                    print(e)
        return driver


def alterFile(field, value, ISIN):
    with open(temp,"wb") as tempCsv:
        writer = csv.writer(tempCsv)
        with open(targetFile, 'rb') as csvFile:
            fileContents = csv.reader(csvFile)
            for row in fileContents: 
                if row[3] == ISIN: 
                    row[field] = str(value)
                writer.writerow(row)
    os.remove(targetFile)
    os.rename(temp,targetFile)
    print "Altered Fund "+ISIN+" to "+str(value)


def checkforFT():
    scraper = Scraper()
    scraper.initiate()
    for row in data.itertuples():
        if pandas.isna(row[FTrow]):
        #if row[FTrow] == False:
            alterFile((FTrow - 1),scraper.checkFT(row[4]), row[4])
    scraper.finalize()


def checkforLSE():
    scraper = Scraper()
    scraper.initiate()
    for row in data.itertuples():
        if row[FTrow] == False and pandas.isna(row[LSErow]):
            alterFile((LSErow - 1),scraper.checkLSE(row[4]), row[4])
    scraper.finalize()


checkforLSE()
