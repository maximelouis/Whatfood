

import os
from PIL import Image
import tensorflow as tf
import numpy as np

Image_size = 100
num_images = 100


out_train = []
out_test = []

img_list = []
label_list = []


#Count the number of bytes written for verification
bytes = 0



image_test = np.array([0 for elt in range(Image_size*Image_size*3)])
a = len(img_list)
label = [5]

for i in xrange(num_images):
    if (i <= 0.7 * a):
        out_train = np.concatenate((out_train,np.array(list(label)+list(image_test))))
    else:
        out_test = np.concatenate((out_test,np.array(list(label)+list(image_test))))

out_train = np.array(out_train,np.uint8)
print out_train
out_test = np.array(out_test,np.uint8)

print "bytes : " + str(bytes)
print(len(out_train)+len(out_test))
out_train.tofile("../data_processed/train_diag.bin")
out_test.tofile("../data_processed/test_diag.bin")


