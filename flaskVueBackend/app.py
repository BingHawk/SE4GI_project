from flask import Flask, jsonify, request, redirect, flash, url_for, session, g
from flask_cors import CORS
import psycopg2
import requests
from werkzeug.security import check_password_hash, generate_password_hash
#from werkzeug.exceptions import abort
from historical import getMonthData, getYearData

#### GLOBAL VARIABLES
MYUSER = 'postgres'
MYPWRD = 'blod'
MYPORT = '5432'

#### FLASK CONFIGURATION
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["APPLICATION_ROOT"] = "/"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#### UNROUTED FUNCTIONS
def get_cityNames():

    r=requests.get("https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/cities?limit=1000&page=1&offset=0&sort=asc&country=IT&order_by=city")

    citiesname=[]
    cityDict = {} # Maps recapitalized city names to their original caputalization. 
    # print(r.json()['results'][0])
    # return r.json()
    for result in r.json()['results']:
        try:
            if result['city'] != "unused": #Filtering out the "unused" value that exist in the API. 
                cityname = result['city'].title() #Forcing one capitalization policy
                if cityname in cityDict.keys(): # Filling the cityDict with lists, as there are sometimes two endpint entries per city. 
                    cityDict[cityname].append(result['city'])
                else: 
                    cityDict[cityname] = [result['city']]
                # print(result['city'])
        except KeyError:
            continue
        if cityname not in citiesname: #Avoiding adding duplicates
            citiesname.append(cityname)
    response = {'cities': citiesname}
    return response, cityDict


# cityDict keys: ['Alessandria', 'Alfonsine', 'Ancona', 'Arezzo', 'Ascoli Piceno', 'Asti', 'Avellino', 'Bari', 'Barletta-Andria-Trani', 'Belluno', 'Benevento', 'Bergamo', 'Biella', 'Bologna', 'Bolzano/Bozen', 'Brescia', 'Brindisi', 'Cagliari', 'Campobasso', 'Carbonia-Iglesias', 'Carpi', 'Caserta', 'Catanzaro', 'Cento', 'Cesena', 'Chiesanuova', 'Civitavecchia', 'Colorno', 'Como', 'Cosenza', 'Cremona', 'Crotone', 'Cuneo', 'Faenza', 'Ferrara', 'Fiorano Modenese', 'Firenze', 'Foggia', "Forli'", "Forli'-Cesena", 'Frosinone', 'Genova', 'Grosseto', 'Guastalla', 'Imola', 'Imperia', 'Jolanda Di Savoia', 'Langhirano', "L'Aquila", 'La Spezia', 'Latina', 'Lecce', 'Lecco', 'Livorno', 'Lodi', 'Lucca', "Lugagnano Val D'Arda", 'Macerata', 'Mantova', 'Massa-Carrara', 'Matera', 'Mezzani', 'Milano', 'Mirandola', 'Modena', 'Molinella', 'Monza E Della Brianza', 'Napoli', 'Novara', 'Nuoro', 'Olbia-Tempio', 'Oristano', 'Ostellato', 'Padova', 'Parma', 'Pavia', 'Perugia', 'Pesaro E Urbino', 'Pescara', 'Piacenza', 'Pisa', 'Pistoia', 'Porretta Terme', 'Potenza', 'Prato', 'Ravenna', 'Reggio Di Calabria', "Reggio Nell'Emilia", 'Rieti', 'Rimini', 'Roma', 'Rovigo', 'Salerno', 'San Clemente', 'San Lazzaro Di Savena', 'San Leo', 'Sassari', 'Sassuolo', 'Savignano Sul Rubicone', 'Savona', 'Siena', 'Sogliano Al Rubicone', 'Sondrio', 'Sorbolo', 'Taranto', 'Teramo', 'Terni', 'Torino', 'Trento', 'Treviso', 'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli', 'Verona', 'Verucchio', 'Vibo Valentia', 'Vicenza', 'Villa Minozzo', 'Viterbo']
def getCityCoords():

    cityString = ""
    for city in cityDict.keys():
        city = city.replace("'","''")
        cityString += "'{}',".format(city)
    cityString += cityString[0:-1]

    query = "SELECT * FROM city WHERE city_name in ({});".format(cityString)

    conn = psycopg2.connect(
    database="SE4G", user = MYUSER, password= MYPWRD, host='localhost', port= MYPORT
    )

    c = conn.cursor()
    c.execute(query)
    res = c.fetchall()
    conn.commit()
    conn.close()

    # Format: cityCoords['city_name'] = [longitude, latitude]
    # The format can be changed through the loop below
    cityCoords = {} 
    for result in res:
        cityCoords[result[1]] = [result[2],result[3]]
    
    return cityCoords

#### PRE FLASK CODE (code that needs to run before flask server starts)
print("starting setup")

cityResponse, cityDict = get_cityNames()
cityCoords = getCityCoords()

