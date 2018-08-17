from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import unicodecsv as csv
import re
import shutil
import os

csvFile = r'tweets.csv'
 
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

#construct the handler and set the access token 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

 
#api = tweepy.API(auth)

#Listener class that defines what to do when a tweet is found
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            #with open('python.json', 'a') as f:
            #    f.write(data)
            #    print "Collected a tweet"
            #print "Tweet Coletado"
            tweet = json.loads(data)
            if tweet['lang'] == 'pt':
                print "Tweet em portugues!!!"
                try:
                    id_original = tweet['retweeted_status']['id_str']
                    count_original = tweet['retweeted_status']['retweet_count']
                    if tweet['retweeted_status']['truncated']:
                        tweet_text = self.processTweet(tweet['retweeted_status']['extended_tweet']['full_text'])
                    else:
                        tweet_text = self.processTweet(tweet['retweeted_status']['text'])
                    self.incrementOnCsv(id_original,count_original,tweet_text)
                except KeyError:
                    text = tweet['text']
                    tweet_id = tweet['id']
                    tweet_text = self.processTweet(text)
                    if self.isRetweet(text):
                        try:
                            self.incrementOnCsv(tweet_id,0,tweet_text,True)
                        except:
                            self.addToCsv(tweet_id,0,tweet_text)
                    else:        
                        self.addToCsv(tweet_id,0,tweet_text)
                
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

    def addToCsv(self,tweet_id,count,text): 
        fields=[tweet_id,text.encode('utf-8'),str(count)]
        print fields
        with open(csvFile, 'ab') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

    def incrementOnCsv(self,tweet_id,count,text,retweet = False):
        if retweet:
            try:
                line, line_number = self.findTweetTextOnCsv(text)
                line[2] = str(int(line[2]) + 1)
                self.updateCsv(line_number,line)
            except:
               self.addToCsv(tweet_id,count,text) 
        else:
            try:
                line, line_number = self.findTweetOnCsv(tweet_id)
                if int(line[2]) < count:
                    line[2] = str(count)
                    self.updateCsv(line_number,line)
            except:
                self.addToCsv(tweet_id,count,text)

    def findTweetTextOnCsv(self,text):
        with open('tweets.csv', 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for i,row in enumerate(reader):
                if text in row[1] or text == row[1] :
                    line = row
                    lineNumber = i
                    return (line, lineNumber)
                    
        return ()

    def findTweetOnCsv(self, tweet_id):
        with open('tweets.csv', 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for i,row in enumerate(reader):
                if tweet_id == row[0]:
                    line = row
                    lineNumber = i
                    return (line, lineNumber)
                    
        return ()

    def updateCsv(self, line_number,line):
        print line
        tempfile = 'tmptweet.csv'
        with open(csvFile, 'rb') as f:
            with open (tempfile, 'wb') as ftemp:
                reader = csv.reader(f, delimiter=',')
                writer = csv.writer(ftemp, delimiter=',')

                for i,row in enumerate(reader):
                    if i == line_number:
                        writer.writerow(line)
                    else:
                        writer.writerow(row)
        os.remove(csvFile)
        shutil.move(tempfile, csvFile)

    def isRetweet(self,text):
        if text.startswith('RT'):
            return True

    def processTweet(self,tweet_text):
        tokens = tweet_text.split(" ")
        for i,token in enumerate(tokens):
            if token.startswith('http'):
                tokens[i] = 'HTTPLINK'
            if token.startswith('@'):
                tokens[i] = '@USERNAME'
        if 'RT' in tokens:
            tokens.remove('RT')
        return " ".join(tokens)

    
class CollectionAnalizer():
    collection = []
    def restrictLanguage(self, language):
        total = 0
        found = 0
        with open('python.json', 'r') as f:
            for line in f:
                tweet = json.loads(line)
                total += 1
                try:
                    if tweet['lang'] == language:
                        print tweet['text']
                        self.collection.append(tweet['text'])
                        found += 1
                except:
                    pass
        print total
        print found

    def writeCollectionToFile(self):
        with open('LanguageRestrictedTweets.txt','w') as f:
            for tweet in self.collection:
                f.write((tweet+"\n").encode('utf-8'))


class Tokenizer(): 
    emoticons_str = ur"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""
     
    regex_str = [
        emoticons_str,
        u'<[^>]+>', # HTML tags
        u'(?:@[\w_]+)', # @-mentions
        u"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        u'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
     
        u'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        u"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        u'(?:[\w_]+)', # other words
        u'(?:\S)' # anything else
    ]
        
    tokens_re = re.compile(ur'('+'|'.join(regex_str)+')',re.U | re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(ur'^'+emoticons_str+'$',re.U | re.VERBOSE | re.IGNORECASE)
     
    def tokenize(self, s):
        return self.tokens_re.findall(s)
     
    def preprocess(self, s, lowercase=False):
        tokens = self.tokenize(s)
        if lowercase:
            tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['bullied, buly, bullying, bulin, buli, bullin, bulen, bullen, bulli'])
#analizer = CollectionAnalizer()
#analizer.restrictLanguage("pt")
#analizer.writeCollectionToFile()
