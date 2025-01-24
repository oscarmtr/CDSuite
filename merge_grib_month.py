#!/bin/python3

import os
import shutil
import subprocess
from tempfile import mkdtemp

###### Inicio configuracion ######
year_i = 1980  # Año inicio (Incluido)
year_f = 2023  # Año fin (Incluido)
month_i = 1  # Mes inicio
month_f = 12  # Mes fin
filename = "era5.tp.sfc.hour" # Nombra como se llama el archivo descargado/carpetas antes de la seccion del rango temporal

directorio_principal = "/home/user/download" # Directorio que contiene a las distintas carpetas que contienen los respectivos "data.grib"
###### Fin configuracion ######

def main():
    # Crear un directorio temporal
    directorio_temporal = mkdtemp(dir="/var/tmp")
    
    try:
        # Iterar sobre el rango de años y meses
        for year in range(year_i, year_f + 1):
            for month in range(month_i, month_f + 1):
                month_str = f"{month:02d}"  # Asegurar formato de dos dígitos
                carpeta = os.path.join(directorio_principal, f"{filename}.{year}.{month_str}")  
                archivo_grib = os.path.join(carpeta, "data.grib")   # Si los archivos .grib del interior de las distintas carpetas tienen un nombre distinto a "data.grib", cambialo por el nombre que tengan
                archivo_nc = os.path.join(directorio_temporal, f"{filename}.{year}.{month_str}.nc")

                # Verificar si el archivo .grib existe y procesarlo
                if os.path.isfile(archivo_grib): 
                    subprocess.run(["cdo", "-f", "nc", "copy", archivo_grib, archivo_nc], check=True)
                    print(f"Procesando archivo: {archivo_grib}")
                else:
                    print(f"Archivo no encontrado: {archivo_grib}")

        # Verificar si hay archivos .nc temporales antes de combinar
        archivos_nc = [os.path.join(directorio_temporal, f) for f in os.listdir(directorio_temporal) if f.endswith(".nc")]
        if archivos_nc:
            archivo_salida = f"{filename}.{year_i}-{year_f}.nc" # Puedes cambiar el nombre del archivo final que te devolverá en el directorio ejecutado todo los "data.grib" transformados a un sólo archivo .nc final.
            subprocess.run(["cdo", "mergetime", *archivos_nc, archivo_salida], check=True)
            print(f"Archivos combinados en: {archivo_salida}")
        else:
            print("No se encontraron archivos para combinar.")

    finally:
        # Eliminar el directorio temporal
        shutil.rmtree(directorio_temporal)

if __name__ == "__main__":
    main()
