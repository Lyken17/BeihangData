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


image_arr_dir = "Data/image_arr.json"
image_label_dir = "Data/image_label.json"
image_type_dir = "Data/image_type.json"
image_attribute_dir = "Data/image_attribute.json"
