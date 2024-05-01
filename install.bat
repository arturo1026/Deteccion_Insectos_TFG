@echo off

rem Instalar dependencias
pip install -r "%~dp0instalacion\requirements.txt"

rem Instalar el paquete
python "%~dp0instalacion\setup.py" install

rem Espera a que el usuario vea el resultado antes de cerrar la ventana
pause
