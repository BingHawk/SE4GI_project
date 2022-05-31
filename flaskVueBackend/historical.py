import requests
import datetime as dt

# t = dt.datetime.now()
# now = t.replace(second = 0, minute = 0)
# oneMonthAgo = now - dt.timedelta(days = 30)
# oneYearAgo  = now - dt.timedelta(days = 365)

# dateformat = "%Y-%m-%dT%H:%M:%S"
# print(now.strftime(dateformat)+"+00:00")
# print(oneMonthAgo.strftime(dateformat)+"+00:00")
# print(now.strftime(dateformat)+"+00:00")

cities = ['Roma', 'Milano', 'Firenze']

def getMonthData(city):
    inFormat = "%Y-%m-%dT%H%%3A%M%%3A%S" # Format to build query string
    outFormat = "%Y-%m-%dT%H:%M:%S+02:00" # Format recieved from openAQ 
    t = dt.datetime.now()
    d0 = t.replace(second = 0, minute = 0) # Today the starting day of query
    d1 = d0 - dt.timedelta(days = 1) # The day before 
    stopTime = d0 - dt.timedelta(days = 30) #iterate untill d0 == stoptime
    limit = 1000 # Number of results accepted per query
    maxlimit = 5000 # The max limit the program is allowed to raise to. 

    iter = 0
    paramUnits= {}
    res = {}
    while d0 != stopTime: # Looping until every day of the month is done
        page = 1
        while True: #Looping though paginations
            d0String = d0.strftime(inFormat)+"%2B00%3A00"
            d1String = d1.strftime(inFormat)+"%2B00%3A00"
            url = f"https://api.openaq.org/v2/measurements?date_from={d1String}&date_to={d0String}&limit={limit}&page={page}&offset=0&sort=desc&radius=1000&city={city}&order_by=datetime"
            page = page+1

            r = requests.get(url)
            resJson = r.json()
            if resJson['meta']['found'] > limit and limit < maxlimit:
                print("WARNING: The limit is lower than number of results, some results are lost")
                print("\tLimit: {}, Number of results: {}".format(limit, resJson['meta']['found']))
                if resJson['meta']['found'] < maxlimit:
                    print("\tRasing limit to {}".format(resJson['meta']['found']))
                    limit = resJson['meta']['found']
                else:
                    print("\tRasing limit to {}".format(maxlimit))
                    print("\tCannot raise limit more, at maxlimit")
                    limit = maxlimit
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
                day = dt.datetime.strptime(result['date']['local'],outFormat).replace(hour=0,minute=0,second=0)

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
        if iter == 40:
            print("Error: Infinite loop.")
            break
        
    return res


res = getMonthData('Firenze')
url2 = "https://api.openaq.org/v2/measurements?date_from=2022-04-01T00%3A00%3A00%2B00%3A00&date_to=2022-05-31T08%3A10%3A00%2B00%3A00&limit=100&page=1&offset=0&sort=desc&radius=1000&city=Roma&order_by=datetime"
