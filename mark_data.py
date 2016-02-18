import os, sys, glob
import json
import cv2
import numpy as np
import random

image_dir = "Data/img/"
label_dir = "Data/tmp/"
with open("config.json", 'r+') as fp:
    data = json.load(fp)
    image_dir = data["image_dir"]
    label_dir = data["label_dir"]

if not os.path.isdir(image_dir) or not os.path.isdir(label_dir):
    print ("image dir or label dir doesn't exist")
    exit(-1)


jpeg_arr = [each.split('.')[0] for each in (glob.glob1(image_dir, "*.jpg"))]
json_arr = [each.split('.')[0] for each in (glob.glob1(label_dir, "*.json"))]

print "There are %d files end with .jpg in %s" % (len(jpeg_arr), image_dir)
print "There are %d files end with .json in %s" % (len(label_dir), label_dir)

color_dict = {
    "spine": (170, 120, 0),
    "left_hand": (0, 255, 0),
    "left_leg": (0, 255, 0),
    "right_hand": (0, 0, 255),
    "right_leg": (0, 0, 255),
}

number2part = ["head"] + ["spine"] * 3 + ["left_hand"] * 3 + ["right_hand"] * 3 + \
              ["left_leg"] * 3 + ["right_leg"] * 3

count = 0
pt_list = []
stored_data = []


def type():
    global count
    if count == 0:
        return "head"
    elif count > 0 and count <= 3:
        return "spine"
    elif count <= 6:
        return "left_hand"
    elif count <= 9:
        return "right_hand"
    elif count <= 12:
        return "left_leg"
    elif count <= 15:
        return "right_leg"


# mouse callback function
def draw_circle(event, x, y, flags, param):
    global count
    if count > 15:
        return
    if event == cv2.EVENT_LBUTTONDOWN:  # click mouse
        pt_list.append((x, y))
        cv2.circle(img, (x, y), 1, (170, 120, 0), 7)

        if count % 3 == 1 or count == 0:
            pass
        else:
            cv2.line(img, pt_list[count - 1], pt_list[count], color_dict[number2part[count]], 15)

        count += 1


def key_check(k, char):
    if k == ord(char.lower()) or k == ord(char.upper()):
        return True
    else:
        return False


if __name__ == "__main__":
    random.shuffle(jpeg_arr)

    for each in jpeg_arr[:1]:
        img_path = image_dir + each + ".jpg"
        data_path = label_dir + each + ".json"

        img = cv2.imread(img_path)
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', draw_circle)

        count = 0
        pt_list = []

        '''
            0 : Head
            1~3 : Spine
            4~6 : Left hand
            7~9 : Right hand
            10~12 : Left leg
            13~15 : Right leg
        '''

        while (1):
            cv2.imshow('image', img)
            k = cv2.waitKey(1) & 0xFF

            if key_check(k, 'm'):
                print ("m is pressed")
            elif key_check(k, 'x'):
                if count > 15:
                    continue
                print ("x is pressed, %s is invisible") % number2part[count]
                pt_list.append((-1, -1))
                count += 1
            elif key_check(k, 'r'):  # Re mark
                print ("re-mark the data")
                pt_list = []
                count = 0
                img = cv2.imread(img_path)
            elif key_check(k, 'n'):  # Next mark
                if count > 15:
                    data = {}
                    data["id"] = each
                    for i in xrange(len(pt_list)):
                        part = number2part[i]
                        temp = {}
                        temp["visible"] = False if pt_list[i] == (-1, -1) else True
                        temp["position"] = list(pt_list[i])

                        if part not in data:
                            data[part] = []
                        data[part].append(temp)

                    print ("%s has been marked") % data_path
                    import json
                    with open(data_path, 'w+') as fp:
                        json.dump(data, fp, indent=2)
                    break
                else:
                    print ("not enough joint")
            elif key_check(k, 't'):
                print img_path
                print data_path
            elif key_check(k, 's'):
                print ("skip this picture")
                pt_list = []
                count = 0
                break
            elif k == 27:
                exit(0)

        cv2.destroyAllWindows()
