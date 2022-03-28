# SE4GI_project
 Repo for project in POLIMI course 

# Dependancies: 
* Flask
* bokeh
* geopandas
* requests
* geopy
* descartes
* seaborn
* contextily
* folium
* geoalchemy2 
* jmcmurray json
* anaconda psycopg2

## Instalation guide

A - this creates an empty environment called "se4g" (If you have it from the course, it is the same)
    
    conda config --add channels conda-forge
    conda create -n se4g python=3.9

B - activate the environment called "se4g"
    
    conda activate se4g

N.B. for Mac/Linux users -> source activate se4g #if this does not work, have a look 
[here](https://stackoverflow.com/questions/60050929/how-to-open-conda-shell-in-mac).
You can alternatively activate the Anaconda Prompt from the Anaconda Navigator

C - this will install almost all the geo libraries you will need (see: https://anaconda.org)

    conda install -c conda-forge geopandas
    conda update --all

D - let's add the interpreter platforms to "se4g" environment (Spyder and Jupyter Lab)

    conda install -c conda-forge spyder jupyterlab

E - some other libraries that can be used

    conda install -c conda-forge geopy descartes seaborn contextily requests folium flask bokeh git geoalchemy2 
    conda install -c jmcmurray json
    conda install -c anaconda psycopg2

# Some notes just for fun: 

Write welcome in your language below: 

Välkommen!

Välkommen!

مرحباً
