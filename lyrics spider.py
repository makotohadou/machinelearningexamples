#This simple spider will revolution the world
import os,random,sys,time,unicodecsv as csv
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas
import re


currentDir         = os.getcwd()+os.sep
animeDatabase      = currentDir + "animeDatabase with LYRICS in ROMAJI.csv"
temp               = currentDir+'/temp.csv'
csvHeader          = ["Id","Name","Genres","N of Episodes","opening"]
myAnimeListLink    = "https://myanimelist.net/anime/"
lyricsSite         = "https://www.letras.mus.br/"
timeout            = 10


data = pandas.read_csv(animeDatabase,encoding='utf-8')


def lookForLyrics(animeId):
    driver.get(myAnimeListLink+str(animeId))
    print (driver.current_url)
    openingName = findElement((By.XPATH,"//*/div[@class='theme-songs js-theme-songs opnening']/span[@class='theme-song'][1]"),driver).text
    openingName = fixOpeningName(openingName)

    if openingName == "None":
        return None
    driver.get(lyricsSite)
    print (driver.current_url)
    box = findElement((By.XPATH,"//*/input[@id='main_suggest']"),driver)
    box.clear()
    box.send_keys(openingName)
    try:
        searchButton = findElement((By.XPATH,"//*/button[@class='main-search_submit']"),driver)
        searchButton.click()
        print (driver.current_url)
        linkToLyrics = findElement((By.XPATH,"//*//*/div[@class='gsc-results gsc-webResult']/div[@class='gsc-webResult gsc-result']/div[@class='gs-webResult gs-result']/table[@class='gsc-table-result']/tbody/tr/td[@class='gsc-table-cell-snippet-close']/div[@class='gsc-url-bottom']/div[@class='gs-bidi-start-align gs-visibleUrl gs-visibleUrl-long']"),driver)
        print linkToLyrics.text
        driver.get(linkToLyrics.text)
        lyrics = findElement((By.XPATH,"//*/div[@class='cnt-trad g-fix']/div[@class='cnt-trad_l']"),driver)
        return lyrics.text
    except Exception as e:
        print str(e)
        try:
            lyrics = findElement((By.XPATH,"//*/div[@class='cnt-letra p402_premium']/article"),driver)
            return lyrics.text
        except Exception as e:
            print str(e)
            return None
     
    
def fixOpeningName(openingName):
    
    print openingName
    if openingName.startswith("#1: "):
        returnStr=openingName[4:]
    else:
        returnStr = openingName
    occ = returnStr.find("(ep")
    if not occ == -1:
        returnStr = returnStr[:occ]
    returnStr = re.sub(r'[^\w]', ' ', returnStr)    
    #returnStr = returnStr.encode("ascii", errors="ignore").decode()
    print returnStr
    return returnStr
    


def addLyricsToFile(animeId, lyrics):
    with open(temp,"wb") as tempCsv:
        writer = csv.writer(tempCsv)
        with open(animeDatabase, 'rb') as csvFile:
            fileContents = csv.reader(csvFile)
            for row in fileContents:
                if str(animeId) == str(row[0]): 
                    row[4] = lyrics
                writer.writerow(row)
    os.remove(animeDatabase)
    os.rename(temp,animeDatabase)
    print "added lyrics to "+str(animeId)

def findElement(locator,driver):
    return WebDriverWait(driver,timeout).until(EC.presence_of_element_located(locator))

    
class scraper:
    #scrapper class
    def __init__(self,url):
        self.url = url
    def scrap(self):
        #This function builds the driver (phantomJS)
        number = 0
        while True:
            try:
                driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true','--ssl-protocol=TLSv1'],service_log_path=os.path.devnull)
                #driver = webdriver.Firefox()
                driver.set_window_size(1120,800)
                driver.implicitly_wait(30)
                driver.get(self.url)
                #time.sleep(random.uniform(4.5,8.97))
                break
            except Exception as e:
                number += 1
                if number > 5:
                    print(str(e)+ " ...retrying...")
                    time.sleep(random.uniform(1.9,3.8))
                    print(e)
        return driver

    def soup(self):
        #this function builds the soup object
        self.driver = self.scrap()
        soup = BeautifulSoup(self.driver.page_source)
        return soup



def cleanLyrics():
    with open(temp,"wb") as tempCsv:
        writer = csv.writer(tempCsv)
        with open(animeDatabase, 'rb') as csvFile:
            fileContents = csv.reader(csvFile)
            for row in fileContents: 
                row[4] = row[4].replace('\n',' ').replace('\r',' ')
                writer.writerow(row)
    os.remove(animeDatabase)
    os.rename(temp,animeDatabase)

scraper_object = scraper(myAnimeListLink)
driver = scraper_object.scrap()
i = 1
for row in data.itertuples():
    #set how much tries do you want
    if i > 50:
        driver.quit()
        break
    if not row[5] or row[5] == 'not found':
        print i
        i+=1
        try:
            lyrics = lookForLyrics(row[1])
            if lyrics:
                addLyricsToFile(row[1],lyrics)
        except:
            addLyricsToFile(row[1],"not applicable")
driver.quit()
cleanLyrics()
