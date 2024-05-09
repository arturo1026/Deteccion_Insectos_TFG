from flask import Flask, render_template, request, redirect, url_for,session,jsonify
import os
from werkzeug.utils import secure_filename 
import skimage
import pickle
import base64 
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset
from matplotlib import pyplot
from mrcnn.visualize import display_instances
from mrcnn.utils import extract_bboxes
import tensorflow as tf
# Configuraciones para el entrenamiento y modelo 
from mrcnn.config import Config
from mrcnn.model import MaskRCNN
import matplotlib 
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import time 
from flask_socketio import SocketIO, emit
from keras.callbacks import Callback
from os import listdir
import threading
import sys

print("ha llegado a la config")
tf.config.set_visible_devices([], 'GPU')


class InsectsConfig(Config):
    NAME = "insects_cfg"
    NUM_CLASSES = 1 + 3  # background + 3 insect types
    STEPS_PER_EPOCH = 5

class InsectsDataset(Dataset):

    def load_dataset(self, dataset_dir, is_train=True):
        # definimos 3 clases de insectos ya que tendremos 3 insectos ha detectar
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
			#print('IMAGE ID: ',image_id)
			
			# skip all images after 196 if we are building the train set
            if is_train and int(image_id) >= 196: # 70%
                continue
			# skip all images before 196 if we are building the val set
            if not is_train and int(image_id) < 196: # 30%
                continue
            img_path = images_dir + filename
            ann_path = annotations_dir + image_id + '.xml'
			# add to dataset
            self.add_image('dataset', image_id=image_id, path=img_path, annotation=ann_path, class_ids = [0,1,2,3])


	# extrae los bordes de las cajas delimitadoras 
    def extract_boxes(self, filename):
		# load and parse the file
        tree = ElementTree.parse(filename)
		# get the root of the document
        root = tree.getroot()
		# extract each bounding box
        boxes = list()
        for box in root.findall('.//object'):
            name = box.find('name').text   #Add label name to the box list
            xmin = int(box.find('./bndbox/xmin').text)
            ymin = int(box.find('./bndbox/ymin').text)
            xmax = int(box.find('./bndbox/xmax').text)
            ymax = int(box.find('./bndbox/ymax').text)
            coors = [xmin, ymin, xmax, ymax, name]
            boxes.append(coors)
		# extract image dimensions
        width = int(root.find('.//size/width').text)
        height = int(root.find('.//size/height').text)
        return boxes, width, height

	# generamos las mascaras para cada uno de los insectos 
    def load_mask(self, image_id):
		# obtenemos informacion de la imagen como id_imagen ,dimensiones , anotacion correspondiente , ids_de los insectos presentes...
        info = self.image_info[image_id]
		# definimos las ubicaciones de las anotaciones 
        path = info['annotation']
        #return info, path
        
        
		# cargamos el .XML
        boxes, w, h = self.extract_boxes(path) #extraemos el ancho y alto de la caja delimitadora
		# creamos un array de 0 como mascara 
        masks = zeros([h, w, len(boxes)], dtype='uint8')
        # guardamos los id de los insectos
        class_ids = list()
        # Repetimso proceso para cada una de las  cajas 
        for i in range(len(boxes)):
            box = boxes[i]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            
            
            # El parametro quinto  recibira el nombre de la caja en este caso de su insecto correspondiente
            if (box[4] == 'WF'): # mosca blanca
                masks[row_s:row_e, col_s:col_e, i] = 1
                class_ids.append(self.class_names.index('WF'))
            elif(box[4] == 'NC'): # nesidicoris
                masks[row_s:row_e, col_s:col_e, i] = 2
                class_ids.append(self.class_names.index('NC')) 
            elif(box[4] == 'MR'): # macrolophus
                masks[row_s:row_e, col_s:col_e, i] = 3
                class_ids.append(self.class_names.index('MR'))
          
        return masks, asarray(class_ids, dtype='int32')
        

	# cargamos la imagen de referencia
    def image_reference(self, image_id):
        info = self.image_info[image_id]
        return info['path']

dataset_dir='datasets/renamed_to_numbers'

train_set = InsectsDataset()
train_set.load_dataset(dataset_dir, is_train=True)
train_set.prepare()
print('Train: %d' % len(train_set.image_ids))

# test/val conjunto
test_set = InsectsDataset()
test_set.load_dataset(dataset_dir, is_train=False)
test_set.prepare()
print('Test: %d' % len(test_set.image_ids))

def train_model():
    
    print("Ha entrado al script")
    # Configura el entorno y el modelo
    filename = sys.argv[1] 
    print("el archivo",filename)
    config = InsectsConfig()
    model = MaskRCNN(mode='training', model_dir="logs", config=config, optimizer="SGD")
    
    # Carga los pesos iniciales, excluyendo las últimas capas para personalización
    model.load_weights("weights/mask_rcnn_coco.h5", by_name=True, exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])
    
    # Preparar datasets
    dataset_dir = 'datasets/renamed_to_numbers'  # Ajusta esta ruta según donde tengas tus datos
    train_set = InsectsDataset()
    train_set.load_dataset(dataset_dir, is_train=True)
    train_set.prepare()

    test_set = InsectsDataset()
    test_set.load_dataset(dataset_dir, is_train=False)
    test_set.prepare()

    # Entrena el modelo
    model.train(train_set, test_set, learning_rate=config.LEARNING_RATE, epochs=1, layers='heads')
    
    model_path = './weights/' + filename + '.h5'
    model.keras_model.save_weights(model_path)
    print("guardar")
    print("Model training completed and saved.")
    # Al final del entrenamiento:
    


if __name__ == "__main__":
    train_model()

