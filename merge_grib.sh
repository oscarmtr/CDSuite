# Directorio principal
directorio_principal="/home/usuario/directorio/directorio_era5.tp.1000hPa.day.1980-2023"  ## Directorio que contiene a las distintas carpetas que contienen los respectivos "data.grib"

# Directorio temporal para almacenar los archivos .nc
directorio_temporal=$(mktemp -d --tmpdir=/var/tmp)

# Rango de años y meses
for ano in {1980..2023}; do  ## Si vas a unir otro periodo de años cambia este rango en función de lo que vayas a usar
  for mes in {01..12}; do  ## Si vas a unir otro periodo de meses cambia este rango en función de lo que vayas a usar
    # Construye el nombre de la carpeta
    carpeta="$directorio_principal/era5.tp.1000hPa.day.$ano.$mes"  ## Si el nombre de las carpetas que continen los archivos .grib es distinto a este esquema o tiene otra variable, cambialo

    # Construye la ruta al archivo .grib dentro de la carpeta
    archivo_grib="$carpeta/data.grib"  ## Si los archivos .grib del interior de las distintas carpetas tienen un nombre distinto a "data.grib", cambialo por el nombre que tengan

    # Construye el nombre del archivo .nc
    archivo_nc="$directorio_temporal/era5.tp.1000hPa.day.$ano.$mes.nc"

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
cdo mergetime "$directorio_temporal/*.nc" "era5.tp.1000hPa.day.1980.2023.nc"  ## Puedes cambiar el nombre del archivo final que te devolverá en el directorio ejecutado todo los "data.grib" transformados a un sólo archivo .nc final.

# Elimina el directorio temporal
rm -rf "$directorio_temporal"
