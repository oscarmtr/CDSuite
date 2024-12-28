#!/bin/bash

# Directorio principal
directorio_principal="/home/oscar/Escritorio/era5.p.1000hPa.day.1980-2023"

# Directorio temporal para almacenar los archivos .nc
directorio_temporal=$(mktemp -d --tmpdir=/var/tmp)

# Rango de años y meses
for ano in {1980..2023}; do
  for mes in {01..12}; do
    # Construye el nombre de la carpeta
    carpeta="$directorio_principal/era5.p.1000hPa.day.$ano.$mes"

    # Construye la ruta al archivo .grib dentro de la carpeta
    archivo_grib="$carpeta/data.grib"

    # Construye el nombre del archivo .nc
    archivo_nc="$directorio_temporal/era5.p.1000hPa.day.$ano.$mes.nc"

    # Verifica si el archivo .grib existe y lo procesa
    if [ -f "$archivo_grib" ]; then
      cdo -f nc copy "$archivo_grib" "$archivo_nc"
      echo "Procesando archivo: $archivo_grib"
    else
      echo "Archivo no encontrado: $archivo_grib"
    fi
  done
done

# Combina todos los archivos .nc en uno solo
cdo mergetime "$directorio_temporal/*.nc" "era5_1980_2023.nc"

# Elimina el directorio temporal
rm -rf "$directorio_temporal"
