from flask import Flask, jsonify, request
from flask_cors import CORS

from process import *
from queries import *
from user import *

#### GLOBAL VARIABLES
MYUSER = 'postgres'
MYPWRD = '123456'
MYPORT = '5433'

#### FLASK CONFIGURATION
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["APPLICATION_ROOT"] = "/"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#### CACHE CLASS
class Cache:
    def __init__(self):

        self.cityNames = getCityNames()
        self.cityCoords = getCityCoords(self.cityNames, MYUSER, MYPWRD, MYPORT)


#### ROUTED FUNCTIONS THAT SEND COORDINATES
@app.route('/api/locations', methods=["GET"])
def serve_locations():
    print("getting locations")
    response = get_locations()
    return jsonify(response)


@app.route('/api/latest', methods=["GET"])
def serve_latest():
    print("getting latest")
    response = get_latest(Cache.cityCoords)
    return jsonify(response)


#### ROUTED FUNCTIONS THAT DOES NOT SEND COORDINATES
@app.route('/api/cities', methods = ['GET']) # Moved the actual API call to another function to be able to reuse getCityNames() elsewhere. 
def serve_cityNames():
    print("getting cityNames")
    return jsonify({'cities':Cache.cityNames})


@app.route('/api/cities/<cityname>', methods=["GET"])
def serve_cities(cityname):
    cityName = cityname.title()
    if cityName not in Cache.cityNames:
        return "City {} does not exist in database".format(cityName), 400
    print("getting data for",cityName)

    response = get_cities(cityName)
    return jsonify(response) 


@app.route('/api/month/<city>', methods = ['GET'])
def serveMonthData(city):
    if city.title() in Cache.cityNames:
        print("Querying month data for",city.title())
        res = getMonthData(city.title())
        return jsonify(res)
    else:
        return "City {} does not exist in database".format(city.title()), 400

@app.route('/api/year/<city>', methods = ['GET'])
def serveYearData(city):
    if city.title() in Cache.cityNames:
        print("Querying year data for",city.title())
        res = getYearData(city.title())
        return jsonify(res)
    else:
        return "City {} does not exist in database".format(city.title()), 400

#### ROUTED FUNCTIONS FOR LOGIN

# This is the current endpoint used by the login function.
# It will recive a post request with the payload: {"username": <String>, "password": <String>}'
# It should check if that username exist in the database and if it has the specified password. 
# It should return the following JSON:  
# Where userID is the id of the user in the db, and None if authentication fails. Access bolean is true if access is granted, else false.
# Feel free to change above scheme of the return, but tell the people working on the frontend if you do!
@app.route('/api/authenticate', methods = ['POST'])
def serve_authResult():
    data = request.get_json()
    try:
        username= data['username']
        password = data['password']
        print("Handling authenticate request for",username)
        result = authenticate(username, password, MYUSER, MYPWRD, MYPORT)
        return jsonify(result)
    except KeyError:
        return "Wrong input", 400

# This is the current endpoint used by the register function.
# It will recive a post request with the payload: {"username": <String>, "password": <String>}'
# It should check if that username exist in the database and if not register it together with the password 
# It should return the following JSON: {"user": {"username": <String>, userID: <Int>|<None>},"register": <Boleean>}
# Where userID is the id of the user in the db generated when adding, and None if username allready exist. Access bolean is true if register is sucsessful, else false.

@app.route('/api/register', methods= ['POST'])
def serve_regResult():
    data = request.get_json()
    try:
        username= data['username']
        password = data['password']
        print("Handling register request for",username)
        result = register(username, password, MYUSER, MYPWRD, MYPORT)
        return jsonify(result)
    except KeyError:
        return "Wrong input", 400  

@app.route('/api/logout', methods= ['POST'])
def serve_logoutResult():
    data = request.get_json()
    try:
        username= data['username']
        lastsearch = data['lastsearch']
        print("Handling logout request for",username)
        result = logout(username, lastsearch, MYUSER, MYPWRD, MYPORT)
        return jsonify(result)
    except KeyError:
        return "Wrong input", 400

# ROUTED FUNCTIONS FOR RETRIEVING THE DATA FOR THE CONTACT US PAGE
@app.route('/api/contact', methods=["GET"])
def serve_contactsInfo():
    print("getting contact info")
    info = getContactInfo(MYUSER, MYPWRD, MYPORT)
    return jsonify(info)


#### RUNNING FLASK IN DEV MODE
if __name__ == "__main__":

    print("Starting setup")
    Cache = Cache()
    print("Setup complete")
    app.run(debug=True,  use_reloader=False)
    # print(get_contactsInfo())
    # print(get_locations())
