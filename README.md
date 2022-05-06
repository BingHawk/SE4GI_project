# SE4GI_project

Repo for project in POLIMI course

Documents can be found on the [google drive here](https://drive.google.com/drive/u/0/folders/1-qme17xkIi_KhyNxs10YBTd-44utuKoX)

# Dependancies:

## Instalation guide

### Python:

First, the se4g python environment is needed. Install it through conda like this

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

D - (Not necessary - VS Code is better!) let's add the interpreter platforms to "se4g" environment (Spyder and Jupyter Lab)

    conda install -c conda-forge spyder jupyterlab

E - some other libraries that can be used

    conda install -c conda-forge geopy descartes seaborn contextily requests folium flask bokeh git geoalchemy2
    conda install -c jmcmurray json
    conda install -c anaconda psycopg2

then, the aditional modules specific to our project are needed:

    conda install flask-cors

### Node

Begin by checking if you have npm (node package manager - like conda for JS) installed and install it if not. Instructions can be found
[here](https://docs.npmjs.com/cli/v7/configuring-npm/install). Below instalation process works for node v.16 but not for version v.17. 
Curently looking for a fix so it works with both!

Once npm is installed, navigate to the /flaskVueFrontend folder and run

    npm install

this will install all dependancies listed in the project. See below for list of dependancies. 

## Full list of dependancies:

### Python:

- Flask
- bokeh
- geopandas
- requests
- geopy
- descartes
- seaborn
- contextily
- folium
- geoalchemy2
- jmcmurray json
- anaconda psycopg2
- flask-cors

### Node:

full list of dependancies can be found in this file:
    
    /flaskVueFrontend/package.json
    {"name": "flaskVueFrontend",
    ...
    "dependancies":
    //Dependancies listed here 
    ...
    }


# Some notes just for fun:

Write welcome in your language below:

Välkommen!

Välkommen!

مرحباً
