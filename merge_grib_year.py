#!/bin/python3

import os
import shutil
import subprocess
import zipfile
from tempfile import mkdtemp

###### Inicio configuracion ######
year_i = 1980  # Año inicio (Incluido)
year_f = 2023  # Año fin (Incluido)
n = 2  # De cuánto en cuántos años has realizado la solicitud
filename = "era5.z.10hPa.hour"  # Nombre base de los archivos descargados/archivos ZIP

directorio_principal = "/home/user/directorio/era5.z.10hPa.hour.1980-2023"  # Directorio que contiene los archivos ZIP
directorio_final = "/home/user/directoriofinal" # Directorio donde se generará el archivo .nc
###### Fin configuracion ######

def main():
    # Crear un directorio temporal
    directorio_temporal = mkdtemp(dir="/var/tmp")

    try:
        # Iterar sobre los años con intervalos de 'n'
        year = year_i
        while year <= year_f:
            # Definir el rango de años para este archivo
            year_end = min(year + n - 1, year_f)  # No exceder el año final
            archivo_zip = os.path.join(directorio_principal, f"{filename}.{year}-{year_end}.zip")
            archivo_nc = os.path.join(directorio_temporal, f"{filename}.{year}-{year_end}.nc")

            # Verificar si el archivo ZIP existe y procesarlo
            if os.path.isfile(archivo_zip):
                with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
                    # Extraer todos los archivos a un directorio temporal
                    zip_ref.extractall(directorio_temporal)

                    # Buscar el archivo .grib dentro del ZIP
                    archivos_extraidos = zip_ref.namelist()
                    archivo_grib = next((os.path.join(directorio_temporal, f) for f in archivos_extraidos if f.endswith("data.grib")), None)

                    if archivo_grib and os.path.isfile(archivo_grib):
                        # Convertir el archivo .grib a .nc
                        subprocess.run(["cdo", "-f", "nc", "copy", archivo_grib, archivo_nc], check=True) # Construye la operacion de CDO
                        print(f"Procesando archivo: {archivo_grib} de {archivo_zip}")
                    else:
                        print(f"Archivo data.grib no encontrado en: {archivo_zip}")
            else:
                print(f"Archivo ZIP no encontrado: {archivo_zip}")

            # Pasar al siguiente intervalo de años
            year = year_end + 1

        # Verificar si hay archivos .nc temporales antes de combinar
        archivos_nc = [os.path.join(directorio_temporal, f) for f in os.listdir(directorio_temporal) if f.endswith(".nc")]
        if archivos_nc:
            # Establecer la ruta de salida en el directorio principal
            archivo_salida = os.path.join(directorio_final, f"{filename}.{year_i}-{year_f}.nc")
            subprocess.run(["cdo", "mergetime", *archivos_nc, archivo_salida], check=True)
            print(f"Archivos combinados en: {archivo_salida}")
        else:
            print("No se encontraron archivos para combinar.")

    finally:
        # Eliminar el directorio temporal
        shutil.rmtree(directorio_temporal)

if __name__ == "__main__":
    main()
