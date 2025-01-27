#!/bin/python3

import os
import shutil
import zipfile
from tempfile import mkdtemp
import subprocess

###### Inicio configuracion ######
year_i = 1980  # Año inicio (Incluido)
year_f = 2023  # Año fin (Incluido)
month_i = 1  # Mes inicio (Incluido)
month_f = 12  # Mes fin (Incluido)
filename = "era5.tp.sfc.hour"  # Nombra como se llama el archivo descargado/carpetas antes de la seccion del rango temporal

directorio_principal = "/home/user/download"  # Directorio que contiene los archivos ZIP descargados
directorio_final = "/home/user/directoriofinal"  # Directorio donde se generará el archivo .nc
###### Fin configuracion ######

def main():
    # Crear un directorio temporal
    directorio_temporal = mkdtemp(dir="/var/tmp")

    try:
        # Iterar sobre el rango de años y meses
        for year in range(year_i, year_f + 1):
            for month in range(month_i, month_f + 1):
                month_str = f"{month:02d}"  # Asegurar formato de dos dígitos
                archivo_zip = os.path.join(directorio_principal, f"{filename}.{year}.{month_str}.zip")
                archivo_nc = os.path.join(directorio_temporal, f"{filename}.{year}.{month_str}.nc")

                # Verificar si el archivo ZIP existe y procesarlo
                if os.path.isfile(archivo_zip):
                    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
                        # Extraer todos los archivos a un directorio temporal
                        zip_ref.extractall(directorio_temporal)

                        # Buscar el archivo .grib dentro del ZIP
                        archivos_extraidos = zip_ref.namelist()
                        archivo_grib = next((os.path.join(directorio_temporal, f) for f in archivos_extraidos if f.endswith("data.grib")), None)

                        if archivo_grib and os.path.isfile(archivo_grib):
                            # Convertir el archivo .grib a .nc (construye la operacion de CDO)
                            subprocess.run(["cdo", "-f", "nc", "copy", archivo_grib, archivo_nc], check=True)
                            print(f"Procesando archivo: {archivo_grib} de {archivo_zip}")
                        else:
                            print(f"Archivo data.grib no encontrado en: {archivo_zip}")
                else:
                    print(f"Archivo ZIP no encontrado: {archivo_zip}")

        # Verificar si hay archivos .nc temporales
        archivos_nc = [os.path.join(directorio_temporal, f) for f in os.listdir(directorio_temporal) if f.endswith(".nc")]
        if archivos_nc:
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
