

import os
from PIL import Image
import tensorflow as tf
import numpy as np



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



image_test = [elt % 256 for elt in range(32*32*3)]
image_test = np.array(image_test)
a = len(img_list)
print a
for i,elt in enumerate(img_list):
    if (i <= 0.7 * a):
        label = [1]
        out_train = np.concatenate((out_train,np.array(list(label)+list(image_test),np.uint8)))
    else:
        im = Image.open(elt)
        im = (np.array(im))
        label = [1]
        out_test = np.concatenate((out_test,np.array(list(label)+list(image_test),np.uint8)))
test = [out_train[i] for i in xrange(len(out_train)) if i % (32*32*3+1)  == 0 ]




print "bytes : " + str(bytes)
print(len(out_train)+len(out_test))
out_train.tofile("../data_processed/train_diag.gz")
out_test.tofile("../test_diag.gz")


