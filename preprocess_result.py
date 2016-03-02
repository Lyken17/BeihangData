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

augmentation_times = 8
img_plot = False

output_dir = "Data/output/"
image_output = os.path.join(output_dir, 'img')
data_ouput = output_dir + 'data.json'


def count_attribute(image_arr, image_type, image_attribute, option=0):
    '''
    :param image_arr: img_id list
    :param image_type: key-value, img_id : type
    :param image_attribute: key-value, img_id : attribute
    :param option: 0 means "generate from file", 1 means read from json.
    :return:
    '''

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
    select_k_largest = lambda x: dict(sorted(x.items(), key=lambda x: x[1], reverse=True)[:3])
    attr_count = {each: select_k_largest(attr_count[each] if each != "Cloth_Type" else attr_count[each]) for each in
                  attr_count}

    for img_id in image_arr[:]:
        attr = image_attribute[img_id]
        attr.update(image_type[img_id])
        cur = {}

        type_list = ['placket', 'sleeve_type', 'collar_type', 'button_type', 'cloth_type']
        key_list = ['Placket1', 'SleeveLength', 'CollarType', 'ButtonType', 'Cloth_Type']

        # Todo
        # don't forget some special case
        for i in xrange(len(type_list)):
            temp_type = type_list[i]
            temp_attr = attr[key_list[i]]

            cur[temp_type] = {each: False for each in attr_count[key_list[i]]}
            cur[temp_type]['0'] = False

            # print temp_type, temp_attr
            if temp_attr in attr_count[key_list[i]]:
                cur[temp_type][temp_attr] = True
            else:
                cur[temp_type]['None'] = True
        ans[img_id] = cur

    return ans


def bbox_generate(height, weight, x_min, y_min, x_max, y_max):
    h, w = height, weight

    # print x_min, x_max, y_min, y_max
    mu, sigma = 0, 2
    ra = np.random.normal(mu, sigma)
    # print ra
    width = min(x_max - x_min, y_max - y_min) * 0.3

    # print width, h, w
    x_min = int(min(max(0, x_min - width * np.random.normal(mu, sigma)), max(0, x_min - 10)))
    y_min = int(min(max(0, y_min - width * np.random.normal(mu, sigma)), max(0, y_min - 10)))
    x_max = int(max(min(w, x_max + width * np.random.normal(mu, sigma)), min(w, x_max + 10)))
    y_max = int(max(min(h, y_max + width * np.random.normal(mu, sigma)), min(h, y_max + 10)))
    height, weight = y_max - y_min, x_max - x_min
    ratio = height / float(weight)

    if 0.8 <= ratio <= 1.25:
        return x_min, y_min, x_max, y_max
    elif ratio < 0.8:
        x_min = int(max(0, x_min - weight * 0.1))
        x_max = int(min(w, x_max + weight * 0.1))
        return x_min, y_min, x_max, y_max
    elif ratio > 1.25:
        y_min = int(max(0, y_min - height * 0.1))
        y_max = int(min(h, y_max + height * 0.1))
        return x_min, y_min, x_max, y_max


def find_bouding_box(img, joints, times=8):
    x_min, y_min = 30000, 30000
    x_max, y_max = 0, 0
    h, w = img.shape[:2]

    for part in joints:
        if part in ['img_id', 'id', 'left_leg', 'right_leg']:
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

    bbox_arr = []
    for i in xrange(times):
        temp_img = np.array(img, copy=True)
        x1, y1, x2, y2 = bbox_generate(h, w, x_min, y_min, x_max, y_max)
        bbox_arr.append([x1, y1, x2, y2])
        # show_img(temp_img[y1:y2, x1:x2])

    return bbox_arr


def data_augmentation(image_arr, image_joint, image_type, image_attribute):
    '''
    :param image_arr: list of image id
    :param image_joint: key-value , img_id : joints
    :param image_type: key-value, img_id : type
    :param image_attribute: key-value, img_id : attribtue
    :return: None
    '''
    random.shuffle(image_arr)
    total_json = {}
    for img_id in image_arr[:]:
        temp_attribute = image_attribute[img_id]
        temp_type = image_type[img_id]
        joints = image_joint[img_id]

        # print joints
        if joints['head'][0]['visible'] == False:
            continue

        img_path = os.path.join('Data/img', img_id + '.jpg')

        img = cv2.imread(img_path)
        # img = draw(img, img_path, joints, debug=False)
        bbox = find_bouding_box(img, joints, times=augmentation_times)

        new_joints = []
        for part in ['head', 'spine', 'left_hand', 'right_hand']:
            for each_pos in joints[part]:
                new_joints.append(each_pos['position'])

        count = 0
        for each in bbox:
            count += 1
            if img_plot:
                print each
            # print new_joints
            cur_h = each[3] - each[1]
            cur_w = each[2] - each[0]
            x_scale = float(227) / cur_w
            y_scale = float(227) / cur_h

            # transform x, y
            temp_joints = [[(pos[0] - each[0]) * x_scale, (pos[1] - each[1]) * y_scale] \
                           for pos in new_joints]
            temp_joints = [[int(pos[0]), int(pos[1])] for pos in temp_joints]

            # Crop img
            temp_img = np.array(img[each[1]:each[3], each[0]:each[2]], copy=True)
            temp_img = cv2.resize(temp_img, (227, 227))

            # print temp_joints
            if img_plot:
                for j in temp_joints:
                    cv2.circle(temp_img, tuple(j), 1, (255, 0, 0), 10)
                show_img(temp_img)

            temp_id = img_id + '_augmentation_' + str(count)
            # write to json and file
            total_json[temp_id] = {}
            total_json[temp_id]["joints"] = temp_joints
            total_json[temp_id]["attribute"] = temp_attribute
            total_json[temp_id]["type"] = temp_type

            cv2.imwrite(os.path.join(image_output, temp_id + '.jpg'), temp_img)

            # ======= Reverse img ========
            '''
            temp_img = np.array(img[each[1]:each[3], each[0]:each[2]], copy=True)
            temp_img = cv2.resize(temp_img, (227, 227))
            # temp_joints = [[int(temp_img.shape[2] - pos[0]), int(pos[1])] for pos in temp_joints]

            for j in temp_joints:
                cv2.circle(temp_img, tuple(j), 1, (255, 0, 0), 10)
            show_img(temp_img)
            '''
    with open(data_ouput, 'w+') as fp:
        json.dump(total_json, fp)

    pass


if __name__ == "__main__":
    image_arr, image_joint, image_type, image_attribute = read_data(option=1)
    image_attribute = combine_attribute(image_arr, image_type, image_attribute)
    # print image_attribute
    # data_augmentation(image_arr, image_joint, image_type, image_attribute)
