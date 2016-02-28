import os, sys
import glob
import cv2
import numpy as np
import random
from read_tool_box import *
from draw_img import *
import operator

'''
if __name__ != "__main__":
    print "please don't import this module"
    exit(-1)
'''

output_dir = "Data/output/"


def count_attribute(image_arr, image_type, image_attribute, option=0):
    attr_count = {}
    ignore_list = ['Sales_Volume', "ID_image", "URL_image", "Comments"]
    ignore_list = [each.lower() for each in ignore_list]
    if option == 0:
        for each in image_arr[:]:
            attr = image_attribute[each]
            attr.update(image_type[each])
            # Count appearance
            for k in attr.keys():
                if k.lower() in ignore_list:
                    continue
                try:
                    attr_count[k]
                except KeyError:
                    attr_count[k] = {}
                try:
                    attr_count[k][str(attr[k])]
                except KeyError:
                    attr_count[k][str(attr[k])] = 0
                attr_count[k][str(attr[k])] += 1
        '''
        with open('Data/ans.json', 'w+') as fp:
            json.dump(attr_count, fp, indent=4)
        '''
    else:
        with open('Data/ans.json', 'r+') as fp:
            attr_count = json.dump(fp)
    return attr_count


def combine_attribute(image_arr, image_type, image_attribute):
    ans = {}
    attr_count = count_attribute(image_arr, image_type, image_attribute)

    for each in image_arr[:]:
        attr = image_attribute[each]
        attr.update(image_type[each])
        cur = {}

        # Merge attributes
        # print attr["Placket1"]
        # print attr["Placket2"]
        # print

        type_list = ['placket', 'sleeve_type', 'collar_type', 'button_type', 'cloth_type']
        key_list = ['Placket1', 'SleeveLength', 'CollarType', 'ButtonType', 'Cloth_Type']

        # Todo
        # don't forget some special case
        for i in xrange(len(type_list)):
            cur[type_list[i]] = {each: False for each in attr_count[key_list[i]]}
            cur['None'] = False
            cur[type_list[i]][attr[key_list[i]]] = True

        '''
        # print attr
        cur['sleeve_type'] = {each: False for each in attr_count["SleeveLength"]}
        cur['sleeve_type'][attr['SleeveLength']] = True
        # print cur['sleeve_type']

        # print attr["CollarType"]
        cur['collar_type'] = {each: False for each in attr_count["CollarType"]}
        cur['collar_type'][attr['CollarType']] = True

        cur['button_type'] = {each: False for each in attr_count["ButtonType"]}
        cur['button_type'][attr['ButtonType']] = True
        # print cur['button_type']
        # attr["ButtonType"]

        cur['cloth_type'] = {each: False for each in attr_count["Cloth_Type"]}
        cur['cloth_type'][attr['Cloth_Type']] = True
        '''
        ans[each] = cur

    return ans


def find_bouding_box(img, joints):
    x_min, y_min = 30000, 30000
    x_max, y_max = 0, 0

    for part in joints:
        if part in ['img_id', 'id']:
            continue

        pt = [each['position'] for each in joints[part]]
        pt_x = [each['position'][0] for each in joints[part] if each['visible']]
        pt_y = [each['position'][1] for each in joints[part] if each['visible']]
        if len(pt_x) > 0:
            x_min = min(min(pt_x), x_min)
            x_max = max(max(pt_x), x_max)
        if len(pt_y) > 0:
            y_min = min(min(pt_y), y_min)
            y_max = max(max(pt_y), y_max)

    print x_min, x_max, y_min, y_max
    color = (60, 80, 0)
    width = 5
    cv2.line(img, (x_min, y_min), (x_max, y_min), color, width)
    cv2.line(img, (x_max, y_min), (x_max, y_max), color, width)
    cv2.line(img, (x_max, y_max), (x_min, y_max), color, width)
    cv2.line(img, (x_min, y_max), (x_min, y_min), color, width)

    return img


def data_augmentation(image_arr, image_joint, image_attribute):
    # random.shuffle(image_arr)

    for each in image_arr[:1]:
        joints = image_joint[each]
        img_path = os.path.join('Data/img', each + '.jpg')

        img = cv2.imread(img_path)
        img = draw(img, img_path, joints, debug=False)
        img = find_bouding_box(img, joints)
        show_img(img)

    pass


if __name__ == "__main__":
    image_arr, image_joint, image_type, image_attribute = read_data(option=1)
    image_attribute = combine_attribute(image_arr, image_type, image_attribute)
    data_augmentation(image_arr, image_joint, image_attribute)
