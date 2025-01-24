# API Copernicus Climate Data Store (CDS)
Modificación del API de Copernicus Climate Data Store (CDS) para obtener secuencias de datos evitando las restricciones por la limitación de solicitud de descarga de datos simultáneos.

## Cómo usar
- Con **"DataDownload.py"** podras configurar bajo que parámetros y que información solicitas a CDS.
- Con **"merge_grib_month.py"** podrás, una vez completada la descarga de los datos desde CDS por mes y extraigas manualmente los archivos .grib de los .zip generados, procesar automáticamente los archivos. El script seleccionará todos las carpetas generadas por la extracción de los .zip, extraerá los archivos "data.grib" de cada una. Finalmente, consolidará todos los archivos "data.grib" en un único archivo .nc, listo para su uso. Este script funcionará solo para archivos con este formato: "era5.z.10hPa.day.1980.01".
- Con **"merge_grib_year.py"** harás lo mismo que con **"merge_grib_month.py"** pero para datos anuales con **n > 1**, es decir, este script funcionará solo para archivos con este formato: "era5.z.10hPa.day.1980-1981", "era5.z.10hPa.day.1980-1982"...

 
 Cada script está preconfigurado a modo de ejemplo.

## Objetivo
El objetivo de esta modificación consiste en no tener que estar pendiente de hacer una solicitud cada vez que se descargue un archivo para una serie de datos tan grande como para que CDS no te deje descargar.
Aun así, dependinedo de la variable y la escala temporal que necesites, deberás de probar cual es la cantidad de años, meses, días y horas que CDS te permite solicitar simultaneamente, y en función de la escala permitida, configurar el .py para obtener los datos.

## Justificación
Esta modificación nace de que cuando quise descargar los datos de precipitación total desde 1980 a 2023 para todos los meses, todos los días y todas las horas de una vez, me devolvía un error de que habia superado el límite de tamaño de solicitud, por lo que tras probar con cual era el límite permitido (normalmente son las opciones simultáneas máximas que te deja seleccionar en la interfaz gráfica de descarga de datos de CDS) terminé de configurar el .py para que descargara todos los datos sin la necesidad de estar cerca del ordenador para solicitarle otra serie de datos cada vez que terminase la anterior. 

## A tener en cuenta
- Es posible que haya algunas líneas que debas modificar para obtener lo que quieras.
-    No es una versión definitiva y es posible que existan fallos no detectados.
