# SE4GI_project

Repo for project in POLIMI course

Documents can be found on the in the "DocumentationFiles" folder

# Guide to run the project:

## Python setup

First, clone this repository to you local machine. Open it in an editor that can run both
python and javascript. We recoment Visual Studio Code. 

Make sure you have an active python environment that contains all dependancies listed below. 
Keep in mind that if you are using the se4g python environment you need to add flask-cors and 
overpy.

    conda install flask-cors overpy

You also need to make sure that you have a working postgres instalation with a database called 
"SE4G".

## Node setup for Nuxt. 

Now, check if you have npm (node package manager - like conda for JS) installed and install it
if not. Instructions can be found [here](https://docs.npmjs.com/cli/v7/configuring-npm/install).
We recomend that you get the latest version, but we will have to manage node versions later. 

Then, make sure you have installed node version manager NVM (instructions can be found [here](https://dev.to/skaytech/how-to-install-node-version-manager-nvm-for-windows-10-4nbi))
, or "n" if you are on mac. It will be used to switch node versions. You will also need yarn,
which does the same as npm, but works better with the template.

If you have mac, run these commands in the terminal

    //Check if n is installed:
    n --verison
    //Install n:
    sudo npm install -g n
    //install yarn:
    sudo npm install -g yarn

    //Once n and yarn is installed, navigate to the /flaskVueFrontend folder and run: 
    cd flaskVueFrontend

    //Change node version to 12.13
    sudo n 12.13

If you are using windows, open a command promt as administrator and run this to install yarn: 
    //install yarn:
    npm install -g yarn

## Running the project

Now you have all prerequisits, time to run things. Start by going into the initDB.py file and
edit the variables MYUSER, MYPWRD and MYPORT to fit your postgres instalation. Then run initDB. 
This initializes the database on your machine and makes sure you have the correct tables.

Then, go into app.py and make the same edit to the variables MYUSER, MYPWRD and MYPORT at the
top of the file. Then run the app.py file. Now you should see something like "running on
[http://127.0.0.1:5000](http://127.0.0.1:5000). If so, the flask app is started successfully. 

For running the nuxt app, open a new terminal window and navigate to the folder 
flaskVueFrontend. write:

    yarn install

And accept to install the project. Then type: 
    
    yarn dev

This should rin the project at [localhost:3000](http://localhost:3000)

## Full list of dependancies:

### Python:

- Flask
- requests
- psycopg2
- flask-cors
- overpy

### Node

All dependancies can be found in the package.json file in the flaskVueFrontend folder. 

## Instalation instructions for se4g environment: 

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

    conda install flask-cors overpy

# Some notes just for fun:

Write welcome in your language below:

Välkommen!

Välkommen!

مرحباً
