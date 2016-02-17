import os, sys
import glob
import shutil

ori_dir = ["Datasets/07.Skeleton/Label_Results/labeled1-2-3/labeled1/",
           "Datasets/07.Skeleton/Label_Results/labeled1-2-3/labeled2/",
           "Datasets/07.Skeleton/Label_Results/labeled1-2-3/labeled3/",
           "Datasets/07.Skeleton/Label_Results/4/labeled/",
           "Datasets/07.Skeleton/Label_Results/5/labeled/"]

des_img_dir = "Data/labeled_img/"
des_label_dir = "Data/labeled_label_txt/"


def test_legal():
    img = glob.glob1(des_img_dir,"*.jpg")
    txt = glob.glob1(des_label_dir,"*.txt")

    img = map(lambda x: x.split('.')[0], img)
    txt = map(lambda x: x.split('.')[0], txt)

    count = sum([1 if each in img else 0 for each in txt])
    print (count)



if __name__ == "__main__":
    test_legal()