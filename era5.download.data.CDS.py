# Que sucede. / Titulo.
## Puedes modificar para obtener diferentes propiedades de los archivos descargados.
### Valores conectados, si cambias un valor, debes cambiar como minimo otro valor en otro lugar del codigo. Por ejemplo, si cambias z en una línea, hay otra línea que depende de z, por lo que si modificas uno, debes modificar el otro valor correspondiente.

import cdsapi
import os
import zipfile

def download_era5_data(variable, years, months, days, times, grid, area, file_prefix, download_path, data_format="grib", download_format="zip"):
    # Construir la solicitud de los datos
    request = {
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
    client.retrieve("reanalysis-era5-land", request).download(file_name)
    print(f"Datos descargados: {file_name}\n")
    return file_name

def compress_to_single_archive(output_file, files):
    with zipfile.ZipFile(output_file, 'w') as archive:
        for file in files:
            archive.write(file, os.path.basename(file))  # Agregar el archivo al ZIP
    print(f"Archivos comprimidos en: {output_file}")

# Parámetros comunes
months = ["01", "02", "03", 
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

grid = [2.5, 2.5]  ## grid = [x, y] --> Obtienes datos con una resolucion de "x" x "y"
area = [90, -180, 0, 180]  ## [N, W, S, E]

# Ruta de descarga personalizada
download_path = "./downloads"  ## Cambia esta ruta para ubicar la descarga

# Variables que se pueden cambiar
variables = ["total_precipitation"]  ## variables = ["v"] --> descarga datos de la variable "v" para los años, meses, dias y horas indicados
years_range = range(1980, 2023, 1)  ## range(x, y, n) --> Empieza desde "x" y hasta "y", con intervalos de "n" años (va de "n" en "n" años)
                                    ### si cambias n

# Opción para elegir cómo descargar: mes a mes o todo el año
download_by_month = True  ## download_by_month = logic --> Cambiar "logic" a "False" para descargar todo el año en una sola solicitud o cambiar a "True" para descargar mes a mes

# Lista para almacenar los archivos descargados
downloaded_files = []

# Descargar datos por años y meses
for start_year in years_range:
    end_year = start_year + 0  ### end_year = start_year + z --> z = n-1
    years = [str(year) for year in range(start_year, end_year + 1)]
    
    if download_by_month:
        # Descarga mes a mes
        for month in months:  # Iterar sobre los meses
            file_prefix = f"era5.p.1000hPa.day.{years[0]}.{month}"  # Un solo año
            for variable in variables:
                downloaded_file = download_era5_data(variable, years, [month], days, times, grid, area, file_prefix, download_path)
                downloaded_files.append(downloaded_file)  # Guardar el nombre del archivo descargado
    else:
        # Descargar todo el año
        file_prefix = f"era5.p.1000hPa.day.{years[0]}"
        for variable in variables:
            downloaded_file = download_era5_data(variable, years, months, days, times, grid, area, file_prefix, download_path)
            downloaded_files.append(downloaded_file)  # Guardar el nombre del archivo descargado

# Comprimir todos los archivos en un único archivo
if len(years_range) == 1:
    total_years = f"{years_range.start}"  # Un solo año
else:
    total_years = f"{years_range.start}-{years_range.stop - 1}"  # Rango de años

output_file = os.path.join(download_path, f"era5_data_{total_years}.zip")
compress_to_single_archive(output_file, downloaded_files)
