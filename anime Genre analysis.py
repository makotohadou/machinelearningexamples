import pandas,os

currentDir         = os.getcwd()+os.sep
animeDatabase      = currentDir + "animeDatabase.csv"

data = pandas.read_csv(animeDatabase,encoding='utf-8')
genres = data['Genres']


classifying_genres = ["Hentai", "Comedy", "Music", "Kids", "Dementia", "Action", "Fantasy", "Adventure", "Drama", "Sci-Fi",
                      "Shounen", "Romance", "School", "Supernatural", "Slice of Life"]
descriptive_genres = ["Parody", "Space", "Samurai", "Martial Arts", "Military", "Super Power", "Mecha", "Yuri", "Ecchi",
                      "Yaoi", "Historical", "Magic", "Shoujo", "Mystery", "Seinen", "Sports", "Harem", "Horror", "Psychological",
                      "Demons", "Game", "Police", "Thriller", "Vampire", "Josei", "Cars", "Shounen Ai", "Shoujo Ai"]


#classifying_genres.extend(descriptive_genres)
#print len(classifying_genres)
#print set([x for x in classifying_genres if classifying_genres.count(x) > 1])
#quit()

combDict = {}
genresDict = {}
uniqueDict = {}


def combine(inputList):
    returnList = []
    for i in range(0,len(inputList)):
        for j in range(i+1,len(inputList)):
            returnList.append(inputList[i]+" -> "+inputList[j])
    return returnList

def getMinGenres(combination):
    first, second = combination.split(" -> ")
    return min(genresDict[first],genresDict[second])

def mergeDuplicated(d):
    for key in d.keys():
        reversedKey = " -> ".join((key.split(" -> ")[::-1]))
        if reversedKey in d and key in d:
            d[key] = d[key]+d[reversedKey]
            d.pop(reversedKey)
    return d



for row in genres:
    instances = row.split(',')
    for instance in instances:
        if instance.lstrip() in genresDict:
            genresDict[instance.lstrip()] = genresDict[instance.lstrip()]+1
        else:
            genresDict[instance.lstrip()] = 1

for w in sorted(genresDict, key=genresDict.get, reverse=True):
    print w, genresDict[w]

print "\n\nNumber of genres = "+str(len(genresDict))            
print "Average of genres per title = "+str(float(sum(genresDict.values()))/len(genres))


combDict = {}
combinationList = []
for row in genres:
    instances = row.split(',')
    instances = [instance.lstrip() for instance in instances]
    combinationList.extend(combine(instances))

for inst in combinationList:
    if inst in combDict:
        combDict[inst] = combDict[inst]+1
    else:
        combDict[inst] = 1
print "\n\n\n\n----------------------------------------------------------------------------------------------\n\n\n\n\n"
for w in sorted(combDict, key=combDict.get, reverse=True):
    print w, combDict[w]
    


combDict = mergeDuplicated(combDict)
makotoValueDict = {}
for key in combDict:
    makotoValueDict[key] = float(combDict[key])/float(getMinGenres(key))

print "\n\n\n\n----------------------------------------------------------------------------------------------\n\n\n\n\n"
for w in sorted(makotoValueDict, key=makotoValueDict.get, reverse=True):
    print w, makotoValueDict[w]



for row in genres:
    instances = row.split(',')
    if len(instances) == 1:
        instance = instances[0].lstrip()
        if instance in uniqueDict:
            uniqueDict[instance] = uniqueDict[instance]+1
        else:
            uniqueDict[instance] = 1

print "\n\n\n\n----------------------------------------------------------------------------------------------\n\n\n\n\n"
for w in sorted(uniqueDict, key=uniqueDict.get, reverse=True):
    print w, uniqueDict[w]

