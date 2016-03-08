

import os
from PIL import Image
import tensorflow as tf
import numpy as np


dir = "../data_unprocessed"
labels = []
adresses = []

#Get the adresses of the images using the recipes_list
with open(dir+"/"+"recipes_list.txt","r") as recettes:
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


#Collect all the images in the images list
images = []
#Output strings (e.g. filenames) to a queue for an input pipeline.
data_food = tf.train.string_input_producer(adresses) #  list of files to read
reader = tf.WholeFileReader()
key, value = reader.read(data_food)


my_img = tf.image.decode_jpeg(value) # use png or jpg decoder based on your files.

init_op = tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(init_op)

# Start populating the filename queue.

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    for i in range(len(adresses)): #length of your filename list
        image = my_img.eval() #here is your image Tensor :)
        images.append(image)



coord.request_stop()
#coord.join(threads)


dir2 = "/Users/Maxime/Desktop/Whatfood/data_processed"

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

# images and labels array as input
def convert_to(images, labels, name):
    num_examples = labels.shape[0]
    if images.shape[0] != num_examples:
        raise ValueError("Images size %d does not match label size %d." %(images.shape[0], num_examples))
    rows = images.shape[1]
    cols = images.shape[2]
    depth = images.shape[3]
    filename = os.path.join(dir2, name + '.tfrecords')
    print('Writing', filename)
    writer = tf.python_io.TFRecordWriter(filename)
    for index in range(num_examples):
        image_raw = images[index].tostring()
        example = tf.train.Example(features=tf.train.Features(feature={
        'height': _int64_feature(rows),
        'width': _int64_feature(cols),
        'depth': _int64_feature(depth),
        'label': _int64_feature(int(labels[index])),
        'image_raw': _bytes_feature(image_raw)}))
        writer.write(example.SerializeToString())

#Convert to numpy arrays
images = np.array(images)
labels = np.array(labels)
#Convert the images and labels to a tf_record.
convert_to(images,labels,"data")
