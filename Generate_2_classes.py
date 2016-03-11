

import os
from PIL import Image
import tensorflow as tf
import numpy as np


Image_size = 100

dir = "../data_unprocessed"
labels = []
adresses = []

#Get the adresses of the images using the recipes_list
with open(dir+"/"+"recipes_list.txt","r") as recettes:
    rec = recettes.readlines()[:2]####Change here for number of classes
    for i,elt in enumerate(rec):
        s = str.strip(elt)
        s = s.replace(" ", "_")
        #print s
        for a in os.listdir(dir+"/"+s):
            #print a
            if a[0] == "A":
                adresses.append(dir+"/"+s+"/"+a)
                l =dir+"/"+s+"/"+a
                img = Image.open(l)
                img2 = img.resize((Image_size,Image_size),Image.ANTIALIAS)
                img2.save(dir+"/"+s+"/"+a)
                labels.append(i)

out_train = []
out_test = []

img_list = []
label_list = []

for i in xrange(len(adresses)/2):
    img_list.append(adresses[i])
    img_list.append(adresses[len(adresses)-i-1])
    label_list.append(labels[i])
    label_list.append(labels[len(adresses)-i-1])

bytes = 0

a = len(img_list)
print a
for i,elt in enumerate(img_list):
    if (i <= 0.7 * a):
        im = Image.open(elt)
        im = (np.array(im))
        r = im[:,:,0].flatten()
        g = im[:,:,1].flatten()
        b = im[:,:,2].flatten()
        #print(len(r),len(g),len(b))
        label = [label_list[i]]
        out_train = np.concatenate((out_train,np.array(list(label)+list(r)+list(g)+list(b))))
        #print(len(r),len(g),len(b),len(label))
        bytes += len(r)+len(g)+len(b)+len(label)
    else:
        im = Image.open(elt)
        im = (np.array(im))
        r = im[:,:,0].flatten()
        g = im[:,:,1].flatten()
        b = im[:,:,2].flatten()
        label = [label_list[i]]
        #print(len(r),len(g),len(b),len(label))
        bytes += len(r)+len(g)+len(b)+len(label)
        out_test = np.concatenate((out_test,np.array(list(label)+list(r)+list(g)+list(b))))

print "bytes : " + str(bytes)
print(len(out_train)+len(out_test))
out_train = np.array(out_train,np.uint8)
out_train.tofile("../data_processed/train_2_classes.bin")
out_test.tofile("../data_processed/test_2_classes.bin")


