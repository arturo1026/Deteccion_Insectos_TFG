## Instalación

Para instalar el proyecto, se recomienda utilizar un entorno virtual de conda con la versión de Python 3.7.11. Puedes optar por utilizar el script `install.bat` para una instalación automatizada en Windows o seguir los pasos de instalación manual. A continuación, se describen ambos métodos:

### Método 1: Instalación Automatizada en Windows

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/Deteccion_Insectos_TFG.git
    cd Deteccion_Insectos_TFG
    ```

2. Se recomienda crear y activar un entorno virtual con conda como se ha hecho en este caso:
    ```sh
    conda create --name deteccion_insectos python=3.7.11
    conda activate deteccion_insectos
    ```

3. Ejecuta el script de instalación:
    ```sh
    cd instalacion
    install.bat
    ```

   El script `install.bat` instalará automáticamente los requisitos del proyecto y configurará Mask R-CNN.

### Método 2: Instalación Manual

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/Deteccion_Insectos_TFG.git
    cd Deteccion_Insectos_TFG
    ```

2. Se recomienda crear y activar un entorno virtual con conda como se ha hecho en este caso:
    ```sh
    conda create --name deteccion_insectos python=3.7.11
    conda activate deteccion_insectos
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Configura Mask R-CNN:
    ```sh
    cd mrcnn
    python setup.py install
    ```

   Este paso instalará y configurará la biblioteca Mask R-CNN necesaria para el proyecto.

---



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

| Permissions | Limitations | Conditions |
| --- | --- | --- |
| ✔️ Commercial use | ❌ Liability | ℹ️ License and copyright notice |
| ✔️ Modification | ❌ Warranty |  |
| ✔️ Distribution |  |  |
| ✔️ Private use |  |  |

For more details, see the [LICENSE](LICENSE) file.
