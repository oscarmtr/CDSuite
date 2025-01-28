# Copernicus Climate Data Store Suite (CDSuite)
Repositorio de herramientas para la obtención y gestión de datos de CDS. La principal herramienta consiste en la modificación del API de Copernicus Climate Data Store (CDS) para obtener secuencias de datos evitando las restricciones por la limitación de solicitud de descarga de datos simultáneos, seguidos de programas para facilitar su gestión.

## Cómo usar
- Con la modificación del API **"DataDownload.py"** podrás configurar bajo que parámetros y que información solicitas a CDS.
- Con **"merge_grib_month.py"** podrás, una vez completada la descarga de los datos desde CDS por mes, procesar automáticamente los archivos. El script seleccionará todos los archivos .zip, extraerá los archivos "data.grib" de cada uno, te permitirá realizar distintas operaciones con Climate Data Operators (CDO) para porcesar los datos y los consolidará todos en un único archivo .nc, listo para su uso. Este script funcionará solo para archivos con este formato de escala temporal: era5.v.ht.form.YYYY.MM p. ej.: "era5.z.10hPa.day.1980.01".
- Con **"merge_grib_year.py"** harás lo mismo que con **"merge_grib_month.py"** pero para datos anuales con **n > 1**, es decir, este script funcionará solo para archivos con este formato de escala temporal: era5.v.ht.form.YYYY-YYYY p. ej.: "era5.z.10hPa.day.1980-1981", "era5.z.10hPa.hour.1980-1982"...

 
 Cada script está preconfigurado a modo de ejemplo.

## Objetivo
El objetivo de esta modificación consiste en no tener que estar pendiente de hacer una solicitud cada vez que se descargue un archivo para una serie de datos tan grande como para que CDS no te deje descargar.
Aun así, dependinedo de la variable y la escala temporal que necesites, deberás de probar cual es la cantidad de años, meses, días y horas que CDS te permite solicitar simultaneamente, y en función de la escala permitida, configurar el .py para obtener los datos.

## Justificación
Esta modificación nace de que cuando quise descargar los datos de precipitación total desde 1980 a 2023 para todos los meses, todos los días y todas las horas de una vez, me devolvía un error de que habia superado el límite de tamaño de solicitud, por lo que tras probar con cual era el límite permitido (normalmente son las opciones simultáneas máximas que te deja seleccionar en la interfaz gráfica de descarga de datos de CDS) terminé de configurar el .py para que descargara todos los datos sin la necesidad de estar cerca del ordenador para solicitarle otra serie de datos cada vez que terminase la anterior. 

## A tener en cuenta
- No se recomienda variar la estructura del nombre del archivo con el fin de evitar posibles errores.
     -   *era5.v.ht.form.YYYY-YYYY*
     -    *era5.v.ht.form.YYYY.MM* 
- Es posible que haya algunas líneas que debas modificar para obtener lo que quieras.
-    No es una versión definitiva y es posible que existan fallos no detectados.
