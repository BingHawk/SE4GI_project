from flask import Flask, jsonify, request, flash
from flask_cors import CORS
import psycopg2
import requests
#from werkzeug.exceptions import abort
from historical import getMonthData, getYearData

#### GLOBAL VARIABLES
MYUSER = 'postgres'
MYPWRD = 'qrC85Ba9Dpg'
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
    for result in r.json()['results']:
        try:
            location = {
                'id': result['id'],
                'cityName': result['name'], # Not correct, this is the name of the station. 
                'coordinates': [result['coordinates']['longitude'],result['coordinates']['latitude']],
                'particles': []
                }
            for parameter in result['parameters']:
                particle = {
                    'particleName': parameter['displayName'],
                    'value': parameter['lastValue'],
                    'unit': parameter['unit'],
                    'lastUpdate': parameter['lastUpdated'], # string with datetime format from openAQ. ex: '2022-05-25T12:02:59+00:00'
                }
                location['particles'].append(particle)
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
            try:
                locations[city] = {'cityName': city,'coordinates': cityCoords[city.title()], 'particles': result['measurements']}
            except KeyError:
                continue #Not storing the data if we don't have coordinates for it

    for city in locations.keys():
        for particle in locations[city]['particles']:
            if isinstance(particle['value'], list):
               n = len(particle['value'])
               mean_l = sum(particle['value'])/n
               particle['value'] = round(mean_l,2) 

    locations = list(locations.values())
    response = {'locations': locations}
        
    return jsonify(response)

#### ROUTED FUNCTIONS THAT DOES NOT SEND COORDINATES
    
#EndPoint for the cities
@app.route('/api/cities', methods = ['GET']) # Moved the actual API call to another function to be able to reuse get_cityNames() elsewhere. 
def serve_cityNames():
    print(cityResponse)
    return jsonify(cityResponse)

# the average as well as the parameters work finally!
@app.route('/api/cities/<cityname>', methods=["GET"])
def get_city(cityname):
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
            average= round(sum(item)/len(item),2)       
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
# It should return the following JSON:  
# Where userID is the id of the user in the db, and None if authentication fails. Access bolean is true if access is granted, else false.
# Feel free to change above scheme of the return, but tell the people working on the frontend if you do!
@app.route('/api/authenticate', methods = ['POST'])
def authenticate():
    if request.method == 'POST' :
        data = request.get_json()
        print(data)
        username= data['username'] 
        password = data['password'] 
        print(username)
        print(password)
        # if the username isn't inserted
        if not username:
            error = 'Username is required.'
        # if the password isn't inserted
        elif not password:
            error = 'Password is required.'
        # if both are inserted
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
                    "access": True
                        }
                print('the user is being verified to be registered, hence it has been authenticated')
                print("Authenticate recieved")
                cur.close()
            # If he is not registered then the authentication fails    
            else:
                responde={
                    "access": False
                }
                print('the user is not being verified to be registered, hence it has to register first')
                print("Authenticate not being granted")
                # cur.execute(
                # 'INSERT INTO users (user_name, user_password) VALUES (%s, %s)',
                # (username, password)
                # )
                # access= cur.execute(
                #      'SELECT user_id FROM users WHERE users.user_name = %s AND users.user_password= %s', (username, password))
                # error= {
                #     'user':{
                #         'user_id': cur.fetchone()[0],
                #         'username': username,
                #     },
                #     'register': bool(access)
                # }
                # print('the user is not in the database and is being registered')
                # cur.close()
                # # conn.close()
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
    if request.method == 'POST' :
        data = request.get_json()
        # data['username']
        username= data['username'] 
        # = request.form['username']
        password = data['password'] 
        # request.form['password']
        # username = request.args.get("username")
        # password = request.args.get("password")
        print(username)
        print(password)
        # if the username isn't inserted
        if not username:
            error = 'Username is required.'
        # if the password isn't inserted
        elif not password:
            error = 'Password is required.'
        # if both password and username are inserted
        # Then checking weather the user is already in the DB|registered
        else :
            conn = psycopg2.connect(
            database="SE4G", user = MYUSER, password= MYPWRD, host='localhost', port= MYPORT
            )
            cur = conn.cursor()
            access= cur.execute(
            'SELECT user_id FROM users WHERE user_name = %s AND user_password= %s', (username, password)) #LEOs comment: You dont need to check if the user exist, postgres will do that itsalf when you do insert since username field is configured as unique. 
            # The user is already registered
            if cur.fetchone() is not None:
                # error = 'User {} is already registered.'.format(username)
                error= {
                    'user':{
                        'user_id': None,
                        'username': username,
                    },
                    'register': bool(access)
                } #LEOs comment: JSON structure seems coorect. 
                print('the user is already in the database')
                cur.close()
                # conn.close()
            else:
                cur.execute(
                'INSERT INTO users (user_name, user_password) VALUES (%s, %s)',
                (username, password)
                )
                access= cur.execute(
                     'SELECT user_id FROM users WHERE users.user_name = %s AND users.user_password= %s', (username, password))
                error= {
                    'user':{
                        'user_id': cur.fetchone()[0],
                        'username': username,
                    },
                    'register': bool(access)
                }
                print('the user is not in the database and is being registered')
                cur.close()
                # conn.close()
            conn.commit()
            conn.close()
    flash(error)
    return jsonify(error)    

@app.route('/api/logout', methods= ['POST'])
def logout():
    #log info from /api/cities, får data från front end med POST
    data = request.get_json()
    #expected to get these json-files from front end
    username= data['username']
    lastsearch = data['lastsearch']

    conn = psycopg2.connect(
            database="SE4G", user = MYUSER, password= MYPWRD, host='localhost', port= MYPORT
            )
    cur = conn.cursor()
    cur.execute(
                'INSERT INTO users (last_search) VALUES (%s)',
                (lastsearch))
    id= cur.execute(
                     'SELECT user_id FROM users WHERE users.user_name = %s', (username))
    error= {
            'user':{
                'user_id': cur.fetchone()[0],
                'username': username,
                'saved': bool(id)
                }}            
    conn.commit()
    conn.close()

    #returns boolean to see if operation was succesful (if the last search was stored in the database)
    return jsonify(error)

#### RUNNING FLASK IN DEV MODE
if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)
