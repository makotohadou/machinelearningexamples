#This simple spider will revolution the world
import os,random,sys,time,unicodecsv as csv
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas
#from bs4 import BeautifulSoup


url = u"https://myanimelist.net"
timeout = 10


currentDir         = os.getcwd()+os.sep
animeDatabase      = currentDir + "animeDatabase.csv"
csvHeader = ["Id","Name","Genres","N of Episodes"]
animeLinkExample = "https://myanimelist.net/anime/"

class Spider:
    #main class that do all the heavy work
    def __init__(self,url):
        self.url = url
        self.OS = sys.platform
    def initiate(self):
        try:
            scraper_object = scraper(self.url)
            self.driver = scraper_object.scrap()
            self.links = self.driver.find_elements_by_tag_name("a")
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

    def findAnimeLinkNotOnDatabase(self):
        try:
            self.navigateToRandomAnimeLink()
            link,animeId = self.findAnimeLink(self.links)
            if not self.animeIdAlreadyOnDataBase(animeId):
                return link
            else:
                print link+" already on database, retrying"
                self.navigateToRandomAnimeLink()
                return self.findAnimeLinkNotOnDatabase()
        except Exception as e:
            print str(e)
            print "Could not find anime link not on database"
            self.navigateToRandomAnimeLink()
            return self.findAnimeLinkNotOnDatabase()

    def navigateToLink(self,link):
        try:
            self.driver.get(link)
            self.links = self.driver.find_elements_by_tag_name("a")
        except Exception as e:
            print str(e)
            print "Could not navigate to link: "+link

    def navigateToRandomAnimeLink(self):
        try:
            link = animeLinkExample+str(random.randint(0,35000))
            self.driver.get(link)
            self.links = self.driver.find_elements_by_tag_name("a")
        except Exception as e:
            print str(e)
            print "Could not navigate to link: "+link

    def collectAnimeData(self):
        try:
            print (self.driver.current_url)
            animeId = self.getAnimeId(self.driver.current_url)
            animeName     = self.findElement((By.XPATH,"//*[@id='contentWrapper']/div[1]/h1[@class='h1']/span")).text
            genres        = self.findElement((By.XPATH,"//*[contains(text(), 'Genres:')]/..")).text
            numberOfEpis = self.findElement((By.XPATH,"//*[@class='js-scrollfix-bottom']/div[@class='spaceit'][1]")).text


            data = [animeId,animeName, genres[8:], numberOfEpis[10:]]
            print data
            self.insertAnimeDataOnCsv(data)
        except Exception as e:
            print str(e)
            print "Could not collect anime data"



    def findAnimeLink(self,links):
        linksOfInterest = [link.get_attribute("href") for link in links if link.get_attribute("href") and
                           animeLinkExample in link.get_attribute("href") and len(link.get_attribute("href").split("/")) == 6]
        randomPosition = random.randint(0, len(linksOfInterest))
        randomLink = linksOfInterest[randomPosition]
        return (randomLink,self.getAnimeId(randomLink))


    def getAnimeId(self,link):
        try:
            return link.split("/")[4]
        except Exception as e:
            print str(e)
            print "Could not get anime ID"


    def animeIdAlreadyOnDataBase(self,animeId):
        if not os.path.exists(animeDatabase):
            return False
        data = pandas.read_csv(animeDatabase,encoding='utf-8')
        ids = data["Id"]
        return any(ids == int(animeId))


    def insertAnimeDataOnCsv(self,data):
        if not os.path.exists(animeDatabase):
            with open(animeDatabase,"ab") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(csvHeader)
        with open(animeDatabase,"ab") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def findElement(self,locator):
        return WebDriverWait(self.driver,timeout).until(EC.presence_of_element_located(locator))

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


def scrapeForAnimes(limit):
    try:
        count = 0
        spider = Spider(url)
        spider.initiate()
        while count < limit:
            link = spider.findAnimeLinkNotOnDatabase()
            spider.navigateToLink(link)
            spider.collectAnimeData()
            count+=1
        spider.driver.quit()
    except Exception as e:
        print str(e)
        print "Could not scrape for new animes"
        spider.driver.quit()


scrapeForAnimes(100)
