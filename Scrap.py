# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os

import time

l = []

fichier = open("recipes_list.txt", "r")



for elt in fichier.readlines():
    l.append(elt)





def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)))

for elt in l[:20]:
    s = str.strip(elt.replace(" ","_"))
    image_type = "Action"
    # you can change the query for the image  here
    query = elt
    print query
    query= query.split()
    query='+'.join(query)
    for nb in xrange(10):
        start = nb * 20
        url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch&start=" + str(start)
        header = {'User-Agent': 'Mozilla/1.0'}
        soup = get_soup(url,header)
        #print soup
        s1 = soup.find_all("img", {"src":re.compile("gstatic.com")})
        images = [a['src'] for a in s1]
        print(len(images))
        for img in images:
        #print img
            raw_img = urllib2.urlopen(img).read()
        #add the directory for your image here
            DIR="../data_unprocessed/" + s + "/"
            if not os.path.exists(DIR):
                os.makedirs(DIR)
            cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
            #print DIR + image_type + "_"+ str(cntr)+".jpg"
            f = open(DIR + image_type + "_"+ str(cntr)+".jpg", 'wb')
            f.write(raw_img)
f.close()
