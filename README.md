# Beihang data project

## Environment
* python2 >= 2.7.3
* python-opencv
    * Install opencv in ubuntu ```sudo apt-get install libopencv```
    * Install opencv in Mac OS X ```brew install opencv```

## How to mark
1. The order :
    * Head -> spine(3 points) -> left hand(3 points) -> right hand(3 points) -> left leg(3 points) -> right leg(3 points)

2. Keyboard
    * N : Next picture (You have to mark all points before going to next image)
    * X : If this point is invisible
    * R : Re-mark the data (if you mark something wrong)
    * S : Skip this image
    * ESC : Exit program

## Procedure:
1. Get python project and data set
    * ```git clone git@github.com:Lyken17/BeihangData.git```
    * [google drive](https://drive.google.com/folderview?id=0B3lu5NBSC7pVSV9hM1h5VTV3SW8&usp=sharing)
    pictures are split into 21 groups, each group has 200 images.
2. Specify the image and label path
    There is an `config.json`. Set `image_dir` and `label_dir` to your own directory.
3. Run code
    ```python mark_data```

## Tips
1. How to examine my label result?
    * To check all ```python draw_img```
    * To check specified picture

        ```
        In[2]: from draw_img import test
        In[3]: test("myfile.jpg")
        ```

2. 




