import cv2
import glob, os
import json, random
from generate_json import log_print

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
            "head" : (100, 100, 255),
            "spine" : (170,120,0),
            "left_hand" : (0, 255, 0),
            "left_leg" : (0, 255, 0),
            "right_hand" : (0, 0, 255),
            "right_leg" : (0, 0, 255),
            }


def my_loop(array):
    for i in xrange(len(array) - 1):
        yield array[i], array[i+1]


def test(img="1.jpg"):
    id = img.split('.')[0] if img.endswith(".jpg") else img
    img_dir = os.path.join(image_dir,id + ".jpg")
    data_dir = os.path.join(label_dir,id + ".json")
    with open(data_dir) as fp:
        img = cv2.imread(img_dir)
        data = json.load(fp)

    new_draw(img, img_dir, pts=data)



def new_draw(img, img_dir, pts):
    global color_dict

    print img_dir
    for part in pts:
        if part == "img_id":
            continue

        print part
        temp_color = color_dict[part]
        if part == "head":
            cv2.circle(img, tuple(pts[part][0]["position"]), 1, temp_color, 10)
        else :
            for d1, d2 in my_loop(pts[part]):
                pt1 = tuple(d1["position"])
                pt2 = tuple(d2["position"])
                print pt1, pt2
                if d1["visible"] and d2["visible"]:
                    cv2.line(img, pt1, pt2, temp_color, 5)

    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def old_draw(img, img_dir , pts, position_print=True):
    for i in xrange(len(pts)):
        point = pts[i]
        cv2.circle(img,pts[i], 1, (128, 128, 128), 10)

    line_width = 5
    spine_color = (170,120,0)
    left_hand_color = (0, 255, 0)
    right_hand_color = (0, 0, 255)
    left_leg_color = left_hand_color
    right_leg_color = right_hand_color

    # Spine
    cv2.line(img, pts[0], pts[1], spine_color, line_width)
    cv2.line(img, pts[1], pts[2], spine_color, line_width)

    # Left hand
    cv2.line(img, pts[0], pts[3], left_hand_color, line_width)
    cv2.line(img, pts[3], pts[4], left_hand_color, line_width)
    cv2.line(img, pts[4], pts[5], left_hand_color, line_width)

    # Right hand
    cv2.line(img, pts[0], pts[6], right_hand_color, line_width)
    cv2.line(img, pts[6], pts[7], right_hand_color, line_width)
    cv2.line(img, pts[7], pts[8], right_hand_color, line_width)

    # Left leg
    cv2.line(img, pts[2], pts[9], left_leg_color, line_width)
    cv2.line(img, pts[9], pts[10], left_leg_color, line_width)
    cv2.line(img, pts[10], pts[11], left_leg_color, line_width)
    # Right leg
    cv2.line(img, pts[2], pts[12], right_leg_color, line_width)
    cv2.line(img, pts[12], pts[13], right_leg_color, line_width)
    cv2.line(img, pts[13], pts[14], right_leg_color, line_width)



    if position_print:
        print "=================="
        print "image name : %s" % (img_dir)
        height, width = img.shape[:2]
        print "image size : [%d %d]" % (height, width)
        log_print(pts)

    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    random.shuffle(jpeg_arr)
    random.shuffle(json_arr)
    for each in json_arr[:15]:
        if each not in jpeg_arr:
            continue

        img_dir = image_dir + each + ".jpg"
        json_dir = label_dir + each + ".json"

        # print os.path.isfile(img_dir), os.path.isfile(json_dir)

        with open(json_dir) as fp:
            img = cv2.imread(img_dir)
            data = json.load(fp)

        new_draw(img, img_dir, pts=data)

