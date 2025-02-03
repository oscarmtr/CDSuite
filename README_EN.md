# Copernicus Climate Data Store Suite (CDSuite)  
Repository of tools for obtaining and managing data from the Copernicus Climate Data Store (CDS). The main tool consists of modifying the CDS API to obtain data sequences while avoiding restrictions due to the limitation on simultaneous data download requests. It also includes additional programs to facilitate data management.  

## How to Use  
First, **request** and **download** are treated as separate actions, where **request** refers to the amount of data you ask from Copernicus servers, which is subject to a predefined limit. Depending on the requested amount, it may be accepted or denied. Meanwhile, **download** refers to obtaining data directly from an already accepted **request**, and this process has no limitations. In other words, to obtain data, the **requested** information must be below the maximum **request** limit so that it can be **downloaded**. This limit must be determined through trial and error until you find a valid amount to configure the **request** and finally obtain the data.  

- By modifying the API with **`DataDownload.py`**, you can configure the parameters and information you want to request and download from CDS.  
- With **`merge_grib_month.py`**, once the data download from CDS is completed on a monthly basis, you can automatically process the files. The script will select all `.zip` files, extract the `data.grib` files from each one, allow you to perform various operations using Climate Data Operators (CDO) to process the data, and consolidate everything into a single `.nc` file, ready for use. This script will work only for files with this **temporal** scale format: *era5.v.ht.form.**YYYY.MM*** e.g., `"era5.z.10hPa.day.1980.01"`.  
- With **`merge_grib_year.py`**, you will perform the same operations as **`merge_grib_month.py`**, but for annual data with **`n > 1`**, meaning that this script will work only for files with this **temporal** scale format: *era5.v.ht.form.**YYYY-YYYY*** e.g., `"era5.z.10hPa.day.1980-1981"`, `"era5.z.10hPa.hour.1980-1982"`...  

Each script is preconfigured as an example.  

## Objective  
The goal of this modification is to eliminate the need to manually make a request every time a file is downloaded for a dataset too large for CDS to allow downloading at once.  
However, depending on the variable and the temporal scale required, you will need to test the maximum number of years, months, days, and hours that CDS allows you to request simultaneously. Based on the permitted scale, you can configure the `.py` script to obtain the data.  

## Justification  
This modification arose when I attempted to download total precipitation data from 1980 to 2023, including all months, all days, and all hours at once. I received an error indicating that the request limit had been exceeded. After testing to determine the allowed limit (which usually corresponds to the maximum simultaneous options available in the CDS graphical download interface), I configured the `.py` script to download all the data without needing to be near the computer to manually request another data batch after each one was completed.  

## Considerations  
- It is not recommended to change the structure of the file name to avoid possible errors.  
     - *era5.v.ht.form.YYYY-YYYY*  
     - *era5.v.ht.form.YYYY.MM*  
- Some lines may need to be modified to obtain the desired results.  
- This is not a final version, and undetected errors may exist.  

## References  
- Contains modified Copernicus Climate Change Service information 2024. Neither the European Commission nor ECMWF is responsible for any use that may be made of the Copernicus information or data it contains. [CDS API Documentation](https://cds.climate.copernicus.eu/how-to-api)  
- Schulzweida, Uwe. (2023). CDO User Guide (2.3.0). Zenodo. [DOI: 10.5281/zenodo.10020800](https://doi.org/10.5281/zenodo.10020800)  
