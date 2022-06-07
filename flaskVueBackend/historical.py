from decimal import DivisionByZero
from flask import jsonify
import requests
import datetime as dt
import concurrent.futures


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
    print("querying moth data for {}".format(city))
    t = dt.datetime.now()
    startDay = t.replace(second = 59, minute = 59, hour=23) # end of today the starting day of query

    with concurrent.futures.ThreadPoolExecutor() as executor: # Execute queries asyncronously
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
    print("querying year data for {}".format(city))
    t = dt.datetime.now()
    startDay = t.replace(second = 59, minute = 59, hour=23) # end of today the starting day of query

    with concurrent.futures.ThreadPoolExecutor() as executor: #Run queries asyncronously
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

def queryByDay(startDay, endDay, city):
    inFormat = "%Y-%m-%dT%H%%3A%M%%3A%S" # Format to build query string
    utcFormat = "%Y-%m-%dT%H:%M:%S+00:00" # Format recieved from openAQ 

    d0 = startDay
    d1 = d0 - dt.timedelta(days = 1) # The day before 
    limit = 5000 # Number of results accepted per query. Fewer means better preformance but risk of missing data. 

    iter = 0
    paramUnits= {}
    res = {}

    maxPages = 10
    while d0 != endDay: # Looping until every day of the month is done
        # print("Querying day {}".format(iter+1),end="\r")
        page = 1
        getNextPage = True
        while getNextPage: #Looping though paginations
            d0String = d0.strftime(inFormat)+"%2B00%3A00"
            d1String = d1.strftime(inFormat)+"%2B00%3A00"
            url = f"https://api.openaq.org/v2/measurements?date_from={d1String}&date_to={d0String}&limit={limit}&page={page}&offset=0&sort=desc&radius=1000&city={city}&order_by=datetime"
            # print(url)

            r = requests.get(url)
            resJson = r.json()

            # When an empty page is recieved, goes on to next day. 
            if not resJson['results']:
                break

            if resJson['meta']['found'] < limit or page == maxPages:
                getNextPage = False
            else:
                if page == 1:
                    maxPages = resJson['meta']['found']// limit + 1
                    print(maxPages)

            page = page+1

            # When an empty page is recieved, goes on to next day. 
            if not resJson['results']:
                break

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
        
        # Advance date counters
        d0 = d1
        d1 = d0 - dt.timedelta(days = 1)

        # Safetybreak
        iter += 1
        if iter == 400:
            print("Error: Infinite loop.")
            break
        
    return res, paramUnits

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
