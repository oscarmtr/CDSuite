#!/bin/python3

import os
import shutil
import subprocess
from tempfile import mkdtemp

###### Inicio configuracion ######
year_i = 1980  # Año inicio (Incluido)
year_f = 2023  # Año fin (Incluido)
n = 2  # De cuanto en cuantos años has realizado la solicitud
filename = "era5.z.10hPa.hour"  # Nombra como se llama el archivo descargado/carpetas antes de la seccion del rango temporal

directorio_principal = "/home/user/directorio/era5.z.10hPa.day.1980.2023"  # Directorio que contiene a las distintas carpetas que contienen los respectivos "data.grib"
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
            
            carpeta = os.path.join(directorio_principal, f"{filename}.{year}-{year_end}")
            archivo_grib = os.path.join(carpeta, "data.grib")
            archivo_nc = os.path.join(directorio_temporal, f"{filename}.{year}-{year_end}.nc")

            # Verificar si el archivo .grib existe y procesarlo
            if os.path.isfile(archivo_grib):
                subprocess.run(["cdo", "-f", "nc", "copy", archivo_grib, archivo_nc], check=True)
                print(f"Procesando archivo: {archivo_grib}")
            else:
                print(f"Archivo no encontrado: {archivo_grib}")

            # Pasar al siguiente intervalo de años
            year = year_end + 1

        # Verificar si hay archivos .nc temporales antes de combinar
        archivos_nc = [os.path.join(directorio_temporal, f) for f in os.listdir(directorio_temporal) if f.endswith(".nc")]
        if archivos_nc:
            # Establecer la ruta de salida en el directorio principal
            archivo_salida = os.path.join(directorio_principal, f"{filename}.{year_i}-{year_f}.nc")
            subprocess.run(["cdo", "mergetime", *archivos_nc, archivo_salida], check=True)
            print(f"Archivos combinados en: {archivo_salida}")
        else:
            print("No se encontraron archivos para combinar.")

    finally:
        # Eliminar el directorio temporal
        shutil.rmtree(directorio_temporal)

if __name__ == "__main__":
    main()