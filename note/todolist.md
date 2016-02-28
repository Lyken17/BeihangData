# Useful labels
    * Collar
    * Sleeve
    * Cloth

# Generate lmdb
1. Clean data
	* make sure each id in image_arr also appears in  image_label, image_type, image_attribute.[Done]
    * combine labels, only choose top three labels and converts every label to binary result.
2. Data augmentation
    * Bounding box
        * Randomize bounding box
    * Left-right => right-left
3.         


# Necessary attribute
    Placket1 衣襟1
    Placket2 衣襟2
SleeveLength 袖子长度
CollarType
ButtonType

clothtype
