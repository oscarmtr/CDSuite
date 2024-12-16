# API Copernicus Climate Data Store (CDS)
Modificacion del API de Copernicus Climate Data Store (CDS) para obtener secuencia de datos evitando las restricciones por la limitación de descarga.

## Objetivo
El objetivo de esta modificación consiste en no tener que estar pendiente de hacer una solicitud cada vez que se descargue un archivo para una serie de datos tan grande como para que CDS no te deje descargar.
Aun así, dependinedo de la variable y la escala temporal que necesites, deberás de probar cual es la cantidad de años, meses, días y horas que CDS te permite solicitar simultaneamente, y en función de la escala permitida, configurar el .py para obtener los datos.

## Justificación
Esta modificación nace de que cuando quise descargar los datos de precipitación total desde 1980 a 2023 para todos los meses, todos los días y todas las horas de una vez, me devolvía un error de que habia superado el límite de tamaño de solicitud, por lo que tras probar con cual era el límite permitido (normalmente son las opciones simultáneas máximas que te deja seleccionar en la interfaz gráfica de descarga de datos de CDS) terminé de configurar el .py para que descargara todos los datos sin la necesidad de estar cerca del ordenador para solicitarle otra serie de datos cada vez que terminase la anterior. 

## A tener en cuenta
- Actualmente está configurado para la variable de precipitación total, para obtener otra variable la buscaría en el API generado al final de la interfaz gráfica de selección de datos para sustituirla.

- Es posible que haya algunas líneas que no estan señaladas como modificables y que si se pueda como la de selección de variable y la de cambiar el nombre con el que se guardan cada archivo descargado antes de comprimirse (si es que fuera necesario).

- Si descargas datos mensuales mes a mes en cada .zip, al final, una vez descarga todos los meses se comprimirán en otro .zip con el título del año corespondiente a esos meses.

- En el script existe una jerarquía de #, en función del número de # del código, hará referencia a unas indicaciones u otras.

### Notas
No es una versión definitiva y es posible que existan fallos no detectados.
