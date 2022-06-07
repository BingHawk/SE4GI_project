from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
#from werkzeug.exceptions import abort
from process import getMonthData, getYearData, getCityCoords
from queries import *

#### GLOBAL VARIABLES
MYUSER = 'postgres'
MYPWRD = 'qrC85Ba9Dpg'
MYPORT = '5432'

#### FLASK CONFIGURATION
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["APPLICATION_ROOT"] = "/"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#### PRE FLASK CODE (code that needs to run before flask server starts)
class Cache:
    def __init__(self):

        self.cityNames = getCityNames()
        self.cityCoords = getCityCoords(self.cityNames, MYUSER, MYPWRD, MYPORT)

print("Starting setup")
Cache = Cache()
print("Setup complete")


#### ROUTED FUNCTIONS THAT SEND COORDINATES
@app.route('/api/locations', methods=["GET"])
def serve_locations():
    response = get_locations()
    return jsonify(response)


@app.route('/api/latest', methods=["GET"])
def serve_latest():
    response = get_latest(Cache.cityCoords)
    return jsonify(response)


#### ROUTED FUNCTIONS THAT DOES NOT SEND COORDINATES
@app.route('/api/cities', methods = ['GET']) # Moved the actual API call to another function to be able to reuse getCityNames() elsewhere. 
def serve_cityNames():
    return jsonify({'cities':Cache.cityNames})


@app.route('/api/cities/<cityname>', methods=["GET"])
def serve_cities(cityname):
    cityName = cityname.title()
    if cityName not in Cache.cityNames:
        return "City {} does not exist in database".format(cityName), 400
    
    response = get_cities(cityName)
    return jsonify(response) 


@app.route('/api/month/<city>', methods = ['GET'])
def serveMonthData(city):
    if city.title() in Cache.cityNames:
        res = getMonthData(city.title())
        return jsonify(res)
    else:
        return "City {} does not exist in database".format(city.title()), 400

@app.route('/api/year/<city>', methods = ['GET'])
def serveYearData(city):
    if city.title() in Cache.cityNames:
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
def authenticate():
    if request.method == 'POST' :
        data = request.get_json()
        try:
            username= data['username']
            password = data['password']
        except KeyError:
            return "Wrong input", 400
        #The authentication
        #Checking whether he is already in the DB|registered
        else :
            conn = psycopg2.connect(
            database="SE4G", user = MYUSER, password= MYPWRD, host='localhost', port= MYPORT
            )
            cur = conn.cursor()
            cur.execute(
            'SELECT user_id FROM users WHERE user_name = %s AND user_password= %s', (username, password))
            # The user is registered then is verified
            if cur.fetchone() is not None:
                cur.execute(
                'SELECT * FROM users WHERE user_name = %s AND user_password= %s', (username, password))
                res= cur.fetchone()
                responde= {
                    "user": {
                                "username": res[1],
                                "userID": res[0],
                             },
                    "access": True,
                    "lastSearch": res[3]
                    }
                print('the user is being verified to be registered, hence it has been authenticated')
                print("Authenticate recieved")
                cur.close()
            # If he is not registered then the authentication fails    
            else:
                responde={
                    "user": {
                                "username": None,
                                "userID": None,
                             },
                    "access": False,
                    "lastSearch": None
                    }
                print('the user is not being verified to be registered, hence it has to register first')
                print("Authenticate not being granted")
                # cur.execute(

            conn.commit()
            conn.close()
    # flash(error)
    return jsonify(responde)   

    # print("Authenticate recieved request")
    # return "Authenticate recieved"

# This is the current endpoint used by the register function.
# It will recive a post request with the payload: {"username": <String>, "password": <String>}'
# It should check if that username exist in the database and if not register it together with the password 
# It should return the following JSON: {"user": {"username": <String>, userID: <Int>|<None>},"register": <Boleean>}
# Where userID is the id of the user in the db generated when adding, and None if username allready exist. Access bolean is true if register is sucsessful, else false.
# Feel free to change above scheme of the return, but tell the people working on the frontend if you do!

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'123'

@app.route('/api/register', methods= ['POST'])
def register():
    data = request.get_json()
    try:
        username= data['username']
        password = data['password']
    except KeyError:
        return "Wrong input", 400

    conn = psycopg2.connect(
    database="SE4G", user = MYUSER, password= MYPWRD, host='localhost', port= MYPORT
    )
    cur = conn.cursor()
    try:
        cur.execute(f"INSERT INTO users (user_name,user_password) VALUES ('{username}','{password}') RETURNING user_id;")

        output= {
        'user':{
            'user_id': cur.fetchone()[0],
            'username': username,
        },
        'register': True
        }  
    except psycopg2.errors.UniqueViolation:
        print("not a new username")
        output= {
        'user':{
            'user_id': None,
            'username': username,
        },
        'register': False
        }

    conn.commit()
    conn.close()
    return jsonify(output)    

@app.route('/api/logout', methods= ['POST'])
def logout():
    #log info from /api/cities, får data från front end med POST
    data = request.get_json()
    #expected to get these json-files from front end
    try:
        username= data['username']
        lastsearch = data['lastsearch']
    except KeyError:
        return "Wrong input", 400


    conn = psycopg2.connect(
            database="SE4G", user = MYUSER, password= MYPWRD, host='localhost', port= MYPORT
            )
    cur = conn.cursor()

    cur.execute(f"UPDATE users SET last_search = '{lastsearch}' WHERE user_name = '{username}'")
    conn.commit()
    cur.execute(f"SELECT user_id FROM users WHERE user_name = '{username}'")
    error = {
            'user':{
                'user_id': cur.fetchone()[0],
                'username': username
                },
            'saved': bool(id)}  
    print(error)         
    conn.commit()
    conn.close()


    #returns boolean to see if operation was succesful (if the last search was stored in the database)
    return jsonify(error)

#### RUNNING FLASK IN DEV MODE
if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)
