import requests
import datetime as dt

import time

def getCityNames():

    # r=requests.get("https://u50g7n0cbj.execute-api.us-east-1.amazonaws.com/v2/cities?limit=1000&page=1&offset=0&sort=asc&country=IT&order_by=city")
    r=requests.get("https://api.openaq.org/v2/cities?limit=1000&page=1&offset=0&sort=asc&country_id=IT&order_by=city")

    cityNames=[]
    # print(r.json()['results'][0])
    # return r.json()
    for result in r.json()['results']:
        try:
            if result['city'] in ['unused', 'Civitavecchia', 'Colorno', 'Verucchio', 'Villa Minozzo']: 
                continue # Filtering out the "unused" value that exist in the API and some cities without data
            if result['city'].upper() == result['city']: # Filtering out capitalized cities since there is no data on them
                continue # Filtering out capitalized cities since there is no data on them
            cityname = result['city']
            # print(result['city'])
        except KeyError:
            continue
        if cityname not in cityNames: #Avoiding adding duplicates
            cityNames.append(cityname)
    return cityNames

def get_locations():
    # the endpoint of meassuring stations in italy
    italyEndpoint = "https://api.openaq.org/v2/latest?limit=10000&page=1&offset=0&sort=desc&radius=1000&country_id=it&order_by=lastUpdated&dumpRaw=false"
    
    # Get the stations
    r = requests.get(italyEndpoint)
    locations = []
    for result in r.json()['results']:
        try:
            if result['coordinates'] is None:
                continue
            location = {
                'location': result['location'],
                'cityName': result['city'], # Not correct, this is the name of the station. 
                'coordinates': [result['coordinates']['longitude'],result['coordinates']['latitude']],
                'particles': [],
                }
            for parameter in result['measurements']:
                particle = {
                    'parameter': parameter['parameter'],
                    'value': parameter['value'],
                    'unit': parameter['unit'],
                    'lastUpdated': parameter['lastUpdated'], # string with datetime format from openAQ. ex: '2022-05-25T12:02:59+00:00'
                }
                location['particles'].append(particle)
        except KeyError:
            continue
        locations.append(location)

    return {'locations': locations}

def get_latest(cityCoords):
    #endpoint for latest values of meassuring stations in italy
    latestEndpoint = 'https://api.openaq.org/v2/latest?limit=1000&page=1&offset=0&sort=desc&radius=1000&country_id=IT&order_by=lastUpdated&dumpRaw=false'
    
    #get values
    r = requests.get(latestEndpoint)

    try: 
        results = r.json()['results']
    except KeyError:
        print(r.json())
        return "something went wrong"
    
    locations = {}
    for result in results:
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
        
    return {'locations': locations}

def get_cities(cityname):

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
    d={
        "no2":parNO2, 
        "o3":paro3, 
        "co":parco, 
        "so2":parso2, 
        "pm10":parpm10, 
        "pm25":parpm25, 
        "bc":parbc, 
        "pm1":parpm1,
        "nox":parnox,
        "ch4":parch4, 
        "ufp":parufp, 
        "no":parno, 
        "co2":parco2, 
        "um010":parum010, 
        "um025":parum025,
        "um100":parum100, 
        "pm4":parpm4
        }
    for key, item in d.items():
        try:
            average= round(sum(item)/len(item),2)       
        except ZeroDivisionError:
            average= None
        parametr = {'parameter': key,  'unit': 	"µg/m³" , 'value': average}
        parameters.append(parametr)
    city={'id':id,'cityName':cityName , 'lastUpdated':lastUpdate,'Measurements':parameters }
    
    return {'city': city} 

