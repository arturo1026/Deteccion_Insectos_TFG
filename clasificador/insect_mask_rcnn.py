# split into train and test set
from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset
from matplotlib import pyplot
from mrcnn.visualize import display_instances
from mrcnn.utils import extract_bboxes

from mrcnn.config import Config
from mrcnn.model import MaskRCNN


# class that defines and loads the kangaroo dataset
class InsectDataset(Dataset):
    # load the dataset definitions
    def load_dataset(self, dataset_dir, is_train=True):
        # define classes
        self.add_class("dataset", 1, "WF")
        self.add_class("dataset", 2, "NC")
        self.add_class("dataset", 3, "MR")

        # define data locations
        images_dir = dataset_dir + '/images/'
        annotations_dir = dataset_dir + '/annots/'

        # find all images
        for filename in listdir(images_dir):
            print(filename)
            # extract image id
            image_id = filename[:-4]
            # print('IMAGE ID: ',image_id)

            # skip all images after 196 if we are building the train set
            if is_train and int(image_id) >= 196:  # 70%
                continue
            # skip all images before 196 if we are building the val set
            if not is_train and int(image_id) < 196:  # 30%
                continue
            img_path = images_dir + filename
            ann_path = annotations_dir + image_id + '.xml'
            # add to dataset
            self.add_image('dataset', image_id=image_id, path=img_path, annotation=ann_path, class_ids=[0, 1, 2, 3])
