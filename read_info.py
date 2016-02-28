import os, sys
import glob
import cv2
import numpy as np
import random, json


def read_in_label(image_dir="Data/img/", \
                  label_dir="Data/current/"):
    jpg_arr = [each.split('.')[0] for each in (glob.glob1(image_dir, "*.jpg"))]
    txt_arr = [each.split('.')[0] for each in (glob.glob1(label_dir, "*.json"))]

    txt_arr = [each for each in txt_arr if each in jpg_arr]
    jpg_arr = [each for each in jpg_arr if each in txt_arr]

    image_label = {}
    for each in txt_arr:
        with open(os.path.join(label_dir, each + '.json'), 'r+') as fp:
            temp = json.load(fp)
        image_label[each] = temp

    return jpg_arr, image_label


def read_in_attribute(type_dir="Data/type.json", \
                      attr_dir="Data/tag.json"):
    with open(type_dir, 'r+') as fp:
        image_type = json.load(fp)

    with open(attr_dir, 'r+') as fp:
        image_attribute = json.load(fp)
    return image_type, image_attribute


if __name__ == "__main__":
    read_in_attribute()
