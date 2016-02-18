import os, sys, glob
import random
import shutil

image_dir = "Data/img/"
label_dir = "Data/tmp/"
des_dir = "Data/split/"


if not os.path.isdir(image_dir) or not os.path.isdir(label_dir):
    print ("image dir or label dir doesn't exist")
    exit(-1)


file_list = glob.glob1(image_dir,"*.jpg")
random.shuffle(file_list)

for i in xrange(len(file_list)):
    id = file_list[i]
    group = i / 200
    src_dir = os.path.join(image_dir, id)
    group_dir = os.path.join(des_dir, "data_set_" + str(group))
    aim_dir = os.path.join(group_dir, id)

    if not os.path.exists(group_dir):
        os.makedirs(group_dir)

    shutil.copyfile(src_dir, aim_dir)
