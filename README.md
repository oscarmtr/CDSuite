[![cdsuite1](https://github.com/user-attachments/assets/b240a777-e22a-4c77-8e44-96a41789845b)](https://github.com/oscarmtr/CDSuite)
[![license1](https://github.com/user-attachments/assets/2c3dba82-5de0-4ed5-9e0d-88a470f0d586)](https://www.gnu.org/licenses/agpl-3.0.html)
[![doi1](https://github.com/user-attachments/assets/51caa891-c1f7-4f34-be4c-0d31eb9b9831)](https://doi.org/10.5281/zenodo.14570087)

<!--[![cdsuite](https://github.com/user-attachments/assets/4c9698da-5b13-4981-a376-df23b5d376a2)](https://github.com/oscarmtr/CDSuite)
[![license](https://github.com/user-attachments/assets/f58a7dee-3fdd-414f-b179-9fa4c134150d)](https://www.gnu.org/licenses/agpl-3.0.html)
[![doi](https://github.com/user-attachments/assets/81be1084-ae2c-40ec-bdb9-3b84f1e84fa9)](https://doi.org/10.5281/zenodo.14570087)-->

# Copernicus Climate Data Store Suite (CDSuite)
Repositorio de herramientas para la obtención y gestión de datos de Copernicus Climate Data Store (CDS). La principal herramienta consiste en la modificación del API de CDS para obtener secuencias de datos evitando las restricciones por la limitación de solicitud de descarga de datos simultáneos. También incluye programas adicionales para facilitar la gestión de estos datos.

## Cómo usar
En primer lugar, **solicitud** y **descarga** se tratan como acciones distintas, donde **solicitud** es la cantidad de datos que le pides a los servidores de Copernicus, la cual está limitada a una cantidad determinada, y en función de la cantidad que solicites, puede ser aceptada o denegada. Mientras, **descarga**, es la obtención de datos directamente, la cual no tiene ninguna limitación, que figuran en la **solicitud** que ha sido previamente aceptada. Es decir, para poder obtener los datos, es necesario que la información que vas a **solicitar**, esté por debajo del límite máximo de **solicitud** para poder ser **descargada**. Este límite deberás encontrarlo mediante prueba y error, hasta que consigas una cantidad válida para configurar la **solicitud** y obtener finalmente los datos.

- Con la modificación del API **`DataDownload.py`** podrás configurar los parámetros e información que deseas solicitar y descargar a CDS.
- Con **`merge_grib_month.py`** podrás, una vez completada la descarga de los datos desde CDS por mes, procesar automáticamente los archivos. El script seleccionará todos los archivos .zip, extraerá los archivos `data.grib` de cada uno, te permitirá realizar distintas operaciones con Climate Data Operators (CDO) para procesar los datos y los consolidará todos en un único archivo .nc, listo para su uso. Este script funcionará solo para archivos con este formato de escala **temporal**: *era5.v.ht.form.**YYYY.MM*** p. ej.: "era5.z.10hPa.hour.1980.01".
- Con **`merge_grib_year.py`** harás lo mismo que con **`merge_grib_month.py`** pero para datos anuales, es decir, este script funcionará solo para archivos con este formato de escala **temporal**: *era5.v.ht.form.**YYYY-YYYY*** p. ej.: "era5.z.10hPa.hour.1980-1981", "era5.z.10hPa.day.1980-1982"...

Cada script está preconfigurado a modo de ejemplo.

## Objetivo
El objetivo de esta modificación consiste en no tener que estar pendiente de hacer una solicitud cada vez que se descargue un archivo para una serie de datos tan grande como para que CDS no te deje descargar.
Aun así, dependiendo de la variable y la escala temporal que necesites, deberás probar cuál es la cantidad de años, meses, días y horas que CDS te permite solicitar simultáneamente, y en función de la escala permitida, configurar el .py para obtener los datos.

## Justificación
Esta modificación nace de que cuando quise descargar los datos de precipitación total desde 1980 a 2023 para todos los meses, todos los días y todas las horas de una vez, me devolvía un error indicando que había superado el límite de solicitud, por lo que tras probar con cual era el límite permitido (normalmente son las opciones simultáneas máximas que te deja seleccionar en la interfaz gráfica de descarga de datos de CDS) terminé de configurar el .py para que descargara todos los datos sin la necesidad de estar cerca del ordenador para solicitarle otra serie de datos cada vez que terminara la anterior. 

## A tener en cuenta
- No se recomienda variar el orden de la estructura del nombre del archivo con el fin de evitar posibles errores.
     - *era5.v.ht.form.YYYY-YYYY*
     - *era5.v.ht.form.YYYY.MM* 
- Es posible que haya algunas líneas que debas modificar para obtener lo que quieras.
- No es una versión definitiva y es posible que existan fallos no detectados.

## Referencias
- Contains modified Copernicus Climate Change Service information 2024. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains. https://cds.climate.copernicus.eu/how-to-api
- Schulzweida, Uwe. (2023). CDO User Guide (2.3.0). Zenodo. https://doi.org/10.5281/zenodo.10020800
