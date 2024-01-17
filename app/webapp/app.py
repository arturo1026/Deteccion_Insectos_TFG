from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Ruta a la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar la carga de imágenes y entrenamiento
@app.route('/entrenamiento', methods=['POST'])
def entrenamiento():
    # Lógica para manejar la carga de imágenes y entrenamiento
    # Aquí puedes implementar tu lógica para el entrenamiento de la red neuronal

    # Ejemplo: obtén el archivo de la solicitud
    uploaded_file = request.files['fileInput']

    # Lógica para guardar y procesar la imagen
    if uploaded_file:
        image_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(image_path)

        # Aquí implementar la lógica para la predicción con la imagen
        # (Asumiendo que ya tienes un modelo entrenado)

        prediction = "Insecto predicho"

        # Redirige a la página de entrenamiento con el resultado de la predicción
        return redirect(url_for('entrenamiento', prediction=prediction))

    return render_template('entrenamiento.html', result="No se pudo completar el entrenamiento")

# Ruta para la página de entrenamiento (GET)
@app.route('/entrenamiento')
def mostrar_entrenamiento():
    # Obtén el resultado de la predicción enviado como argumento en la URL
    prediction = request.args.get('prediction', 'No se ha proporcionado una predicción')

    return render_template('entrenamiento.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)