print("setup complete")


#### ROUTED FUNCTIONS THAT SEND COORDINATES
@app.route('/api/locations', methods=["GET"])
def get_locations():
    # the endpoint of meassuring stations in italy
    italyEndpoint = "https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/locations?limit=10000&page=1&offset=0&sort=desc&radius=10000&country_id=it&order_by=lastUpdated&dumpRaw=false"
    
    # Get the stations
    r = requests.get(italyEndpoint)

    locations = []
    print(r.json()['results'][0])
    for result in r.json()['results']:
        try:
            location = {'id': result['id'], 'coordinates': [result['coordinates']['longitude'], result['coordinates']['latitude']]}
        except KeyError:
            continue
        locations.append(location)
    
    response = jsonify({'locations': locations})

    return response

# Returns latest value for every city.
@app.route('/api/latest', methods=["GET"])
def get_latest():
    #endpoint for latest values of meassuring stations in italy
    latestEndpoint = 'https://api.openaq.org/v2/latest?limit=1000&page=1&offset=0&sort=desc&radius=1000&country_id=IT&order_by=lastUpdated&dumpRaw=false'
    
    #get values
    r = requests.get(latestEndpoint)
    
    locations = {}
    for result in r.json()['results']:
        if result['city'] == None:
            continue
        else:
            city = result['city']
        if city in locations.keys():
            for particle in locations[city]['particles']:
                for particle_in in result['measurements']:
                    if particle['parameter'] == particle_in['parameter']:
                        if isinstance(particle['value'], list):
                            particle['value'].append(particle_in['value'])
                        else:
                            particle['value'] = [particle['value']]
                            particle['value'].append(particle_in['value'])
        else:
            locations[city] = {'cityName': city, 'particles': result['measurements']}       
        
    for city in locations.keys():
        for particle in locations[city]['particles']:
            if isinstance(particle['value'], list):
               n = len(particle['value'])
               mean_l = sum(particle['value'])/n
               particle['value'] = mean_l  

    for city in getCityCoords().keys():
            coords = getCityCoords()
            locations[city] = {'cityName': city, 'coordinates': coords[city], 'particles': result['measurements']}
               
    locations = list(locations.values())
    response = {'locations': locations}
        
    return jsonify(response)

#### ROUTED FUNCTIONS THAT DOES NOT SEND COORDINATES
    
#EndPoint for the cities
@app.route('/api/cities', methods = ['GET']) # Moved the actual API call to another function to be able to reuse get_cityNames() elsewhere. 
def serve_cityNames():
    return jsonify(cityResponse)

# the average as well as the parameters work finally!
@app.route('/api/cities/<cityname>', methods=["GET"])
def get_cities(cityname):
    try:
        cityname = cityDict[cityname.title()][0]
    except KeyError:
        return "City {} does not exist in database".format(cityname.title()), 400

    cityEndpoint =f"https://api.openaq.org/v2/locations?limit=15&page=1&offset=0&sort=desc&radius=1000&country_id=IT&city={cityname}&order_by=lastUpdated&dumpRaw=false"
    # Get the stations
    parameters=[]
    r = requests.get(cityEndpoint)
    parNO2, paro3, parco, parso2, parpm10, parpm25, parbc, parpm1, parnox, parch4, parufp, parno, parco2, parum010, parum025, parum100, parpm4 = ([] for i in range(17))
    for result in r.json()['results']:
        cityName = result['city']   
        id=result['id']
        lastUpdate=result['lastUpdated']
        for value in result['parameters']:
            print(value['parameter'])
            print(value['lastValue'])
            if value['parameter']== 'no2':
                parNO2.append(value['lastValue'])
            elif value['parameter']== "o3":
                paro3.append(value['lastValue'])
            elif value['parameter']== "co":
                parco.append(value['lastValue'])
            elif  value['parameter']== "so2":
                parso2.append(value['lastValue'])
            elif  value['parameter']== "pm10":
                parpm10.append(value['lastValue'])
            elif  value['parameter']== "pm25":
                parpm25.append(value['lastValue'])
            elif  value['parameter']== "bc":
                parbc.append(value['lastValue'])
            elif  value['parameter']== "pm1":
                parpm1.append(value['lastValue'])
            elif  value['parameter']== "nox":
                parnox.append(value['lastValue'])
            elif  value['parameter']== "ch4":
                parch4.append(value['lastValue'])
            elif  value['parameter']== "ufp":
                parufp.append(value['lastValue'])
            elif  value['parameter']== "no":
                parno.append(value['lastValue'])
            elif  value['parameter']== "co2":
                parco2.append(value['lastValue'])
            elif  value['parameter']== "um010":
                parum010.append(value['lastValue'])
            elif  value['parameter']== "um025":
                parum025.append(value['lastValue'])
            elif  value['parameter']== "um100":
                parum100.append(value['lastValue'])
            elif  value['parameter']== "pm4":
                parpm4.append(value['lastValue'])
            else:
                print('new parameter')
    d={"no2":parNO2, "o3":paro3, "co":parco, "so2":parso2, "pm10":parpm10, "pm25":parpm25, "bc":parbc, "pm1":parpm1, "nox":parnox , "ch4":parch4, "ufp":parufp , "no":parno, "co2":parco2 , "um010":parum010 , "um025":parum025 , "um100":parum100 , "pm4":parpm4}
    for key, item in d.items():
        try:
            average= sum(item)/len(item)         
        except ZeroDivisionError:
            average= None
        parametr = {'particleName': key,  'unit': 	"µg/m³" , 'value': average}
        parameters.append(parametr)
    city={'id':id,'city':cityName , 'lastUpdate':lastUpdate,'Measurements':parameters }
    response = jsonify({'cities': city})
    return response  

