# Beihang data project

## Environment
* python2 >= 2.7.3
* python-opencv
    * Install opencv in ubuntu ```sudo apt-get install libopencv```
    * Install opencv in Mac OS X ```brew install opencv```

## Dataset
pictures are split into 9 groups, each group has 500 images. [google drive](https://drive.google.com/folderview?id=0B3lu5NBSC7pVTWhxeG1oVVV1bWM&usp=sharing)

## How to mark
* The order :
    * Head -> spine(3 points) -> left arm(3 points) -> right arm(3 points) -> left leg(3 points) -> right leg(3 points)

* Keyboard
    * N : Next picture (You have to mark all points before going to next image)
    * X : If this point is invisible
    * R : Re-mark the data (if you mark something wrong)
    * S : Skip this image
    * ESC : Exit program

## Procedure:
1. Get python project and data set
    * ```git clone git@github.com:Lyken17/BeihangData.git```
    * [google drive](https://drive.google.com/folderview?id=0B3lu5NBSC7pVTWhxeG1oVVV1bWM&usp=sharing)
    pictures are split into 9 groups, each group has 500 images.
2. Specify the image and label path
    There is an `config.json`. Set `image_dir` and `label_dir` to your own directory.
3. Run code
    ```python mark_data```
4. Mark joint by order (press x, if this joint is invisible)

## Sample
![pic](https://cloud.githubusercontent.com/assets/7783214/13130814/d951852e-d59b-11e5-8451-bab13490edb1.png)

## PS
1. How to examine my label result?
    * To check all ```python draw_img```
    * To check specified picture

        ```
        In[2]: from draw_img import test
        In[3]: test("myfile.jpg")
        ```

2.




