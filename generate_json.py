import os, sys
import glob
import cv2
import numpy as np
import random

image_dir = "Data/labeled_img/"
label_dir = "Data/labeled_label_txt/"
label_json_dir = "Data/labeled_label_json/"

jpg_arr = [each.split('.')[0] for each in (glob.glob1(image_dir, "*.jpg"))]
txt_arr = [each.split('.')[0] for each in (glob.glob1(label_dir, "*.txt"))]

res = []
for each in jpg_arr:
    if each in txt_arr:
        res.append(each)


def parse_txt(filename):
    txt_dir = label_dir + filename + ".txt"
    with open(txt_dir, 'r') as fp:
        pt = fp.readline().strip()

    import re
    temp = re.split(r"[\s\t\r\n]+",pt)
    temp = [int(each) for each in temp]
    temp = zip(temp[0::2],temp[1::2])
    # pts = np.array(temp)
    # pts = pts.reshape((-1,1,2))
    return map(lambda each : tuple(each), temp)


def log_print(pts):
    print "Spine position",
    print "[%d %d]" % pts[0],
    print "[%d %d]" % pts[1]

    print "Left hand position",
    print "[%d %d]" % pts[1],
    print "[%d %d]" % pts[2],
    print "[%d %d]" % pts[3]

    print "Right hand position",
    print "[%d %d]" % pts[4],
    print "[%d %d]" % pts[5],
    print "[%d %d]" % pts[6]

    print "Left leg position",
    print "[%d %d]" % pts[7],
    print "[%d %d]" % pts[8],
    print "[%d %d]" % pts[9]

    print "Right leg position",
    print "[%d %d]" % pts[10],
    print "[%d %d]" % pts[11],
    print "[%d %d]" % pts[12]




def change_format(id, size, pts, des):
    data = extract_data(id, size, pts)
    import json
    des_dir = os.path.join(des, id + ".json")
    with open(des_dir, 'w+') as fp:
        json.dump(data, fp, indent=2)


def extract_data(id, size, pts):
    data = {}

    # image name
    data['img_id'] = id

    def inside(point, size):
        if point[0] <= 0 or point[0] > size[0] or point[1] <= 0 or point[1] > size[1]:
            return False
        return True

    pt_set = {
              "spine" : list(pts[:3]), # 0 1 2
              "left_hand" : list(pts[3:6]),
              "right_hand" : list(pts[6:9]),
              "left_leg" : list(pts[9:12]),
              "right_leg" : list(pts[12:15])
              }

    for part in pt_set:
        data[part] = [{"position" : each, "visible" : True} for each in pt_set[part]]

    return data


def main():
    random.shuffle(res)

    for each in res:

        img_dir = image_dir + each + ".jpg"
        # print img_dir

        img = cv2.imread(img_dir)
        height, width = img.shape[:2]
        size = (height, width)

        pts = parse_txt(each)
        # pts = np.array([[10,10],[200,10],[200,200],[10,200]])
        # pts = pts.reshape((-1,1,2))

        # old_draw(img, img_dir, pts, position_print=False)
        data = extract_data(each, size, pts)
        change_format(each, size, pts, label_json_dir)
        # print data



if __name__ == "__main__":
    main()

