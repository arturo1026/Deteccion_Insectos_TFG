import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os

def mostrarImagenDilimitadores(fich_xml, fich_jpg, ImagenesParseadas):
    # Parsear el archivo XML
    tree = ET.parse(fich_xml)
    root = tree.getroot()

    # Cargar la imagen
    img = Image.open(fich_jpg)

    # Crear la figura y mostrar la imagen
    plt.figure(figsize=(11, 11))
    plt.imshow(img)

    # Dibujar los cuadros delimitadores de los objetos
    for obj in root.findall('.//object'):
        name = obj.find('name').text
        bbox = obj.find('.//bndbox')

        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)

        rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='r', facecolor='none')
        plt.gca().add_patch(rect)
        plt.text(xmin, ymin, name, color='r', backgroundcolor='none', fontsize=8)

    plt.axis('on')  # Desactivar ejes

    # Guardar la figura en la carpeta de salida
    output_path = os.path.join(ImagenesParseadas, f'parsed_image_{os.path.basename(fich_jpg)}')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def mostrarImagenesEnCarpeta(dataset_path, ImagenesParseadas):
    i = 1001
    while True:
        # Construir rutas de archivos
        fichero_jpg = os.path.join(dataset_path, f'{i}.jpg')
        fichero_xml = os.path.join(dataset_path, f'{i}.xml')

        # Verificar si ambos archivos existen antes de llamar al método
        if os.path.exists(fichero_jpg) and os.path.exists(fichero_xml):
            mostrarImagenDilimitadores(fichero_xml, fichero_jpg, ImagenesParseadas)
            i += 1
        else:
            break

def ParseoImagenes():
    # Ruta de la carpeta de salida para las imágenes parseadas
    ImagenesParseadas = "ImagenesParseadas"

    # Crear la carpeta de salida si no existe
    os.makedirs(ImagenesParseadas, exist_ok=True)

    mostrarImagenesEnCarpeta("4TUDatasetAnonymised", ImagenesParseadas)

ParseoImagenes()
