import os, sys
import glob
import cv2
import numpy as np
import random
from read_info import *

'''
if __name__ != "__main__":
    print "please don't import this module"
    exit(-1)
'''

def read_data(option=0):
    image_dir = "Data/img/"
    label_dir = "Data/current/"
    type_dir = "Data/type.json"
    attr_dir = "Data/tag.json"

    image_arr_dir = "Data/image_arr.json"
    image_label_dir = "Data/image_label.json"
    image_type_dir = "Data/image_type.json"
    image_attribute_dir = "Data/image_attribute.json"
    dir_arr = [image_arr_dir, image_label_dir, image_type_dir, image_attribute_dir]
    data_arr = range(4)
    if option == 0: # read in from file and generate
        image_arr, image_label = read_in_label(image_dir=image_dir, label_dir=label_dir)
        image_type, image_attribute = read_in_attribute(type_dir=type_dir, attr_dir=attr_dir)

        # reconstruct json file
        image_type = {each.values()[0]: each for each in image_type}
        image_attribute = {each.values()[0]: each for each in image_attribute}

        # Make sure that every img_id appears in three dict
        avaliable_set = set(image_label.keys()) & \
                        set(image_type.keys()) & \
                        set(image_attribute.keys())
        image_arr = [img_id for img_id in image_arr if img_id in avaliable_set]

        data_arr = [image_arr, image_label, image_type, image_attribute]

        for i in xrange(4):
            with open(dir_arr[i], 'w+') as fp:
                json.dump(data_arr[i], fp, indent=4)
        return tuple(data_arr)
    else:
        for i in xrange(4):
            with open(dir_arr[i], 'r+') as fp:
                data_arr[i] = json.load(fp)
        return tuple(data_arr)

def combine_attribute():
    pass

if __name__ == "__main__":
    image_arr, image_joint, image_type, image_attribute = read_data(option=1)