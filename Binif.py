

import os
from PIL import Image
import tensorflow as tf
import numpy as np


Image_size = 100

dir = "../data_unprocessed"
imglab_list = []

#Get the adresses of the images using the recipes_list
with open(dir+"/"+"recipes_list.txt","r") as recettes:
    rec = recettes.readlines()[:10]####Change here for number of classes
    for i,elt in enumerate(rec):
        s = str.strip(elt)
        s = s.replace(" ", "_")
        print dir+"/"+s
        for a in os.listdir(dir+"/"+s):
            #print a
            if a[0] == "A":
                #print a
                imglab_list.append((dir+"/"+s+"/"+a,i))
                l =dir+"/"+s+"/"+a
                img = Image.open(l)
                img2 = img.resize((Image_size,Image_size),Image.ANTIALIAS)
                img2.save(dir+"/"+s+"/"+a)

out_train = []
out_test = []

#Shuffle the images.
np.random.shuffle(imglab_list)

bytes = 0
a = len(imglab_list)
print "Nombre d'images :" + str(a)

for i,elt in enumerate(imglab_list):
    if (i%100 ==0):
        print i
    if (i <= 0.7 * a):
        im = Image.open(elt[0])
        im = (np.array(im))
        r = im[:,:,0].flatten()
        g = im[:,:,1].flatten()
        b = im[:,:,2].flatten()
        #print(len(r),len(g),len(b))
        label = [elt[1]]
        out_train = np.concatenate((out_train,np.array(list(label)+list(r)+list(g)+list(b))))
        #print(len(r),len(g),len(b),len(label))
        bytes += len(r)+len(g)+len(b)+len(label)
    else:
        im = Image.open(elt[0])
        im = (np.array(im))
        r = im[:,:,0].flatten()
        g = im[:,:,1].flatten()
        b = im[:,:,2].flatten()
        label = [elt[1]]
        #print(len(r),len(g),len(b),len(label))
        bytes += len(r)+len(g)+len(b)+len(label)
        out_test = np.concatenate((out_test,np.array(list(label)+list(r)+list(g)+list(b))))

print "bytes : " + str(bytes)
print(len(out_train)+len(out_test))
out_train = np.array(out_train,np.uint8)
out_test = np.array(out_test,np.uint8)
out_train.tofile("../data_processed/train_10_classes.bin")
out_test.tofile("../data_processed/test_10_classes.bin")


