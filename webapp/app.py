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
tf.config.set_visible_devices([], 'GPU')


process_status = {}



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'una_clave_secreta_very_secret'


def create_or_get_session_id():
    if 'session_id' not in session:
        # Genera un identificador único para la sesión
        session['session_id'] = os.urandom(16).hex()
    return session['session_id']

def update_status(session_id, status, progress):
    if session_id not in process_status:
        process_status[session_id] = {}
    process_status[session_id]['status'] = status
    process_status[session_id]['progress'] = int(progress)


@app.route('/get_status')
def get_status():
    session_id = create_or_get_session_id()
    status = process_status.get(session_id, {'status': 'Listo', 'progress': 0})
    return jsonify(status)


class PredictionConfig(Config):
	# definimos nombre de configurcion
	NAME = "insects_cfg"
	# tendremos 3 clases (3 insectos) + 1 que seria el fondo
	NUM_CLASSES = 1 + 3
	# Especificamos que utilziaremos una sola GPU 
	GPU_COUNT = 1
    # Indicamos cuantas imagenes se procesaran por GPU a la vez
	IMAGES_PER_GPU = 1


# preparemos la configuracion
cfg = PredictionConfig()
cfg.display() # aseguramos de la correcta configuracion

# prepareamos el directorio donde se guardara el modelo
import os
ROOT_DIR = os.path.abspath("./")
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "weights")
 
##############

# Iniciamos el modelo con la configuracion previa 

model = MaskRCNN(mode='inference', model_dir='logs', config=cfg, optimizer='SGD')


model.load_weights('logs/mask_rcnn_insects_cfg_24_04_2024.h5', by_name=True)



# Ruta a la página principal
@app.route('/')
def index():
    return render_template('index.html')

def count_class_ids(class_ids):
    class_id_counter_WF = 0  
    class_id_counter_NC = 0  
    class_id_counter_MR = 0  
    class_id_counter_TOTAL = 0  # Contador para el total de elementos

    # Iteramos sobre cada elemento en el array para contar las ocurrencias
    for class_id in class_ids:
        if class_id == 1:
            class_id_counter_WF += 1
        elif class_id == 2:
            class_id_counter_NC += 1
        elif class_id == 3:
            class_id_counter_MR += 1
        class_id_counter_TOTAL += 1  # Incrementamos el contador total en cada iteración

    # Retornamos una lista con los contadores
    return [class_id_counter_WF, class_id_counter_NC, class_id_counter_MR, class_id_counter_TOTAL]



@app.route('/deteccion', methods=['GET', 'POST'])
def deteccion():
    pngImageB64String = ''
    conteos = []  # Inicialización de conteos

    if request.method == 'POST':
        try:
            session_id = create_or_get_session_id()
            print("Solicitud recibida")
            file = request.files['fileInput']
            if not file or file.filename == '':
                print("No se seleccionó ningún archivo")
                return 'No se seleccionó ningún archivo', 400

            print("cargando")
            update_status(session_id, 'Cargando imagen...', 20)
            insect_img = skimage.io.imread(file.stream)

            print("detectando")
            update_status(session_id, 'Realizando detección...', 50)
            detected = model.detect([insect_img])[0]

            print("graficando")
            update_status(session_id, 'Graficando resultados...', 80)
            fig, ax = pyplot.subplots()
            display_instances(insect_img, detected['rois'], detected['masks'], detected['class_ids'],
                              ['BG', 'WF', 'NC', 'MR'], detected['scores'], ax=ax)

            pngImage = BytesIO()
            FigureCanvas(fig).print_png(pngImage)
            pyplot.close(fig)

            print("codificando")
            update_status(session_id, 'Codificando...', 90)
            pngImageB64String = "data:image/png;base64," + base64.b64encode(pngImage.getvalue()).decode('utf8')

            conteos = count_class_ids(detected['class_ids'])
            update_status(session_id, 'Proceso completado con éxito.', 100)

            return render_template('deteccion.html', image_data=pngImageB64String, conteos=conteos)
        except Exception as e:
            print("Error durante la detección o la visualización:", e)
            return str(e), 500

    return render_template('deteccion.html', image_data=pngImageB64String, conteos=conteos)





@app.route('/entrenamiento', methods=['GET', 'POST'])
def entrenamiento():
        print("hola entrenamiento")
        return render_template('entrenamiento.html')







if __name__ == '__main__':
    app.run(debug=True, threaded=False)



    