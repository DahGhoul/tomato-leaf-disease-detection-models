@echo off
TITLE Tomatismo - Sistema Portable en USB
color 0A

echo ===================================================
echo    Iniciando Deteccion de Enfermedades en Tomate
echo ===================================================
echo.

:: Cambiar al directorio del USB
cd /d "%~dp0"

:: Verificar si la carpeta de dependencias existe
IF NOT EXIST "librerias_usb" (
    echo [!] Preparando el USB por PRIMERA Y UNICA VEZ...
    echo Esto descargara las librerias directamente dentro del USB para que no tengas que descargar nada en otras PCs.
    echo.
    python -m pip install --target librerias_usb -r requirements.txt
    echo.
    echo [OK] Librerias guardadas en el USB.
) ELSE (
    echo [OK] Dependencias detectadas en el USB. No se descargara nada.
)

echo.
echo Iniciando aplicacion web super rapido...
echo.

:: Decirle a Python que use las librerias que estan en el USB, no las de la PC
set PYTHONPATH=%~dp0librerias_usb
set PATH=%~dp0librerias_usb\bin;%~dp0librerias_usb\Scripts;%PATH%

:: Iniciar la aplicacion usando el Python instalado en la PC destino
python -m streamlit run app.py

pause
