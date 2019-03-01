from jikanpy import Jikan
import json,time,os
folder = os.getcwd()+'/anime/'

jikan = Jikan()

for a in range(33817,40000):
    time.sleep(3)
    try:
        anime = jikan.anime(a)
        print ('Saving id '+ str(a))
        path = folder+'anime'+str(a)+'.json'
        print (path)
        with open(path, 'w') as outfile:
            json.dump(anime, outfile)
    except Exception as e:
        print ('Id '+str(a)+' does no exists')


