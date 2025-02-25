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
filename = "era5.z.10hPa.hour"  # Nombra como se llama el archivo descargado/carpetas antes de la seccion del rango temporal
format = "hour" # Indica el formato de las datos, si se ha descargado por horas (hour), días...

# Operaciones CDO a realizar. 
## option = 1 -> copia y fusiona .grib a un unico .nc
## option = 2 -> calcula la media diaria y fusiona .grib a un unico .nc
## option = 3 -> calcula la media mensual y fusiona .grib a un unico .nc
## option = 4 -> calcula el sumatorio diario y fusiona .grib a un unico .nc
option = 1

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
                            if option == 1:
                                subprocess.run(["cdo", "-f", "nc", "copy", archivo_grib, archivo_nc], check=True)
                                print(f"Procesando archivo: {archivo_grib} de {archivo_zip}")
                            elif option == 2:
                                subprocess.run(["cdo", "-f", "nc", "daymean", archivo_grib, archivo_nc], check=True)
                                print(f"Procesando archivo: {archivo_grib} de {archivo_zip}")
                            elif option == 3:
                                subprocess.run(["cdo", "-f", "nc", "monmean", archivo_grib, archivo_nc], check=True)
                                print(f"Procesando archivo: {archivo_grib} de {archivo_zip}")
                            elif option == 4:
                                subprocess.run(["cdo", "-f", "nc", "daysum", archivo_grib, archivo_nc], check=True)
                                print(f"Procesando archivo: {archivo_grib} de {archivo_zip}") 
                            else:
                                 print("Elige un \033[3moption\033[0m valido entre 1 y 4")
                        else:
                            print(f"Archivo data.grib no encontrado en: {archivo_zip}")
                else:
                    print(f"Archivo ZIP no encontrado: {archivo_zip}")

        # Verificar si hay archivos .nc temporales
        archivos_nc = [os.path.join(directorio_temporal, f) for f in os.listdir(directorio_temporal) if f.endswith(".nc")]
        if archivos_nc:
            if option == 1:
                filename1 = filename
                filename1 = filename1.replace(format,"")
                archivo_salida1 = os.path.join(directorio_final, f"{filename1}hour.{year_i}-{year_f}.nc")
                subprocess.run(["cdo", "mergetime", *archivos_nc, archivo_salida1], check=True)
                print(f"Archivos combinados en: {archivo_salida1}")
            elif option == 2:
                filename2 = filename
                filename2 = filename2.replace(format,"")
                archivo_salida2 = os.path.join(directorio_final, f"{filename2}day.{year_i}-{year_f}.nc")
                subprocess.run(["cdo", "mergetime", *archivos_nc, archivo_salida2], check=True)
                print(f"Archivos combinados en: {archivo_salida2}")
            elif option == 3:
                filename3 = filename
                filename3 = filename3.replace(format,"")
                archivo_salida3 = os.path.join(directorio_final, f"{filename3}month.{year_i}-{year_f}.nc")
                subprocess.run(["cdo", "mergetime", *archivos_nc, archivo_salida3], check=True)
                print(f"Archivos combinados en: {archivo_salida3}")
            elif option == 4:
                filename4 = filename
                filename4 = filename4.replace(format,"")
                archivo_salida4 = os.path.join(directorio_final, f"{filename4}dailysum.{year_i}-{year_f}.nc")
                subprocess.run(["cdo", "mergetime", *archivos_nc, archivo_salida4], check=True)
                print(f"Archivos combinados en: {archivo_salida4}")
        else:
            print("No se encontraron archivos para combinar o revisa \033[3moption\033[0m, \033[3mformat\033[0m y el apartado \033[3m#Verificar si hay archivos .nc temporales#\033[0m del script.")

    finally:
        # Eliminar el directorio temporal
        shutil.rmtree(directorio_temporal)

if __name__ == "__main__":
    main()