@app.route('/api/month/<city>', methods = ['GET'])
def serveMonthData(city):
    try:
        city = cityDict[city.title()][0]
    except KeyError:
        return "City {} does not exist in database".format(city.title()), 400
    
    res = getMonthData(city)
    return jsonify(res)

@app.route('/api/year/<city>', methods = ['GET'])
def serveYearData(city):
    try:
        city = cityDict[city.title()][0]
    except KeyError:
        return "City {} does not exist in database".format(city.title()), 400

    res = getYearData(city)
    return jsonify(res)

#### ROUTED FUNCTIONS FOR LOGIN
# This is the current endpoint used by the login function.
# It will recive a post request with the payload: {"username": <String>, "password": <String>}'
# It should check if that username exist in the database and if it has the specified password. 
# It should return the following JSON: {"user": {"username": <String>, userID: <Int>|<None>}, "access": <Boleean>}
# Where userID is the id of the user in the db, and None if authentication fails. Access bolean is true if access is granted, else false.
# Feel free to change above scheme of the return, but tell the people working on the frontend if you do!
@app.route('/api/authenticate', methods = ['POST'])
def authenticate():
    print("Authenticate recieved request")
    return "Authenticate recieved"

# This is the current endpoint used by the register function.
# It will recive a post request with the payload: {"username": <String>, "password": <String>}'
# It should check if that username exist in the database and if not register it together with the password 
# It should return the following JSON: {"user": {"username": <String>, userID: <Int>|<None>},"register": <Boleean>}
# Where userID is the id of the user in the db generated when adding, and None if username allready exist. Access bolean is true if register is sucsessful, else false.
# Feel free to change above scheme of the return, but tell the people working on the frontend if you do!
@app.route('/api/register', methods = ['POST'])
def register():
    print("Register recieved request")
    return "Register recieved"

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'123'

def get_dbConn():
    if 'dbConn' not in g:
        myConn = 'dbname=5432 user=postgres password=blod'
        connStr = myConn
        g.dbConn = psycopg2.connect(connStr)
    
    return g.dbConn

def close_dbConn():
    if 'dbConn' in g:
        g.dbComm.close()
        g.pop('dbConn')

@app.route('/register', methods=('GET', 'POST')) # make POST request with curl (need front end data, the curl sends a request)
def register():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['user_password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else :
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
            'SELECT user_id FROM users WHERE user_name = %s', (username,)) ##  'SELECT user_id FROM blog_user WHERE user_name = %s', (username,))
            if cur.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
                cur.close()

        if error is None:
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (user_name, user_password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            response = cur.fetchall() #guess
            cur.close()
            conn.commit()
            return redirect(url_for('login'))

        flash(error)

        
        return jsonify(response) #render_template('auth/register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        #curl -X POST -H "Content-Type: application/json" \ -d '{"username": "user", "password": "pass"}' \ http://127.0.0.1:5000/register \
        #curl -X POST -F 'name=user' -F 'password=passw' http://127.0.0.1:5000/register
        #curl -X POST -d "userId=5&title=Hello World&body=Post body." http://127.0.0.1:5000/register
        #curl -i -X POST -H 'Content-Type: application/json' -d '{"name": "user", "password": "passw"}' http://127.0.0.1:5000/register

        username = request.form['username']
        password = request.form['password']
        conn = get_dbConn()
        cur = conn.cursor()
        error = None
        cur.execute(
            'SELECT * FROM users WHERE user_name = %s', (username,) 
        )
        user = cur.fetchone()
        cur.close()
        conn.commit()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)
        
        response = cur.fetchall() #guess
        return jsonify(response) #render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('register'))


def load_logged_in_user():
    username = session.get('user_name')

    if username is None:
        g.user = None
    else:
        conn = get_dbConn()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM users WHERE user_name = %s', (username,)
        )
        g.user = cur.fetchone()
        cur.close()
        conn.commit()
    if g.user is None:
        return False
    else: 
        return True

#### RUNNING FLASK IN DEV MODE
if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)