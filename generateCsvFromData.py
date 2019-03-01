from os import listdir
from os.path import isfile, join
import json,os
import unicodecsv as csv

currentDir         = os.getcwd()+os.sep
mypath             = currentDir+'anime'
csvFilePath            = currentDir+'csvFile.csv'
    


def extractGenres(genres):
    gnames = ''
    for g in genres:
        if gnames == '':
            gnames += g["name"]
        else:
            gnames+=","+g["name"]
    return gnames

def appendToCsv(name,malId,synopsis,gnames):
    with open(csvFilePath,'ab') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([name,malId,synopsis,gnames])

            
files = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

for f in files:
    with open (f) as json_data:
         d = json.load(json_data)
    name     = d["title"]
    malId    = d["mal_id"]
    synopsis = d["synopsis"]
    genres   = d["genres"]
    gnames   = extractGenres(genres)
    print name
    appendToCsv(name,malId,synopsis,gnames)

        
    






    
