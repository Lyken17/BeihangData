import os, sys
import glob
import cv2
import numpy as np
import random
from read_tool_box import *
from draw_img import *
from preprocess_result import *

if __name__ == "__main__":
    image_arr, image_joint, image_type, image_attribute = read_data(option=1)

    # print image_arr # image id list
    # print image_joint
    # print image_type.items()[:1] # cloth type
    print image_attribute.items()[:1]