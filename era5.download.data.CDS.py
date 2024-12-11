import cdsapi

def download_era5_data(variable, years, months, days, times, grid, area, file_prefix, data_format="grib", download_format="zip"):
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
    
    # Generar el nombre del archivo basado en el prefijo y las fechas solicitadas
    file_name = f"{file_prefix}.zip"
    
    # Descargar los datos
    client.retrieve("reanalysis-era5-land", request).download(file_name)
    print(f"Datos descargados: {file_name}")

# Parámetros comunes
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
        "00:00", "12:00"
]
grid = [2.5, 2.5]
area = [90, -180, 0, 180] # [N, W, S, E]

# Variables que se pueden cambiar
variables = ["total_precipitation"]
years_range = range(1980, 2023, 3)  # Empieza desde 1980 y hasta 2023, con intervalos de 3 (n=3) años

# Llamar a la función para cada grupo de años
for start_year in years_range:
    end_year = start_year + 2 # si quiero un intervalo distinto a n=3 necesito sumar aqui, en vez de + 2, sumar + (n-1)
    years = [str(year) for year in range(start_year, end_year + 1)]
    file_prefix = f"era5.p.1000hPa.day.{years[0]}.{years[-1]}"
    for variable in variables:
        download_era5_data(variable, years, months, days, times, grid, area, file_prefix)
