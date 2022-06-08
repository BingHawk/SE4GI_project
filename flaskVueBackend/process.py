import datetime as dt
import concurrent.futures
import psycopg2


from queries import queryByDay



# t = dt.datetime.now()
# now = t.replace(second = 0, minute = 0)
# oneMonthAgo = now - dt.timedelta(days = 30)
# oneYearAgo  = now - dt.timedelta(days = 365)

# dateformat = "%Y-%m-%dT%H:%M:%S"
# print(now.strftime(dateformat)+"+00:00")
# print(oneMonthAgo.strftime(dateformat)+"+00:00")
# print(now.strftime(dateformat)+"+00:00")

def getMonthData(city):
    days = 30
    t = dt.datetime.now()
    startDay = t.replace(second = 59, minute = 59, hour=23) # end of today the starting day of query

    with concurrent.futures.ProcessPoolExecutor() as executor: # Execute queries asyncronously
        futures = []
        for _ in range(days):
            endDay = startDay - dt.timedelta(days = 1)
            f = executor.submit(queryByDay, startDay, endDay, city)
            futures.append(f)
            startDay = endDay
        res = {}
        paramUnits = {}
        for future in concurrent.futures.as_completed(futures): # Gather results together as completed

            resDay, paramUnitsDay = future.result()
            res.update(resDay)
            paramUnits.update(paramUnitsDay)

    # Desired JSON scheme
    #  {
    # "time_month": {
    #     particle1: {
    #         "data": [day1, day2, ... day30],
    #         "unit":unit
    #         },
    #     particle2: {
    #         "data": [day1, day2, ... day30],
    #         "unit": unit
    #         }
    # }
        time_month = {}
        for param in paramUnits.keys():
            time_month[param] = {"data": [], "unit": paramUnits[param]}

            currentDay = endDay.replace(hour=0,minute=0,second=0,microsecond=0)# + dt.timedelta(days = 1)
            while currentDay != endDay.replace(hour=0,second=0,minute=0,microsecond=0) + dt.timedelta(days = days):
                currentDay = currentDay + dt.timedelta(days = 1)
                try:
                    avg = res[currentDay][param]['sum']/res[currentDay][param]['n']
                    time_month[param]['data'].append(round(avg,2))
                except KeyError:
                    # print("missing day: {} or parameter: {}".format(currentDay, param), end="\r")
                    time_month[param]['data'].append(None)
        
        return {"time_month":time_month}

def getYearData(city):
    days = 365
    t = dt.datetime.now()
    startDay = t.replace(second = 59, minute = 59, hour=23) # end of today the starting day of query

    with concurrent.futures.ProcessPoolExecutor() as executor: #Run queries asyncronously
        futures = []
        for _ in range(days):
            endDay = startDay - dt.timedelta(days = 1)
            f = executor.submit(queryByDay, startDay, endDay, city)
            futures.append(f)
            startDay = endDay
        res = {}
        paramUnits = {}
        for future in concurrent.futures.as_completed(futures): #Assmble results as the queries complete

            resDay, paramUnitsDay = future.result()
            res.update(resDay)
            paramUnits.update(paramUnitsDay)

    # Desired JSON scheme
    #  {
    # "time_month": {
    #     particle1: {
    #         "data": [day1, day2, ... day30],
    #         "unit":unit
    #         },
    #     particle2: {
    #         "data": [day1, day2, ... day30],
    #         "unit": unit
    #         }
    # }
        time_year = {}
        for param in paramUnits.keys():
            time_year[param] = {"data": [], "unit": paramUnits[param]}

            currentDay = endDay.replace(hour=0,minute=0,second=0,microsecond=0)
            currentWeek = currentDay.isocalendar().week
            weekSum = 0
            weekN = 0
            while currentDay != endDay.replace(hour=0,minute=0,second=0,microsecond=0) + dt.timedelta(days = days):
                currentDay = currentDay + dt.timedelta(days = 1)
                lastWeek = currentWeek
                currentWeek = currentDay.isocalendar().week
                if lastWeek == currentWeek:
                    # still in same week, just add upp the numbers
                    try:
                        weekSum += res[currentDay][param]['sum']
                        weekN += res[currentDay][param]['n']
                    except KeyError:
                        # print("missing day: {} or parameter: {}".format(currentDay, param), end="\r")
                        continue
                    pass
                else: 
                    # new week has started, add last weeks average to data
                    try: 
                        avg = round(weekSum / weekN,2)
                        time_year[param]['data'].append(avg)
                    except ZeroDivisionError:
                        #No meassurements in this week.
                        time_year[param]['data'].append(None)
                    try:
                        # Reset week counts
                        weekSum = res[currentDay][param]['sum']
                        weekN = res[currentDay][param]['n']
                    except KeyError:
                        # print("missing day: {} or parameter: {}".format(currentDay, param), end=("\r"))
                        weekSum = 0
                        weekN = 0
                    pass
            try: 
                avg = weekSum / weekN
                time_year[param]['data'].append(avg)
            except ZeroDivisionError:
                #No meassurements in this week.
                time_year[param]['data'].append(None)
            

        return {"time_year":time_year}

