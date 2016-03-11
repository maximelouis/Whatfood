

import os
from PIL import Image
import tensorflow as tf
import numpy as np


Image_size = 100

dir = "../data_unprocessed"
labels = []
adresses = []

#Get the adresses of the images using the recipes_list
with open("recipes_list.txt","r") as recettes:
    rec = recettes.readlines()[:20]
    for i,elt in enumerate(rec):
        s = str.strip(elt)
        s = s.replace(" ", "_")
        for a in os.listdir(dir+"/"+s):
            if a[0] == "A":
                adresses.append(dir+"/"+s+"/"+a)
                l =dir+"/"+s+"/"+a
                img = Image.open(l)
                img2 = img.resize((Image_size,Image_size),Image.ANTIALIAS)
                img2.save(dir+"/"+s+"/"+a)
                labels.append(i)

out = []

print len(labels)
for i,elt in enumerate(adresses):
    im = Image.open(elt)
    im = (np.array(im))
    r = im[:,:,0].flatten()
    g = im[:,:,1].flatten()
    b = im[:,:,2].flatten()
    label = [labels[i]]
    out = np.concatenate((out,np.array(list(label)+list(r)+list(g)+list(b))))
#print out

out = np.array(out,np.uint8)
out.tofile("../data_processed/train_set.bin")

