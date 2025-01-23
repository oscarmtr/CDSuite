import cdsapi
import os
import zipfile


###### Inicio configura tu descarga ######
dataset = "reanalysis-era5-pressure-levels"

product_type = ["reanalysis"]

variables = ["geopotential"]  # variables = ["v"] --> descarga datos de la variable "v" para los años, meses, dias y horas indicados

# Selecciona el rango del tiempo, descargaras datos desde year_i hasta year_f, cada archivo generado, contendra un total de n años del rango seleccionado.
year_i = 1980 # Año de inicio de la solicitud (incluido)
year_f = 2023 # Año de fin de la solicitud (incluido)
n = 2 # De cuanto en cuantos años realizas la solicitud

# Selecciona el resto de parametros y añadelos, modificalos o eliminalos segun tus necesidades, ten en cuenta que tambien deberas cambiar los parámetros en el resto del script 
months = [
    "01", "02", "03", 
    "04", "05", "06", 
    "07", "08", "09", 
    "10", "11", "12"
]

days = [
    "01", "02", "03", 
    "04", "05", "06", 
    "07", "08", "09", 
    "10", "11", "12", 
    "13", "14", "15", 
    "16", "17", "18", 
    "19", "20", "21", 
    "22", "23", "24", 
    "25", "26", "27", 
    "28", "29", "30", 
    "31"
]

times = [
    "00:00", "01:00", "02:00",
    "03:00", "04:00", "05:00",
    "06:00", "07:00", "08:00",
    "09:00", "10:00", "11:00",
    "12:00", "13:00", "14:00",
    "15:00", "16:00", "17:00",
    "18:00", "19:00", "20:00",
    "21:00", "22:00", "23:00"
]

pressure_level = [
   "10"
    ]

grid = [2.5, 2.5]  # grid = [x, y] --> Obtienes datos con una resolucion de "x" x "y"
area = [90, -180, -90, 180]  # [N, W, S, E]
datas_format = "grib"
downloads_format = "zip" # Deberias dejarlo asi

# Selecciona si cada archivo corresponderá a un mes o a un año
download_by_month = True  # download_by_month = logic --> Cambiar "logic" a "False" para descargar todo el año en una sola solicitud o cambiar a "True" para solicitar mes a mes

# Ruta de descarga personalizada
download_path = "./downloads/era5.ght.10hPa"  # download_path = /home/user/"./directorio1/directorio1.1/" --> Cambia esta ruta para ubicar la descarga del archivo dentro del directorio del user

# Nombra como se llamara al archivo descargado hasta la seccion del rango temporal
filename = "era5.10hPa.day" # Teniendo esto en cuenta, el archivo final se llamaria asi: era5.10hPa.day.1980.01.zip o era5.10hPa.day.1980.zip, segun las opciones seleccionadas

###### Fin configura tu descarga ######



def download_era5_data(product_type, pressure_level, variable, years, months, days, times, grid, area, file_prefix, download_path, data_format=datas_format, download_format=downloads_format):
    # Construir la solicitud de los datos
    request = {
        "product_type": product_type,
        "pressure_level": pressure_level,
        "variable": [variable],
        "year": years,
        "month": months,
        "day": days,
        "time": times,
        "grid": grid,
        "data_format": data_format,
        "download_format": download_format,
        "area": area
    }

    # Crear el cliente de CDS API
    client = cdsapi.Client()

    # Generar la ruta completa del archivo
    file_name = os.path.join(download_path, f"{file_prefix}.zip")
    os.makedirs(download_path, exist_ok=True)  # Crear la carpeta si no existe

    # Descargar los datos
    client.retrieve(dataset, request).download(file_name)
    print(f"Datos descargados: {file_name}\n")
    return file_name

def compress_to_single_archive(output_file, files):
    with zipfile.ZipFile(output_file, 'w') as archive:
        for file in files:
            archive.write(file, os.path.basename(file))  # Agregar el archivo al ZIP
    print(f"Archivos comprimidos en: {output_file}")
                                 
# Lista para almacenar los archivos descargados
downloaded_files = []

# Generar un rango completo de años
years_list = list(range(year_i, year_f + 1))

# Descargar datos por años y meses
for i in range(0, len(years_list), n):
    # Crear un subconjunto de años del tamaño `n`
    years = [str(year) for year in years_list[i:i + n]]

    if download_by_month:
        # Descarga mes a mes
        for year in years:
            for month in months:
                # Usar el año y el mes actuales para el nombre del archivo
                file_prefix = f"{filename}.{year}.{month}"   # Cambia el nombre del archivo descargado
                for variable in variables:
                    downloaded_file = download_era5_data(
                        product_type, pressure_level, variable, [year], [month], days, times, grid, area, file_prefix, download_path
                    )
                    downloaded_files.append(downloaded_file)  # Agregar el archivo descargado a la lista
    else:
        # Descargar todo el bloque de años
        # Usar el rango de años para el nombre del archivo
        start_year = years[0]
        end_year = years[-1]
        file_prefix = f"{filename}.{start_year}-{end_year}"   # Cambia el nombre del archivo descargado
        for variable in variables:
            downloaded_file = download_era5_data(
                product_type, pressure_level, variable, years, months, days, times, grid, area, file_prefix, download_path
            )
            downloaded_files.append(downloaded_file)  # Agregar el archivo descargado a la lista