def getCityCoords(cityNames, *args):

    cityString = ""
    for city in cityNames:
        city = city.replace("'","''")
        cityString += "'{}',".format(city)
    cityString += cityString[0:-1]

    query = "SELECT * FROM city WHERE city_name in ({});".format(cityString)

    
    conn = psycopg2.connect(
    database="SE4G", user = args[0], password= args[1], host='localhost', port= args[2]
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


def getContactInfo(*args):
        # with app.app_context():
        #test code
            contactus=[]
            conn = psycopg2.connect(
                database="SE4G", user = args[0], password= args[1], host='localhost', port= args[2]
                )
            cur = conn.cursor()
            cur.execute('SELECT * FROM contacts')
            outcome=cur.fetchall()
            # print(outcome)
            for item in outcome:
                contact={ 'first_name': item[1].strip(), 'last_name':item[2].strip(), 'nationality':item[4].strip(), 'description':item[3].strip(), 'email':item[5].strip()}
                contactus.append(contact)
            # print(contactus)
            info={"contactus":contactus}
            # outcome2=jsonify(info)
            return info
def test():
    cityDict = {
        'Alessandria': ['Alessandria'],
        'Alfonsine': ['ALFONSINE'], #Fails
        'Ancona': ['Ancona'],
        'Arezzo': ['Arezzo'],
        'Ascoli Piceno': ['Ascoli Piceno'], 
        'Asti': ['Asti'],
        'Avellino': ['Avellino'],
        'Bari': ['Bari'],
        'Barletta-Andria-Trani': ['Barletta-Andria-Trani'],
        'Belluno': ['Belluno'],
        'Benevento': ['Benevento'],
        'Bergamo': ['Bergamo'], #Fails month
        'Biella': ['Biella'],
        'Bologna': ['Bologna', 'BOLOGNA'],
        'Bolzano/Bozen': ['Bolzano/Bozen'],
        'Brescia': ['Brescia'], #Fails month
        'Brindisi': ['Brindisi'],
        'Cagliari': ['Cagliari'],
        'Campobasso': ['Campobasso'],
        'Carbonia-Iglesias': ['Carbonia-Iglesias'],
        'Carpi': ['CARPI'], #Fails
        'Caserta': ['Caserta'],
        'Catanzaro': ['Catanzaro'],
        'Cento': ['CENTO'], #Fails
        'Cesena': ['CESENA'], #Fails
        'Chiesanuova': ['Chiesanuova'],
        'Civitavecchia': ['Civitavecchia'], #Fails
        'Colorno': ['COLORNO'], #Fails
        'Como': ['Como'], #Fails month
        'Cosenza': ['Cosenza'],
        'Cremona': ['Cremona'], #Fails month
        'Crotone': ['Crotone'],
        'Cuneo': ['Cuneo'],
        'Faenza': ['FAENZA'], #Fails
        'Ferrara': ['Ferrara', 'FERRARA'],
        'Fiorano Modenese': ['FIORANO MODENESE'], #Fails
        'Firenze': ['Firenze'],
        'Foggia': ['Foggia'],
        "Forli'": ["FORLI'"], #Fails
        "Forli'-Cesena": ["Forli'-Cesena"],
        'Frosinone': ['Frosinone'],
        'Genova': ['Genova'],
        'Grosseto': ['Grosseto'],
        'Guastalla': ['GUASTALLA'], #Fails
        'Imola': ['IMOLA'], #Fails
        'Imperia': ['Imperia'],
        'Jolanda Di Savoia': ['JOLANDA DI SAVOIA'], #Fails
        'Langhirano': ['LANGHIRANO'], #Fails
        "L'Aquila": ["L'Aquila"],
        'La Spezia': ['La Spezia'],
        'Latina': ['Latina'],
        'Lecce': ['Lecce'],
        'Lecco': ['Lecco'], #Fails month
        'Livorno': ['Livorno'],
        'Lodi': ['Lodi'], #Fails month
        'Lucca': ['Lucca'],
        "Lugagnano Val D'Arda": ["LUGAGNANO VAL D'ARDA"], #Fails
        'Macerata': ['Macerata'],
        'Mantova': ['Mantova'], #Fails month
        'Massa-Carrara': ['Massa-Carrara'],
        'Matera': ['Matera'],
        'Mezzani': ['MEZZANI'], #Fails
        'Milano': ['Milano'], #Fails month
        'Mirandola': ['MIRANDOLA'], #Fails
        'Modena': ['Modena', 'MODENA'],
        'Molinella': ['MOLINELLA'], #Fails
        'Monza E Della Brianza': ['Monza E Della Brianza'], #Fails month
        'Napoli': ['Napoli'],
        'Novara': ['Novara'],
        'Nuoro': ['Nuoro'],
        'Olbia-Tempio': ['Olbia-Tempio'],
        'Oristano': ['Oristano'],
        'Ostellato': ['OSTELLATO'], #Fails
        'Padova': ['Padova'],
        'Parma': ['Parma', 'PARMA'],
        'Pavia': ['Pavia'], #Fails month
        'Perugia': ['Perugia'],
        'Pesaro E Urbino': ['Pesaro E Urbino'],
        'Pescara': ['Pescara'],
        'Piacenza': ['Piacenza', 'PIACENZA'],
        'Pisa': ['Pisa'],
        'Pistoia': ['Pistoia'],
        'Porretta Terme': ['PORRETTA TERME'], #Fails
        'Potenza': ['Potenza'], 
        'Prato': ['Prato'], 
        'Ravenna': ['Ravenna', 'RAVENNA'], 
        'Reggio Di Calabria': ['Reggio Di Calabria'], 
        "Reggio Nell'Emilia": ["Reggio Nell'Emilia", "REGGIO NELL'EMILIA"], 
        'Rieti': ['Rieti'],
        'Rimini': ['Rimini', 'RIMINI'], 
        'Roma': ['Roma'], 
        'Rovigo': ['Rovigo'], 
        'Salerno': ['Salerno'], 
        'San Clemente': ['SAN CLEMENTE'], #Fails
        'San Lazzaro Di Savena': ['SAN LAZZARO DI SAVENA'], #Fails
        'San Leo': ['SAN LEO'], #Fails
        'Sassari': ['Sassari'], 
        'Sassuolo': ['SASSUOLO'], #Fails
        'Savignano Sul Rubicone': ['SAVIGNANO SUL RUBICONE'], #Fails
        'Savona': ['Savona'], 
        'Siena': ['Siena'], 
        'Sogliano Al Rubicone': ['SOGLIANO AL RUBICONE'], #Fails
        'Sondrio': ['Sondrio'], #Fails month
        'Sorbolo': ['SORBOLO'], #Fails
        'Taranto': ['Taranto'], 
        'Teramo': ['Teramo'], 
        'Terni': ['Terni'], 
        'Torino': ['Torino'], 
        'Trento': ['Trento'],
        'Treviso': ['Treviso'],
        'Varese': ['Varese'], #Fails month
        'Venezia': ['Venezia'],
        'Verbano-Cusio-Ossola': ['Verbano-Cusio-Ossola'], 
        'Vercelli': ['Vercelli'], 
        'Verona': ['Verona'], 
        'Verucchio': ['VERUCCHIO'], #Fails
        'Vibo Valentia': ['Vibo Valentia'], 
        'Vicenza': ['Vicenza'], 
        'Villa Minozzo': ['VILLA MINOZZO'], #Fails
        'Viterbo': ['Viterbo']}
    cityNames = ['Alessandria', 'Ancona', 'Arezzo', 'Ascoli Piceno', 'Asti', 'Avellino', 'Bari', 'Barletta-Andria-Trani', 'Belluno', 'Benevento', 'Bergamo', 'Biella', 'Bologna', 'Bolzano/Bozen', 'Brescia', 'Brindisi', 'Cagliari', 'Campobasso', 'Carbonia-Iglesias', 'Caserta', 'Catanzaro', 'Chiesanuova', 'Civitavecchia', 'Como', 'Cosenza', 'Cremona', 'Crotone', 'Cuneo', 'Ferrara', 'Firenze', 'Foggia', "Forli'-Cesena", 'Frosinone', 'Genova', 'Grosseto', 'Imperia', "L'Aquila", 'La Spezia', 'Latina', 'Lecce', 'Lecco', 'Livorno', 'Lodi', 'Lucca', 'Macerata', 'Mantova', 'Massa-Carrara', 'Matera', 'Milano', 'Modena', 'Monza E Della Brianza', 'Napoli', 'Novara', 'Nuoro', 'Olbia-Tempio', 'Oristano', 'Padova', 'Parma', 'Pavia', 'Perugia', 'Pesaro E Urbino', 'Pescara', 'Piacenza', 'Pisa', 'Pistoia', 'Potenza', 'Prato', 'Ravenna', 'Reggio Di Calabria', "Reggio Nell'Emilia", 'Rieti', 'Rimini', 'Roma', 'Rovigo', 'Salerno', 'Sassari', 'Savona', 'Siena', 'Sondrio', 'Taranto', 'Teramo', 'Terni', 'Torino', 'Trento', 'Treviso', 'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli', 'Verona', 'Vibo Valentia', 'Vicenza', 'Viterbo']
    
    failedMonth = ['Bergamo', 'Brescia', 'Civitavecchia', 'Colorno', 'Como', 'Cremona', 'Lecco', 'Lodi', 'Mantova', 'Milano', 'Monza E Della Brianza', 'Pavia', 'Sondrio', 'Varese', 'Verucchio', 'Villa Minozzo']
    missedCities = []
    for city in failedMonth:
        resMonth = getYearData(city)
        if len(resMonth["time_year"].keys()) != 0:
            print(city,"OK")
        else:
            missedCities.append(city)
            print(resMonth)
    print(missedCities)
    print(len(missedCities))

if __name__ == "__main__":
    # cities = ['Roma', 'MILANO', 'Firenze']
    # resMonth = getMonthData('Roma')

    # print(resMonth)
    # resYear = getYearData('Firenze')
    # print(resYear)
    test()
