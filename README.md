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

D - let's add the interpreter platforms to "se4g" environment (Spyder and Jupyter Lab)

    conda install -c conda-forge spyder jupyterlab

E - some other libraries that can be used

    conda install -c conda-forge geopy descartes seaborn contextily requests folium flask bokeh git geoalchemy2
    conda install -c jmcmurray json
    conda install -c anaconda psycopg2

then, the aditional modules specific to our project are needed:

    conda install flask-cors

### Node

Begin by checking if you have npm (node package manager - like conda for JS) installed and install it if not. Instructions can be found
[here](https://docs.npmjs.com/cli/v7/configuring-npm/install)

Once npm is installed, navigate to the /flaskVueFrontend folder and run

    npm install

this will install all dependancies listed in the project. See below. 

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
- json
- psycopg2
- flask-cors

### Node

Begin by checking if you have npm (node package manager - like conda for JS) installed and install it if not. Instructions can be found
[here](https://docs.npmjs.com/cli/v7/configuring-npm/install). Below instalation process works for node v.16.15 which is the Long term stable release.

Then, make sure you have installed "n", which is a Node Version Manager. It will be used to switch node versions.
You will also need yarn, which does the same as npm, but works with the template.

Run these commands in the terminal

    //Check if n is installed:
    n --verison
    //Install n:
    sudo npm install -g n
    //install yarn:
    sudo npm install -g yarn

Once n and yarn is installed, navigate to the /flaskVueFrontend folder and run

    //Change node version to 12.13
    sudo n 12.13
    yarn install

this will install all dependancies listed in the project. See below for list of dependancies.
Run the project by typing:

    yarn dev

This should rin the project at [localhost:3000](http://localhost:3000)

# Some notes just for fun:

Write welcome in your language below:

Välkommen!

Välkommen!

مرحباً