def queryByDay(startDay, endDay, city):
    inFormat = "%Y-%m-%dT%H%%3A%M%%3A%S" # Format to build query string
    utcFormat = "%Y-%m-%dT%H:%M:%S+00:00" # Format recieved from openAQ 

    paramUnits= {}
    res = {}

    qTimes = []
    aTimes = []
    # print("Querying day {}".format(iter+1),end="\r")

    startDayString = startDay.strftime(inFormat)+"%2B00%3A00"
    endDayString = endDay.strftime(inFormat)+"%2B00%3A00"
    url = f"https://api.openaq.org/v2/measurements?date_from={endDayString}&date_to={startDayString}&limit=5000&page=1&offset=0&sort=desc&radius=1000&city={city}&order_by=datetime"
    # print(url)

    r = requests.get(url)
    resJson = r.json()


    # If an empty page is recieved, goes on to next day. 
    if not resJson['results']:
        return res, paramUnits

    # Target format: 
    # res = {
    #     dateTime: {
    #         param1: {n: int, sum: float}
    #         param2:{n: int, sum: float}
    #         ...
    #         },{
    #         day2 = datetime,
    #         param1: {n: int, sum: float}
    #         param2:{n: int, sum: float}
    #         ...
    #        }, 
    #    }
    # }
    for result in resJson['results']:
        day = dt.datetime.strptime(result['date']['utc'],utcFormat).replace(hour=0,minute=0,second=0)

        if day not in res.keys():
            res[day] = {}

        param = result['parameter']
        if param in res[day]:
            res[day][param]['n'] += 1
            res[day][param]['sum'] += result['value']
        else:
            res[day][param] = {'n':1,'sum':result['value']}
        
        if param not in paramUnits:
            paramUnits[param] = result['unit']

    return res, paramUnits

#Timed version of above for performance testing
def queryByDayTimed(startDay, endDay, city):
    inFormat = "%Y-%m-%dT%H%%3A%M%%3A%S" # Format to build query string
    utcFormat = "%Y-%m-%dT%H:%M:%S+00:00" # Format recieved from openAQ 

    paramUnits= {}
    res = {}

    qTimes = []
    aTimes = []
    # print("Querying day {}".format(iter+1),end="\r")
    qTic = time.perf_counter()
    startDayString = startDay.strftime(inFormat)+"%2B00%3A00"
    endDayString = endDay.strftime(inFormat)+"%2B00%3A00"
    url = f"https://api.openaq.org/v2/measurements?date_from={endDayString}&date_to={startDayString}&limit=5000&page=1&offset=0&sort=desc&radius=1000&city={city}&order_by=datetime"
    # print(url)

    r = requests.get(url)
    resJson = r.json()

    # When an empty page is recieved, goes on to next day. 
    # try : 
    #     if not resJson['results']:
    #         break
    # except KeyError:
    #     break

    qToc = time.perf_counter()
    qTime = qToc-qTic
    qTimes.append(qTime)

    # When an empty page is recieved, goes on to next day. 
    if not resJson['results']:
        qTime = sum(qTimes)/len(qTimes)
        try: 
            aTime = sum(aTimes)/len(aTimes)
        except ZeroDivisionError:
            aTime = None

        return res, paramUnits

    aTic = time.perf_counter()
    # Target format: 
    # res = {
    #     dateTime: {
    #         param1: {n: int, sum: float}
    #         param2:{n: int, sum: float}
    #         ...
    #         },{
    #         day2 = datetime,
    #         param1: {n: int, sum: float}
    #         param2:{n: int, sum: float}
    #         ...
    #        }, 
    #    }
    # }
    for result in resJson['results']:
        day = dt.datetime.strptime(result['date']['utc'],utcFormat).replace(hour=0,minute=0,second=0)

        if day not in res.keys():
            res[day] = {}

        param = result['parameter']
        if param in res[day]:
            res[day][param]['n'] += 1
            res[day][param]['sum'] += result['value']
        else:
            res[day][param] = {'n':1,'sum':result['value']}
        
        if param not in paramUnits:
            paramUnits[param] = result['unit']
    
    aToc = time.perf_counter()
    aTime = aToc-aTic
    aTimes.append(aTime)


    qTime = sum(qTimes)/len(qTimes)
    try: 
        aTime = sum(aTimes)/len(aTimes)
    except ZeroDivisionError:
        aTime = None
        

    return res, paramUnits, qTime, aTime